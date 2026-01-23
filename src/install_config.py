from os import mkdir
from pathlib import Path
from shutil import copy
from subprocess import run
from src.install_types import ErrorMsg, GitRepo, MoveFile, Setting, Platform
from src.install_utils import get_effective_user_id, exists_on_path


def create_bunnylol_daemon(_: Setting) -> ErrorMsg:
    # Is rustc downloaded
    if not exists_on_path("cargo"):
        return "Count not find cargo in PATH"

    # Compile bunnylol
    run(
        [
            "cargo",
            "install",
            "--path",
            ".",
            "--features",
            "server",
            "--no-default-features",
        ],
        cwd="./bunnylol.rs",
    )

    # Copy bunnylol to destination
    dest = Path("/usr/local/bin/bunnylol")
    if dest.is_file():
        dest.unlink()
    elif dest.exists():
        return f"{dest} exists and isn't a file"
    copy("./bunnylol.rs/target/release/bunnylol", dest)

    bunnylol_job_path = Path("~/Library/LaunchAgents/archer.bunnylol.daemon.plist")
    run_launch_agent(bunnylol_job_path)


def start_update_homebrew_cron_job(_: Setting) -> ErrorMsg:
    homebrew_job_path = Path("~/Library/LaunchAgents/archer.homebrew.update.plist")
    return run_launch_agent(homebrew_job_path)


def run_launch_agent(p: Path) -> ErrorMsg:
    p = p.expanduser()

    # Validate Config
    if run(["plutil", "-lint"]).returncode != 0:
        return f"{p} is an invalid config"

    # Turn agent off if it's on
    effective_user_id = get_effective_user_id()
    if effective_user_id is None:
        return "Failed to get effective user id"
    run(
        [
            "launchctl",
            "bootout",
            f"gui/{effective_user_id}",
            str(p.expanduser()),
        ]
    )  # Don't check if success

    # Run agent
    if (
        run(
            [
                "launchctl",
                "bootstrap",
                f"gui/{effective_user_id}",
                str(p.expanduser()),
            ]
        ).returncode
        != 0
    ):
        return "Failed to bootstrap."


def create_user_local_bin(_: Setting):
    f = Path("/usr/local/bin/").expanduser()
    if f.exists():
        return
    mkdir(f, mode=777)


settings: list[Setting] = [
    Setting(
        "Create /usr/local/bin",
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
        create_bunnylol_daemon,
        [Platform.MACOS],
    ),
]
