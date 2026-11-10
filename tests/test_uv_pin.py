"""Tests for the CI step that compares the uv binary and the uv floor with the uv_build pin."""

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

SCRIPT: Path = Path(__file__).resolve().parent.parent / ".github" / "scripts" / "check_uv_pin.py"
VERSION: str = "1.2.3"
UV_TEXT: str = "uv 1.2.3 (abc 2026-01-01 x86_64-unknown-linux-gnu)"


def _load() -> ModuleType:
    spec = importlib.util.spec_from_file_location("check_uv_pin", SCRIPT)
    assert spec is not None
    assert spec.loader is not None
    module: ModuleType = importlib.util.module_from_spec(spec)
    previous: bool = sys.dont_write_bytecode
    sys.dont_write_bytecode = True  # keep .pyc files out of the repo tree
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = previous
    return module


check_uv_pin: ModuleType = _load()


FLOOR_TABLE: str = f'[tool.uv]\nrequired-version = ">={VERSION}"\n'


def _pyproject(
    requires: str = f'["uv_build=={VERSION}"]',
    backend: str = '"uv_build"',
    extra: str = "",
    floor: str = FLOOR_TABLE,
) -> str:
    return f"[build-system]\nrequires = {requires}\nbuild-backend = {backend}\n{extra}\n{floor}"


def _run(
    tmp_path: Path,
    text: str,
    expected: str = VERSION,
    uv_text: str = UV_TEXT,
    capsys: pytest.CaptureFixture[str] | None = None,
) -> tuple[int, str]:
    path: Path = tmp_path / "pyproject.toml"
    path.write_text(text, encoding="utf-8", newline="\n")
    code: int = check_uv_pin.main([str(path), expected, uv_text])
    out: str = capsys.readouterr().out if capsys is not None else ""
    return code, out


def test_matching_values_pass(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert _run(tmp_path, _pyproject(), capsys=capsys) == (0, "check_uv_pin: ok\n")


@pytest.mark.parametrize(
    ("text", "expected", "uv_text"),
    [
        (_pyproject(), "1.2.4", UV_TEXT),
        (_pyproject(), VERSION, "uv 1.2.4 (abc)"),
        (_pyproject(), "", UV_TEXT),
        (_pyproject(), VERSION, ""),
        (_pyproject(), VERSION, "uv"),
        (_pyproject('["uv_build>=1.2.3"]'), VERSION, UV_TEXT),
        (_pyproject("[\"uv_build==1.2.3; sys_platform == 'linux'\"]"), VERSION, UV_TEXT),
        (_pyproject('["uv_build[x]==1.2.3"]'), VERSION, UV_TEXT),
        (_pyproject('["uv_build ==1.2.3"]'), VERSION, UV_TEXT),
        (_pyproject('["uv_build==1.2.3", "uv-build==1.2.3"]'), VERSION, UV_TEXT),
        (_pyproject('["UV_Build==1.2.3"]'), VERSION, UV_TEXT),
        (_pyproject("[]"), VERSION, UV_TEXT),
        (_pyproject('["uv_build==1.2.3rc1"]'), VERSION, "uv 1.2.3rc1 (abc)"),
        (_pyproject('["uv_build==١.2.3"]'), "١.2.3", "uv ١.2.3 (abc)"),
        (_pyproject(backend='"hatchling.build"'), VERSION, UV_TEXT),
        (_pyproject(backend='""'), VERSION, UV_TEXT),
        ("[build-system]\nrequires = []\n", VERSION, UV_TEXT),
        (_pyproject(extra='backend-path = ["."]\n'), VERSION, UV_TEXT),
        ("[project]\nname = 'x'\n", VERSION, UV_TEXT),
        (_pyproject('"uv_build==1.2.3"'), VERSION, UV_TEXT),
        (_pyproject("[1]"), VERSION, UV_TEXT),
        ("[build-system\n", VERSION, UV_TEXT),
    ],
)
def test_each_mismatch_fails_with_one_line(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], text: str, expected: str, uv_text: str
) -> None:
    code, out = _run(tmp_path, text, expected, uv_text, capsys)
    assert code == 1
    assert out.startswith("check_uv_pin:")
    assert out.count("\n") == 1
    assert "Traceback" not in out


def test_the_wrong_number_of_arguments_fails(capsys: pytest.CaptureFixture[str]) -> None:
    assert check_uv_pin.main(["only-one"]) == 1
    assert capsys.readouterr().out.startswith("check_uv_pin: usage")


def test_a_missing_file_fails(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert check_uv_pin.main([str(tmp_path / "absent.toml"), VERSION, UV_TEXT]) == 1
    assert capsys.readouterr().out.startswith("check_uv_pin:")


def _fails_with(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], text: str, message: str
) -> None:
    code, out = _run(tmp_path, text, capsys=capsys)
    assert code == 1
    assert out.startswith("check_uv_pin:")
    assert out.count("\n") == 1
    assert "Traceback" not in out
    assert message in out


@pytest.mark.parametrize("floor", [">=1.2.2", ">=1.2.4"])
def test_a_floor_that_differs_from_the_pin_fails(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], floor: str
) -> None:
    text: str = _pyproject(floor=f'[tool.uv]\nrequired-version = "{floor}"\n')
    _fails_with(tmp_path, capsys, text, "the uv floor in required-version differs")


@pytest.mark.parametrize(
    "text",
    [
        _pyproject(floor=""),
        _pyproject(floor="[tool]\nuv = 1\n"),
        _pyproject(floor="[tool.ruff]\nline-length = 99\n"),
        "tool = 1\n" + _pyproject(floor=""),
    ],
)
def test_a_missing_uv_table_fails(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], text: str
) -> None:
    _fails_with(tmp_path, capsys, text, "no [tool.uv] table")


@pytest.mark.parametrize("floor", ["[tool.uv]\n", "[tool.uv]\nrequired-version = 1\n"])
def test_a_missing_floor_string_fails(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], floor: str
) -> None:
    _fails_with(tmp_path, capsys, _pyproject(floor=floor), "no [tool.uv].required-version string")


@pytest.mark.parametrize(
    "floor",
    [
        "==1.2.3",
        ">1.2.3",
        ">= 1.2.3",
        ">=1.2.3,<2",
        ">=1.2",
        ">=1.2.3rc1",
        ">=١.2.3",
        ">=1.2.3\\n",
        "",
    ],
)
def test_a_malformed_floor_fails(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], floor: str
) -> None:
    text: str = _pyproject(floor=f'[tool.uv]\nrequired-version = "{floor}"\n')
    _fails_with(tmp_path, capsys, text, "must be exactly >=X.Y.Z")


@pytest.mark.parametrize("dangling", [False, True])
def test_a_uv_toml_beside_the_pyproject_fails(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], dangling: bool
) -> None:
    if dangling:
        (tmp_path / "uv.toml").symlink_to(tmp_path / "absent-target")
    else:
        (tmp_path / "uv.toml").write_text("", encoding="utf-8")
    _fails_with(tmp_path, capsys, _pyproject(), "a uv.toml beside pyproject.toml")
