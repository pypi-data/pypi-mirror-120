from __future__ import annotations

import contextlib
from datetime import datetime, timedelta, timezone
import os.path
import tempfile
from typing import Any, TypedDict

from pulumi import Input, Output
from pulumi.automation import (
    ConfigValue as _PulumiConfigValue, LocalWorkspaceOptions, StackSettings,
    create_or_select_stack, select_stack,
)
from pulumi.dynamic import ResourceProvider
from pulumi.dynamic.dynamic import (CreateResult, DiffResult, Resource, UpdateResult)

from .config import Config
from .subprocess_run import subprocess_run


class _Inputs(TypedDict):
    stack_name: str
    deployment_dir: str

    repository_url: str

    backend_url: str
    secrets_provider: str
    backend_azure_storage_account: str

    config: Config
    repository_ref: str
    commands: list[str]
    always_deploy: bool
    outputs: dict[str, Any]


class RemoteStack(
    Resource,
    module="remote_stack",
    name="Remotestack",
):
    deployment: Output[dict]
    stack_name: Output[str]
    config: Output[dict]
    outputs: Output[dict[str, Any]]

    def __init__(
        self,
        name: str,
        stack_name: Input[str],
        deployment_dir: Input[str],

        repository_url: Input[str],

        backend_url: Input[str],
        secrets_provider: Input[str],
        backend_azure_storage_account: Input[str],

        repository_ref: Input[str] = '',
        commands: Input[list[str]] = None,
        config: Input[Config] = None,
        always_deploy: Input[bool] = False,
        opts=None,
    ):
        commands = commands or []
        config = config or {}
        props: _Inputs = {
            "stack_name": stack_name,
            "deployment_dir": deployment_dir,
            "repository_url": repository_url,

            "backend_url": backend_url,
            "secrets_provider": secrets_provider,
            "backend_azure_storage_account": backend_azure_storage_account,
            "config": config,
            "repository_ref": repository_ref,
            "commands": commands,
            "always_deploy": always_deploy,
            "outputs": {},
        }

        super().__init__(
            RemoteStackProvider(),
            name,
            props,
            opts
        )


def generate_user_sas(azure_storage_account):
    expiry = (datetime.now(timezone.utc) + timedelta(minutes=20)).strftime(
        '%Y-%m-%dT%H:%MZ'
    )

    return subprocess_run(
        [
            "az", "storage", "container", "generate-sas", "--account-name",
            azure_storage_account, "--name", "pulumi", "--permissions", "acdlrw",
            "--expiry", expiry, "--as-user", "--auth-mode", "login", "-o", "tsv"
        ],
        env=os.environ,
    )


