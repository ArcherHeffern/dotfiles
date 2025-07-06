from pathlib import Path
from subprocess import run
from install_types import ErrorMsg, GitRepo, Pair, Setting, Platform
from install_utils import get_effective_user_id


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


settings: list[Setting] = [
    Setting(
        "vimrc",
        [
            Pair(Path(".vimrc"), Path("~/.vimrc")),
            Pair(Path("colors"), Path("~/.vim/colors/")),
        ],
        final_message="Launch vim and run :PluginInstall",
    ),
    Setting(
        "bash",
        [
            Pair(
                Path(".bash_profile"),
                Path("~/.bash_profile"),
            )
        ],
        final_message="Source the new bash_profile using `source ~/.bash_profile` or restart your terminal.",
    ),
    Setting(
        "tmux",
        [
            Pair(
                Path(".tmux.conf"),
                Path("~/.tmux.conf"),
            )
        ],
    ),
    Setting(
        "AScripts",
        [
            Pair(
                GitRepo("https://github.com/archerheffern/AScripts"),
                Path("~/code/AScripts/"),
            )
        ],
    ),
    Setting(
        "Update Homebrew Cron Job",
        [
            Pair(
                Path("scripts/update_homebrew.sh"),
                Path("~/Scripts/update_homebrew.sh"),
                True,
            ),
            Pair(
                Path("scripts/archer.homebrew.update.plist"),
                Path("~/Library/LaunchAgents/archer.homebrew.update.plist"),
            ),
        ],
        start_update_homebrew_cron_job,
        [Platform.MACOS],
    ),
]
