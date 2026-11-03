#!/usr/bin/env bash
# Print the path to the production Blender executable on a Linux x86-64 host.
set -euo pipefail

version=5.2.3
if command -v blender >/dev/null && [[ "$(blender --version | sed -n '1p')" == "Blender $version" ]]; then
    command -v blender
    exit 0
fi
if [[ "$(uname -s)/$(uname -m)" != Linux/x86_64 ]]; then
    echo "Install Blender $version for your operating system." >&2
    exit 1
fi
root=$(cd "$(dirname "$0")/.." && pwd)
tools_dir="$root/build/tools"
release="blender-$version-linux-x64"
if [[ ! -x "$tools_dir/$release/blender" ]]; then
    mkdir -p "$tools_dir"
    stage=$(mktemp -d "$tools_dir/download.XXXXXXXX")
    trap 'rm -rf "$stage"' EXIT
    base=https://download.blender.org/release/Blender5.2
    cd "$stage"
    curl --proto '=https' --fail --location --silent --show-error --retry 2 "$base/$release.tar.xz" -o "$release.tar.xz"
    curl --proto '=https' --fail --location --silent --show-error --retry 2 "$base/blender-$version.sha256" -o checksums
    sha256sum --check --ignore-missing --strict checksums >&2
    tar -xf "$release.tar.xz"
    mv "$release" "$tools_dir/"
fi
printf '%s\n' "$tools_dir/$release/blender"
