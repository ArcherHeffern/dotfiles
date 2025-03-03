#!/usr/bin/env bash

set -euo pipefail

CROSS_PLATFORM_PACKAGES=('sl' 'bat')
MACOS_PACKAGES=('fd' 'ggrep')
LINUX_PACKAGES=('fd-find' 'net-tools' 'zip')

if [[ "$(uname -s)" == "Darwin" ]]; then
	# TODO: Check if brew is installed and install if not
	brew install "${CROSS_PLATFORM_PACKAGES[@]}"
	brew install "${MACOS_PACKAGES[@]}"
else
	sudo apt-get update -y && sudo apt-get upgrade -y
	sudo apt install "${CROSS_PLATFORM_PACKAGES[@]}" -y
	sudo apt install "${LINUX_PACKAGES[@]}" -y
fi
