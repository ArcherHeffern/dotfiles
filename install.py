from pathlib import Path

from install_types import Dest, GitRepo, Setting, Src
from install_utils import has_unstaged_changes, have_same_directory_contents, have_same_file_contents, prompt_yn
from install_config import settings


def can_update(src: Src, dest: Dest):
    """
    If dest does not exist, or if src and dest are different
    """
    if not dest.exists():
        return True

    if type(src) is GitRepo:
        if has_unstaged_changes(dest):
            return prompt_yn(f"{dest} has unstaged changes. Overwrite anyways? (y/n) ")
        return False # TODO: May want to prompt anyways since there may be ignored files we would like to keep
    elif type(src) is Path:
        if src.stat().st_mode != dest.stat().st_mode:
            return prompt_yn(f"{src} and {dest} are not the same File System Object. eg. File vs Directory. Overwrite? (y/n) ")
        elif src.is_file():
            if have_same_file_contents(src, dest):
                return False
            return prompt_yn(f"{src} and {dest} have different file contents. Overwrite {dest}? (y/n) ")
        elif src.is_dir():
            if have_same_directory_contents(src, dest):
                return False
            return prompt_yn(f"{src} and {dest} have different directory contents. Overwrite {dest}? The entire directory will be removed. (y/n) ")
        else:
            raise NotImplementedError("Only copying files and directories is supported.")
    else:
        raise NotImplementedError("Unreachable!")

if __name__ == '__main__':
    passed: list[Setting] = []
    skipped: list[Setting] = []
    failed: list[Setting] = []
    for setting in settings:
        print(f"Running {setting.name}")