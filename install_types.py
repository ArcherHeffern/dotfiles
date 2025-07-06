
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import Callable, Iterable, Optional, TypeAlias


ErrorMsg: TypeAlias = str|None
@dataclass(frozen=True)
class GitRepo:
    url: str
SrcType: TypeAlias = Path | GitRepo
Src: TypeAlias = SrcType
Callback: TypeAlias = Callable[["Setting"],ErrorMsg]
Dest: TypeAlias = Path

class Platform(Enum):
    MACOS = "MacOS"
    WINDOWS = "Windows"
    LINUX = "Linux"
    UNKNOWN = "Unknown"

@dataclass
class Pair:
    src: Src
    dest: Dest
    make_executable: bool = False

    def __post_init__(self):
        if type(self.src) is Path:
            self.src = self.src.expanduser()
        self.dest = self.dest.expanduser()


@dataclass
class Setting:
    name: str
    src_dest_pairs: list[Pair]
    callback: Optional[Callback] = None
    platform: Optional[Iterable[Platform]] = None
    final_message: str|None = None