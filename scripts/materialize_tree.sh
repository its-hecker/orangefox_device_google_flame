#!/usr/bin/env bash
# Seed an empty Flame repository without flattening the Coral commit history.
set -euo pipefail
base=f67f624c0b94213f4447f8ab6039c80de9b82a21
[[ ${GITHUB_REPOSITORY:-} = its-hecker/orangefox_device_google_flame ]] || {
    echo 'This importer is restricted to the Flame repository' >&2
    exit 1
}
if [[ -f flame/BoardConfig.mk ]]; then
    sha=$(git rev-parse HEAD)
else
    seed=$(git rev-parse HEAD)
    branch=${GITHUB_REF_NAME:?Missing branch name}
    [[ "$branch" = main || "$branch" = orangefox-flame ]]
    patch_file=$(mktemp "${RUNNER_TEMP:-/tmp}/flame-port.XXXXXX.patch")
    trap 'rm -f "$patch_file"' EXIT
    cp .bootstrap/flame.patch "$patch_file"
    git fetch --no-tags https://github.com/its-hecker/orangefox_device_google_coral.git "$base"
    [[ $(git rev-parse FETCH_HEAD) = "$base" ]]
    git checkout --detach "$base"
    git apply --index --check "$patch_file"
    git apply --index "$patch_file"
    git config user.name 'github-actions[bot]'
    git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
    tree=$(git write-tree)
    sha=$(git commit-tree "$tree" -p "$base" -p "$seed" <<'MESSAGE'
Port the tested Coral OrangeFox fixes to the Flame TWRP target

Preserve the pinned Coral history and isolate the Pixel 4 target, kernel
checkpoint, runtime validation and build artifacts in the Flame repository.
Flame hardware validation is pending.
MESSAGE
)
    git checkout -B "$branch" "$sha"
    git push origin "HEAD:refs/heads/$branch"
    # Populate the new repository's default branch too; never force an update.
    if [[ "$branch" != main ]]; then
        git push origin HEAD:refs/heads/main
    fi
fi
git merge-base --is-ancestor "$base" "$sha"
printf 'sha=%s\n' "$sha" >> "${GITHUB_OUTPUT:?Missing Actions output file}"
