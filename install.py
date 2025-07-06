from typing import Callable, Iterable, TypeAlias, Optional
from subprocess import run
from pathlib import Path
from platform import system
from dataclasses import dataclass
from enum import Enum, auto

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


ErrorMsg: TypeAlias = str|None
@dataclass(frozen=True)
class GitRepo:
    url: str
SrcType: TypeAlias = Path | GitRepo
Src: TypeAlias = SrcType
Callback: TypeAlias = Callable[["Setting"],ErrorMsg]
Dest: TypeAlias = Path

class Platform(Enum):
    MACOS = auto()
    WINDOWS = auto()
    LINUX = auto()
    UNKNOWN = auto()

@dataclass
class Pair:
    src: Src
    dest: Dest
    make_executable: bool = False


@dataclass
class Setting:
    name: str
    src_dest_pairs: Pair | list[Pair]
    callback: Optional[Callback] = None
    platform: Optional[Platform | Iterable[Platform]] = None
    final_message: str|None = None


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

def start_update_homebrew_cron_job(_: "Setting") -> ErrorMsg:
    effective_user_id = get_effective_user_id()
    if effective_user_id is None:
        return "Failed to get effective user id"
    run(["launchctl", "bootout", f"gui/{effective_user_id}", str(Path("~/Library/LaunchAgents/archer.homebrew.update.plist").expanduser())]) # Don't check if success
    if run(["launchctl", "bootstrap", f"gui/{effective_user_id}", str(Path("~/Library/LaunchAgents/archer.homebrew.update.plist").expanduser())]).returncode != 0:
        return "Failed to bootstrap."


settings: list[Setting] = [
    Setting("vimrc", [
        Pair(Path(".vimrc"), Path("~/")), 
        Pair(Path("colors"), Path("~.vim/")),
        ],
        final_message="Launch vim and run :PluginInstall"
    ),
    Setting(
        "bash",
        Pair(
            Path(".bash_profile"),
            Path("~/"),
        ),
        final_message="Source the new bash_profile using `source ~/.bash_profile` or restart your terminal."
    ),
    Setting(
        "tmux",
        Pair(
            Path(".tmux.conf"),
            Path("~/"),
        )
    ),
    Setting(
        "AScripts",
        Pair(
            GitRepo("https://github.com/archerheffern/AScripts"),
            Path("~/code/"),
        )
    ),
    Setting(
        "Update Homebrew Cron Job",
        [
            Pair(Path("scripts/update_homebrew.sh"), Path("~/Scripts/"), True),
            Pair(Path("scripts/archer.homebrew.update.plist"), Path("~/Library/LaunchAgents/archer.homebrew.update.plist")),
        ],
        start_update_homebrew_cron_job
    ),
]

if __name__ == '__main__':
    ...