class RemoteStackProvider(ResourceProvider):
    def _prepare_runtime(
        self,
        deployment_dir: str,
        repository_url: str,
        repository_ref: str,
        commands: list[str],
        tmp_dir,
    ) -> tuple[str, str, dict[str, str]]:

        subprocess_run(["git", "init", tmp_dir])
        subprocess_run(
            ["git", "remote", "add", "origin", repository_url],
            cwd=tmp_dir,
        )
        subprocess_run(
            ["git", "fetch", "origin", f"{repository_ref}:local"],
            cwd=tmp_dir,
            env=os.environ
        )
        subprocess_run(
            ["git", "checkout", "local"],
            cwd=tmp_dir
        )
        subprocess_run(
            ["git", "submodule", "update", "--init", "--recursive"],
            cwd=tmp_dir,
            env=os.environ,
        )

        deployment_dir = os.path.join(tmp_dir, deployment_dir)

        for command in commands:
            subprocess_run(
                command.split(),
                cwd=deployment_dir,
                env=os.environ,
            )

        virtualenv_path = os.path.join(tmp_dir, ".venv")

        subprocess_run(["python3", "-m", "venv", virtualenv_path], env=os.environ)

        virtualenv_python = os.path.join(virtualenv_path, "bin", "python")

        subprocess_run([virtualenv_python, "-m", "pip", "install", "--upgrade", "pip"])

        # TODO remove
        subprocess_run([virtualenv_python, "-m", "pip", "install", "pyyaml"])

        # TODO do it with shell command
        deployment_name = subprocess_run(
            [
                virtualenv_python,
                "-c",
                'import yaml;print(yaml.load(open("Pulumi.yaml"), Loader=yaml.SafeLoader).get("name", ""))'
            ],
            cwd=deployment_dir,
        )

        src_dir = subprocess_run(
            [
                virtualenv_python,
                "-c",
                'import yaml;print(yaml.load(open("Pulumi.yaml"), Loader=yaml.SafeLoader).get("main", ""))'
            ],
            cwd=deployment_dir,
        )

        subprocess_run(
            [
                virtualenv_python, "-m", "pip", "install", "-r",
                os.path.join(deployment_dir, src_dir, "requirements.txt")
            ],
            cwd=tmp_dir,
        )
        return deployment_name, deployment_dir, {
            "VIRTUAL_ENV": virtualenv_path,
            "PATH": f"{virtualenv_path}/bin:{os.environ['PATH']}",
        }

    @contextlib.contextmanager
    def _prepare_environment(
        self,
        deployment_dir: str,
        repository_url: str,
        repository_ref: str,
        commands: list[str],
        backend_azure_storage_account: str,
    ) -> tuple[str, str, dict[str, str]]:
        with tempfile.TemporaryDirectory() as tmp_dir:
            deployment_name, work_dir, runtime_vars = self._prepare_runtime(
                deployment_dir=deployment_dir,
                repository_url=repository_url,
                repository_ref=repository_ref,
                commands=commands,
                tmp_dir=tmp_dir,
            )
            yield deployment_name, work_dir, {
                **runtime_vars,
                "AZURE_STORAGE_ACCOUNT": backend_azure_storage_account,
                "AZURE_STORAGE_SAS_TOKEN": generate_user_sas(
                    backend_azure_storage_account
                )
            }

    def _create_or_update(self, inputs: _Inputs) -> tuple[str, dict[str, Any]]:
        stack_name = inputs['stack_name']
        config = inputs['config']
        deployment_dir = inputs['deployment_dir']
        repository_url = inputs['repository_url']
        repository_ref = inputs['repository_ref']
        backend_azure_storage_account = inputs['backend_azure_storage_account']
        secrets_provider = inputs['secrets_provider']
        commands = inputs['commands']

        with self._prepare_environment(
            deployment_dir=deployment_dir,
            repository_url=repository_url,
            repository_ref=repository_ref,
            backend_azure_storage_account=backend_azure_storage_account,
            commands=commands,
        ) as (
            deployment_name, work_dir, env_vars
        ):
            stack_settings = StackSettings(
                secrets_provider=secrets_provider,
            )
            stack = create_or_select_stack(
                stack_name=stack_name,
                work_dir=work_dir,
                opts=LocalWorkspaceOptions(
                    secrets_provider=secrets_provider,
                    stack_settings={stack_name: stack_settings},
                    env_vars=env_vars,
                )
            )
            stack.set_all_config({
                key: _PulumiConfigValue(
                    value=config_value["value"],
                    secret=config_value["secret"],
                )
                for key, config_value in config.items()
            })

            up_result = stack.up()

            # TODO solve how to make an output secret when output_value.secret
            outputs = {
                key: output_value.value
                for key, output_value in up_result.outputs.items()
            }
            return deployment_name, outputs

    def create(self, inputs: _Inputs):
        stack_name = inputs['stack_name']
        deployment_name, outputs = self._create_or_update(inputs)
        return CreateResult(
            f"{deployment_name}-{stack_name}",
            outs={**inputs, "outputs": outputs}
        )

    def delete(self, id, inputs: _Inputs):
        stack_name = inputs['stack_name']
        deployment_dir = inputs['deployment_dir']
        repository_url = inputs['repository_url']
        repository_ref = inputs['repository_ref']
        backend_azure_storage_account = inputs['backend_azure_storage_account']
        secrets_provider = inputs['secrets_provider']
        commands = inputs['commands']
        with self._prepare_environment(
            deployment_dir=deployment_dir,
            repository_url=repository_url,
            repository_ref=repository_ref,
            backend_azure_storage_account=backend_azure_storage_account,
            commands=commands,
        ) as (
            deployment_name, work_dir, env_vars
        ):
            stack_settings = StackSettings(
                secrets_provider=secrets_provider,
            )
            stack = select_stack(
                stack_name=stack_name,
                work_dir=work_dir,
                opts=LocalWorkspaceOptions(
                    secrets_provider=secrets_provider,
                    stack_settings={stack_name: stack_settings},
                    env_vars=env_vars,
                )
            )
            stack.destroy()

    def diff(self, id, old_inputs: _Inputs, new_inputs: _Inputs):
        replaces = []
        del old_inputs["outputs"]
        del new_inputs["outputs"]
        # TODO fix always_deploy True -> False transition
        return DiffResult(
            changes=new_inputs["always_deploy"] or (old_inputs != new_inputs),
            replaces=replaces,
            stables=None,
            delete_before_replace=True
        )

    def update(self, id, old_inputs: _Inputs, new_inputs: _Inputs):
        deployment_name, outputs = self._create_or_update(new_inputs)
        return UpdateResult(outs={**new_inputs, "outputs": outputs})
