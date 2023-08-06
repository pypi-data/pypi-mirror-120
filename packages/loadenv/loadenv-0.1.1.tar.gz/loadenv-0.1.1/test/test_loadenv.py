# type: ignore
from contextlib import contextmanager
from dataclasses import dataclass
import os
from typing import Optional

import pytest

from loadenv import EnvEnum, loadenv_into_dataclass

@contextmanager
def override_env(env_vars):
    old_env, os.environ = os.environ, env_vars
    yield
    os.environ = old_env


simple_bool_parameters = [
    ({"FOO": "True"}, True),
    ({"FOO": "true"}, True),
    ({"FOO": "TRUE"}, True),
    ({"FOO": "yes"}, True),
    ({"FOO": "y"}, True),
    ({"FOO": "on"}, True),
    ({"FOO": "False"}, False),
    ({"FOO": "false"}, False),
    ({"FOO": "FALSE"}, False),
    ({"FOO": "no"}, False),
    ({"FOO": "n"}, False),
    ({"FOO": "off"}, False),
]
@pytest.mark.parametrize("env,loadedenv", simple_bool_parameters)
def test_simple_bool_dataclass(env, loadedenv):
    @dataclass
    class TestSimpleBoolDataclass:
        FOO: bool
    with override_env(env):
        loaded_dataclass = loadenv_into_dataclass(TestSimpleBoolDataclass)
        loaded_dataclass.FOO == loadedenv
@pytest.mark.parametrize("env,loadedenv", simple_bool_parameters)
def test_simple_bool_envenum(env, loadedenv):
    with override_env(env):
        class TestSimpleBoolEnvEnum(EnvEnum):
            FOO: bool = ()
        assert TestSimpleBoolEnvEnum.FOO.value == loadedenv


simple_float_parameters = [
    ({"FOO": ".0"}, 0.0),
    ({"FOO": "0.0"}, 0.0),
    ({"FOO": "1."}, 1.0),
    ({"FOO": "-1.0"}, -1.0),
    ({"FOO": "-1.1"}, -1.1),
    ({"FOO": "01.10"}, 1.1),
    ({"FOO": "000001.01"}, 1.01),
    ({"FOO": ".1_234"}, 0.1234),
    ({"FOO": "1_2.3_4"}, 12.34),
    ({"FOO": "0_1."}, 1.0),
    ({"FOO": "11111111111111111111111111111111."}, 11111111111111111111111111111111.),
    ({"FOO": ".11111111111111111111111111111111"}, .11111111111111111111111111111111),
    ({"FOO": "0e0"}, 0e0),
    ({"FOO": "1e100"}, 1e100),
    ({"FOO": "-1e-1_00"}, -1e-100),
]
@pytest.mark.parametrize("env,loadedenv", simple_float_parameters)
def test_simple_float_dataclass(env, loadedenv):
    @dataclass
    class TestSimpleFloatDataclass:
        FOO: float
    with override_env(env):
        loaded_dataclass = loadenv_into_dataclass(TestSimpleFloatDataclass)
        loaded_dataclass.FOO == loadedenv
@pytest.mark.parametrize("env,loadedenv", simple_float_parameters)
def test_simple_float_envenum(env, loadedenv):
    with override_env(env):
        class TestSimpleFloatEnvEnum(EnvEnum):
            FOO: float = ()
        assert TestSimpleFloatEnvEnum.FOO.value == loadedenv
@pytest.mark.parametrize("env,loadedenv", simple_float_parameters)
def test_simple_float_functional_envenum(env, loadedenv):
    with override_env(env):
        envenum = EnvEnum("envenum", {"FOO": float})
        assert envenum.FOO.value == loadedenv


simple_int_parameters = [
    ({"FOO": "1"}, 1),
    ({"FOO": "-11"}, -11),
    ({"FOO": "0101"}, 101),
    ({"FOO": "00000101"}, 101),
    ({"FOO": "1_234"}, 1234),
    ({"FOO": "1_2_3_4"}, 1234),
    ({"FOO": "0_1"}, 1),
    ({"FOO": "11111111111111111111111111111111"}, 11111111111111111111111111111111),
]
@pytest.mark.parametrize("env,loadedenv", simple_int_parameters)
def test_simple_int_dataclass(env, loadedenv):
    @dataclass
    class TestSimpleIntDataclass:
        FOO: int
    with override_env(env):
        loaded_dataclass = loadenv_into_dataclass(TestSimpleIntDataclass)
        loaded_dataclass.FOO == loadedenv
