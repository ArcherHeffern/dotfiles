from io import TextIOBase
from pathlib import Path
from platform import system
from subprocess import run
from sys import stderr
from typing import Optional
from install_types import Platform

def prompt_yn(msg: str) -> bool:
    while True:
        r = input(msg)
        if r in ["y", "yes"]:
            return True
        if r in ["n", "no"]:
            return False

def get_platform() -> "Platform":
    match system():
        case 'Windows':
            return Platform.WINDOWS
        case 'Linux':
            return Platform.LINUX
        case 'Darwin':
            return Platform.MACOS
        case _:
            return Platform.UNKNOWN

def get_effective_user_id() -> Optional[int]:
    if get_platform() != Platform.MACOS:
        return None

    a = run(["id", "-u"], capture_output=True)
    if a.returncode != 0:
        return None
    try:
        return int(a.stdout.decode())
    except:
        return None

def has_unstaged_changes(repo: Path) -> bool:
    raise NotImplementedError("Not implemented")

def have_same_file_contents(src: Path, dest: Path) -> bool:
    with open(src, "r", encoding="utf-8") as s_f, open(dest, "r", encoding="utf-8") as d_f:
        return _have_same_file_contents(s_f, d_f)
            
def _have_same_file_contents(src: TextIOBase, dest: TextIOBase) -> bool:
    try:
        for s_line, d_line in zip(src, dest, strict=True):
            if s_line != d_line:
                return False
        return True
    except ValueError:
        return False

def have_same_directory_contents(src: Path, dest: Path) -> bool:
    try:
        for a, b in zip(src.walk(), dest.walk(), strict=True):
            for dir_group_a_entry, dir_group_b_entry in zip(a[1], b[1], strict=True):
                if dir_group_a_entry != dir_group_b_entry:
                    return False
            for file_group_a_entry, file_group_b_entry in zip(a[2], b[2], strict=True):
                if file_group_a_entry != file_group_b_entry:
                    return False
                if not have_same_file_contents(a[0]/file_group_a_entry, b[0]/file_group_b_entry):
                    return False
    except ValueError:
        return False
    return True

def eprint(msg: str, red=False):
    if red:
        print(f"\033[91m{msg}\033[0m", file=stderr)
    else:
        print(msg, file=stderr)