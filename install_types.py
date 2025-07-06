
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