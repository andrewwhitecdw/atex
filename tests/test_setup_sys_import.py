"""Regression test for missing `import sys` in setup.py."""

import ast
import pathlib


def test_setup_py_imports_sys():
    """setup.py must import `sys` because `build_cmake()` calls `sys.stdout.flush()`."""
    setup_path = pathlib.Path(__file__).resolve().parent.parent / "setup.py"
    source = setup_path.read_text()
    tree = ast.parse(source)

    imports_sys = any(
        isinstance(node, ast.Import)
        and any(alias.name == "sys" for alias in node.names)
        for node in ast.walk(tree)
    )

    assert imports_sys, "setup.py imports sys so build_cmake() can call sys.stdout.flush()"


def test_setup_py_can_flush_stdout():
    """Importing setup.py must not raise NameError on `sys.stdout.flush()`."""
    setup_path = pathlib.Path(__file__).resolve().parent.parent / "setup.py"
    source = setup_path.read_text()
    assert "sys.stdout.flush()" in source