@pytest.mark.parametrize("env,loadedenv", simple_int_parameters)
def test_simple_int_envenum(env, loadedenv):
    with override_env(env):
        class TestSimpleIntEnvEnum(EnvEnum):
            FOO: int = ()
        assert TestSimpleIntEnvEnum.FOO.value == loadedenv
@pytest.mark.parametrize("env,loadedenv", simple_int_parameters)
def test_simple_int_functional_envenum(env, loadedenv):
    with override_env(env):
        envenum = EnvEnum("envenum", {"FOO": int})
        assert envenum.FOO.value == loadedenv


simple_string_parameters = [
    ({"FOO": ""}, ""),
    ({"FOO": "foo"}, "foo"),
    ({"FOO": "foo bar"}, "foo bar"),
    ({"FOO": "None"}, "None"),
    ({"FOO": "12"}, "12"),
]
@pytest.mark.parametrize("env,loadedenv", simple_string_parameters)
def test_simple_string_dataclass(env, loadedenv):
    @dataclass
    class TestSimpleStringDataclass:
        FOO: str
    with override_env(env):
        loaded_dataclass = loadenv_into_dataclass(TestSimpleStringDataclass)
        loaded_dataclass.FOO == loadedenv
@pytest.mark.parametrize("env,loadedenv", simple_string_parameters)
def test_simple_string_envenum(env, loadedenv):
    with override_env(env):
        class TestSimpleStringEnvEnum(EnvEnum):
            FOO: str = ()
        assert TestSimpleStringEnvEnum.FOO.value == loadedenv
@pytest.mark.parametrize("env,loadedenv", simple_string_parameters)
def test_simple_string_functional_envenum(env, loadedenv):
    with override_env(env):
        envenum = EnvEnum("envenum", {"FOO": str})
        assert envenum.FOO.value == loadedenv


simple_bytes_parameters = [
    ({"FOO": ""}, b""),
    ({"FOO": "foo"}, b"foo"),
    ({"FOO": "foo bar"}, b"foo bar"),
    ({"FOO": "None"}, b"None"),
    ({"FOO": "12"}, b"12"),
]
@pytest.mark.parametrize("env,loadedenv", simple_bytes_parameters)
def test_simple_bytes_dataclass(env, loadedenv):
    @dataclass
    class TestSimpleBytesDataclass:
        FOO: bytes
    with override_env(env):
        loaded_dataclass = loadenv_into_dataclass(TestSimpleBytesDataclass)
        loaded_dataclass.FOO == loadedenv
@pytest.mark.parametrize("env,loadedenv", simple_bytes_parameters)
def test_simple_bytes_envenum(env, loadedenv):
    with override_env(env):
        class TestSimpleBytesEnvEnum(EnvEnum):
            FOO: bytes = ()
        assert TestSimpleBytesEnvEnum.FOO.value == loadedenv


simple_optional_parameters = [
    ({}, None),
    ({"FOO": ""}, ""),
    ({"FOO": "foo"}, "foo"),
    ({"BAR": "unrelated"}, None),
]
@pytest.mark.parametrize("env,loadedenv", simple_optional_parameters)
def test_simple_optional_dataclass(env, loadedenv):
    @dataclass
    class TestSimpleStringDataclass:
        FOO: Optional[str]
    with override_env(env):
        loaded_dataclass = loadenv_into_dataclass(TestSimpleStringDataclass)
        loaded_dataclass.FOO == loadedenv
@pytest.mark.parametrize("env,loadedenv", simple_optional_parameters)
def test_simple_optional_envenum(env, loadedenv):
    with override_env(env):
        class TestSimpleStringEnvEnum(EnvEnum):
            FOO: Optional[str] = ()
        assert TestSimpleStringEnvEnum.FOO.value == loadedenv


simple_list_parameters = [
    ({"FOO": "[]"}, []),
    ({"FOO": " [  ] "}, []),
    ({"FOO": "[,]"}, []),
    ({"FOO": "None"}, "None"),
    ({"FOO": "12"}, "12"),
]
@pytest.mark.parametrize("env,loadedenv", simple_list_parameters)
def test_simple_list_dataclass(env, loadedenv):
    @dataclass
    class TestSimpleListDataclass:
        FOO: list = ()
    with override_env(env):
        loaded_dataclass = loadenv_into_dataclass(TestSimpleListDataclass)
        loaded_dataclass.FOO == loadedenv
@pytest.mark.parametrize("env,loadedenv", simple_list_parameters)
def test_simple_list_envenum(env, loadedenv):
    with override_env(env):
        class TestSimpleListEnvEnum(EnvEnum):
            FOO: list = ()

        assert TestSimpleListEnvEnum.FOO.value == loadedenv
