from enum import Enum, auto
from pathlib import Path
from subprocess import run
from stat import S_IFMT
from shutil import copy, copytree, rmtree

from install_types import Dest, GitRepo, Pair, Setting, Src
from install_utils import ANSI_CLEAR_FORMATTING, ANSI_UNDERLINE, eprint, get_platform, git_status, have_same_directory_contents, have_same_file_contents, prompt_yn
from install_config import settings


def can_update(src: Src, dest: Dest):
    """
    If dest does not exist, or if src and dest are different
    """
    if not dest.exists():
        return True

    if isinstance(src, GitRepo):
        status = git_status(dest)
        if not status:
            return prompt_yn(f"{dest} has untracked content. Overwrite? (y/n) ")
        if not status.synced_with_remote():
            print(status)
            return prompt_yn(f"{dest} has unstaged changes. Overwrite? (y/n) ")
        return False # TODO: May want to prompt anyways since there may be ignored files we would like to keep
    elif isinstance(src, Path):
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
        
        if pair.dest.is_dir():
            rmtree(pair.dest)
        elif pair.dest.is_file():
            pair.dest.unlink()
        elif pair.dest.exists():
            raise NotImplementedError(f"Unhandled file type at {pair.dest}")
            
        if isinstance(pair.src, GitRepo):
            completed_process = run(["git", "clone", pair.src, pair.dest])
            print(completed_process.returncode)
        elif isinstance(pair.src, Path):
            if pair.src.is_file():
                copy(pair.src, pair.dest)
            elif pair.src.is_dir():
                copytree(pair.src, pair.dest)
            else:
                raise NotImplementedError(f"Unhandled file type at {pair.src}")
        else:
            raise NotImplementedError(f"Unreachable: {type(pair.src)}")
            
        if pair.make_executable and pair.dest.is_file():
            pair.dest.chmod(755)
    except Exception as e:
        eprint(f"Error processing pair: {e}", red=True)
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
        print(f"{ANSI_UNDERLINE}Running {setting.name}{ANSI_CLEAR_FORMATTING}")
        run_callback = False
        for pair in setting.src_dest_pairs:
            print(f"{pair.src} -> {pair.dest}")
            match process_pair(pair):
                case Status.PASSED:
                    passed.append(setting)
                    run_callback = True
                case Status.SKIPPED:
                    skipped.append(setting)
                case Status.FAILED:
                    failed.append(setting)
        if run_callback and setting.callback:
            print("Running callback.")
            error_msg = setting.callback(setting)
            if error_msg:
                eprint(error_msg, red=True)
                continue
    for each_passed in passed:
        if each_passed.final_message:
            print(f"{each_passed.name}: {each_passed.final_message}")