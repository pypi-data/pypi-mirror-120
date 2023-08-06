from __future__ import annotations

from datetime import datetime, timedelta, timezone
import os
from typing import TypedDict

from pulumi import Input, Output
from pulumi.automation import (
    ConfigValue as _PulumiConfigValue, LocalWorkspace, LocalWorkspaceOptions,
    ProjectBackend, ProjectSettings, PulumiFn, StackSettings, create_or_select_stack,
    create_stack,
)
from pulumi.dynamic import (
    CreateResult, DiffResult, Resource, ResourceProvider, UpdateResult
)

from .config import Config, ConfigValue
from .subprocess_run import subprocess_run


class _Inputs(TypedDict):
    project_name: str
    stack_name: str
    backend_url: str
    secrets_provider: str
    backend_azure_storage_account: str
    config: Config
    only_create: bool
    output_config: bool


class RemoteConfig(
    Resource,
    module="remote_stack",
    name="RemoteConfig"
):
    project_name: Output[str]
    stack_name: Output[str]
    backend_url: Output[str]
    secrets_provider: Output[str]
    backend_azure_storage_account: Output[str]
    config: Output[dict]
    only_create: Output[bool]
    output_config: Output[bool]

    def __init__(
        self,
        name: str,
        project_name: Input[str],
        stack_name: Input[str],
        backend_url: Input[str],
        secrets_provider: Input[str],
        backend_azure_storage_account: Input[str],
        config: Input[Config],
        only_create: Input[bool] = False,
        output_config: Input[bool] = True,
        opts=None
    ):
        props: _Inputs = {
            "project_name": project_name,
            "stack_name": stack_name,
            "backend_url": backend_url,
            "secrets_provider": secrets_provider,
            "backend_azure_storage_account": backend_azure_storage_account,
            "config": config,
            "only_create": only_create,
            "output_config": output_config,
        }
        super().__init__(
            RemoteConfigProvider(),
            name,
            props,
            opts
        )


def generate_user_sas(azure_storage_account: str) -> str:
    expiry = (datetime.now(timezone.utc) + timedelta(minutes=5)).strftime(
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


def generate_program(stack_config: dict[str, ConfigValue]) -> PulumiFn:
    def _pulumi_program() -> None:
        import pulumi
        config = pulumi.Config()
        for name, value_dict in stack_config.items():
            if value_dict["secret"]:
                secret = "_secret"
            else:
                secret = ""
            if value_dict['type'] == "str":
                kind = ""
            else:
                kind = f"_{value_dict['type']}"
            method_name = f"get{secret}{kind}"
            pulumi.export(name, getattr(config, method_name)(name))

    return _pulumi_program


class RemoteConfigProvider(ResourceProvider):

    def _setup_project_stack(self, inputs: _Inputs, ):
        project_name = inputs['project_name']
        stack_name = inputs['stack_name']
        backend_url = inputs['backend_url']
        backend_azure_storage_account = inputs['backend_azure_storage_account']
        secrets_provider = inputs['secrets_provider']
        config = inputs['config']
        only_create = inputs['only_create']
        output_config = inputs['output_config']
        pulumi_program = generate_program(config)

        project_settings = ProjectSettings(
            name=project_name,
            runtime="python",
            backend=ProjectBackend(url=backend_url),
        )

        stack_settings = StackSettings(
            secrets_provider=secrets_provider
        )

        env_vars = {
            'AZURE_STORAGE_ACCOUNT': backend_azure_storage_account,
            'AZURE_STORAGE_SAS_TOKEN': generate_user_sas(backend_azure_storage_account),
        }

        kwargs = {
            "project_name": project_name,
            "stack_name": stack_name,
            "program": pulumi_program if output_config else lambda: None,
            "opts": LocalWorkspaceOptions(
                project_settings=project_settings,
                secrets_provider=secrets_provider,
                stack_settings={stack_name: stack_settings},
                env_vars=env_vars,
            )
        }

        if only_create:
            stack = create_stack(**kwargs)
        else:
            stack = create_or_select_stack(**kwargs)

        stack.set_all_config({
            key: _PulumiConfigValue(
                value=config_value["value"],
                secret=config_value["secret"],
            )
            for key, config_value in config.items()
        })

        stack.up()

    def create(self, inputs: _Inputs):
        project_name = inputs['project_name']
        stack_name = inputs['stack_name']
        self._setup_project_stack(inputs)
        return CreateResult(f"{project_name}-{stack_name}", outs=inputs)

    def delete(self, id: str, inputs: _Inputs):
        project_name = inputs['project_name']
        stack_name = inputs['stack_name']
        backend_url = inputs['backend_url']
        backend_azure_storage_account = inputs['backend_azure_storage_account']

        env_vars = {
            'AZURE_STORAGE_ACCOUNT': backend_azure_storage_account,
            'AZURE_STORAGE_SAS_TOKEN': generate_user_sas(backend_azure_storage_account),
        }

        project_settings = ProjectSettings(
            name=project_name,
            runtime="python",
            backend=ProjectBackend(url=backend_url),
        )

        local_workspace = LocalWorkspace(
            project_settings=project_settings,
            env_vars=env_vars,
        )

        local_workspace._run_pulumi_cmd_sync(
            # TODO fill pulumi issue --force in remove_stack
            ["stack", "rm", "--yes", "--force", stack_name]
        )

    def diff(self, id: str, old_inputs: _Inputs, new_inputs: _Inputs):
        replaces = []
        if old_inputs["project_name"] != new_inputs["project_name"]:
            replaces.append("project_name")
        if old_inputs["stack_name"] != new_inputs["stack_name"]:
            replaces.append("stack_name")
        return DiffResult(
            changes=old_inputs != new_inputs,
            replaces=replaces,
            stables=None,
            delete_before_replace=True
        )

    def update(self, id: str, old_inputs: _Inputs, new_inputs: _Inputs):
        self._setup_project_stack(new_inputs)
        return UpdateResult(outs=new_inputs)
