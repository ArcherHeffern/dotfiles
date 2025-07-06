from enum import Enum, auto
from pathlib import Path, PosixPath
from stat import S_IFMT

from install_types import Dest, GitRepo, Pair, Setting, Src
from install_utils import get_platform, has_unstaged_changes, have_same_directory_contents, have_same_file_contents, prompt_yn
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
    elif type(src) is Path or type(src) is PosixPath:
        if S_IFMT(src.stat().st_mode) != S_IFMT(dest.stat().st_mode):
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
        raise NotImplementedError(f"Unreachable! {type(src)}")

class Status(Enum):
    PASSED = auto()
    SKIPPED = auto()
    FAILED = auto()
def process_pair(pair: Pair) -> Status:
    try:
        if not can_update(pair.src, pair.dest):
            return Status.SKIPPED
        # Delete dest if it exists
        # Copy src into dest
        # Chmod 
    except:
        return Status.FAILED
    return Status.PASSED
    
    
    
    ...
if __name__ == '__main__':
    passed: list[Setting] = []
    skipped: list[Setting] = []
    failed: list[Setting] = []
    for setting in settings:
        if setting.platform is not None and get_platform() not in setting.platform:
            print(f"Skipping {setting.name}. Intended for {",".join([p.value for p in setting.platform])}")
            continue
        print(f"Running {setting.name}")
        run_callback = False
        for pair in setting.src_dest_pairs:
            match process_pair(pair):
                case Status.PASSED:
                    passed.append(setting)
                    run_callback = True
                case Status.SKIPPED:
                    skipped.append(setting)
                case Status.FAILED:
                    failed.append(setting)
        if run_callback and setting.callback:
            error_msg = setting.callback(setting)
            if error_msg:
                print(error_msg)
                continue
    for each_passed in passed:
        if each_passed.final_message:
            print(f"{each_passed.name}: {each_passed.final_message}")