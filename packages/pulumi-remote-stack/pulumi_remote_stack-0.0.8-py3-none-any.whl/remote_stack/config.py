from __future__ import annotations

from functools import singledispatch
import json
from typing import TypedDict, Union

import pulumi
from pulumi import Output


class ConfigValue(TypedDict):
    value: str
    secret: bool
    type: str


@singledispatch
def _config_value(value: Union[dict, list, int, bool], secret: bool = False):
    return {
        "value": json.dumps(value),
        "secret": secret,
        "type": "object",
    }


@_config_value.register
def _config_value_str(value: str, secret: bool = False) -> ConfigValue:
    return {"value": value, "secret": secret, "type": "str"}


def config_value(value, secret: bool = False) -> pulumi.Output[ConfigValue]:
    return Output.from_input(value).apply(
        lambda val:
        _config_value(val, secret)
    )


Config = dict[str, ConfigValue]
