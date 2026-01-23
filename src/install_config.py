from os import mkdir
from pathlib import Path
from subprocess import run
from src.install_types import ErrorMsg, GitRepo, MoveFile, Setting, Platform
from src.install_utils import get_effective_user_id


def start_bunnylol_daemon(_: Setting) -> ErrorMsg:
    # Compile bunnylol
    # Copy bunnylol to destination
    ...


def start_update_homebrew_cron_job(_: Setting) -> ErrorMsg:
    effective_user_id = get_effective_user_id()
    if effective_user_id is None:
        return "Failed to get effective user id"
    run(
        [
            "launchctl",
            "bootout",
            f"gui/{effective_user_id}",
            str(
                Path("~/Library/LaunchAgents/archer.homebrew.update.plist").expanduser()
            ),
        ]
    )  # Don't check if success
    if (
        run(
            [
                "launchctl",
                "bootstrap",
                f"gui/{effective_user_id}",
                str(
                    Path(
                        "~/Library/LaunchAgents/archer.homebrew.update.plist"
                    ).expanduser()
                ),
            ]
        ).returncode
        != 0
    ):
        return "Failed to bootstrap."


def create_user_local_bin(_: Setting):
    f = Path("~/usr/local/bin/").expanduser()
    if f.exists():
        return
    mkdir(f)


settings: list[Setting] = [
    Setting(
        "Create usr/local/bin",
        [],
        create_user_local_bin,
    ),
    Setting(
        "vimrc",
        [
            MoveFile(Path("configs/.vimrc"), Path("~/.vimrc")),
            MoveFile(Path("colors"), Path("~/.vim/colors/")),
        ],
        final_message="Launch vim and run :PluginInstall",
    ),
    Setting(
        "zsh and bash",
        [
            MoveFile(
                Path("configs/.archer_profile"),
                Path("~/.archer_profile"),
            ),
            MoveFile(
                Path("configs/.zprofile"),
                Path("~/.zprofile"),
            ),
            MoveFile(
                Path("configs/.bash_profile"),
                Path("~/.bash_profile"),
            ),
        ],
        final_message="restart your terminal to run .profile files.",
    ),
    Setting(
        "tmux",
        [
            MoveFile(
                Path("configs/.tmux.conf"),
                Path("~/.tmux.conf"),
            )
        ],
    ),
    Setting(
        "AScripts",
        [
            MoveFile(
                GitRepo("https://github.com/archerheffern/AScripts"),
                Path("~/code/AScripts/"),
            )
        ],
    ),
    Setting(
        "Intellij Idea Vim Config",
        [
            MoveFile(
                Path("configs/.ideavimrc"),
                Path("~/.ideavimrc"),
            )
        ],
    ),
    Setting(
        "Update Homebrew Cron Job",
        [
            MoveFile(
                Path("scripts/update_homebrew.sh"),
                Path("~/Scripts/update_homebrew.sh"),
                True,
            ),
            MoveFile(
                Path("scripts/archer.homebrew.update.plist"),
                Path("~/Library/LaunchAgents/archer.homebrew.update.plist"),
            ),
        ],
        start_update_homebrew_cron_job,
        [Platform.MACOS],
    ),
    Setting(
        "Run bunnylol Daemon",
        [
            MoveFile(
                Path("scripts/archer.bunnylol.daemon.plist"),
                Path("~/Library/LaunchAgents/archer.bunnylol.daemon.plist"),
            ),
        ],
        start_bunnylol_daemon,
        [Platform.MACOS],
    ),
]
