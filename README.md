# OrangeFox for Google Pixel 4 (flame)

Maintainer: **Hecker** ([its-hecker](https://github.com/its-hecker)).
Updates: [Pixel 4 Series Updates](https://t.me/pixel4seriesupdates).
Support: [Pixel 4 ROMs](https://t.me/Pixel4Roms).

[Builds and logs](https://github.com/its-hecker/orangefox_device_google_flame/actions/workflows/build.yml)

OrangeFox R12.0 / Android 12.1 recovery source for **Pixel 4 (flame)**. This
branch aligns the boot and Keymaster metadata with HeckerOS Android 17's
November 2026 update and carries forward the Coral storage fixes.
**Flame device testing of this build is pending.**

## Shared TWRP source

[TeamWin's official Flame page](https://twrp.me/google/googlepixel4.html) links to
[TeamWin/android_device_google_coral](https://github.com/TeamWin/android_device_google_coral),
the same common Floral tree used for Pixel 4 XL. It contains `twrp_flame.mk`,
`device-flame.mk` and `flame/BoardConfig.mk` alongside the Coral files.

Use this repository's **fix/november-asb-20261112** branch. See
[port/provenance.json](port/provenance.json) for the original Coral base and the
November update's reference commit.

The checkout path deliberately stays **device/google/coral**, because that is
the upstream common-tree path. The build product is **twrp_flame-eng**, the
bootloader board is **flame**, and output is **out/target/product/flame**.
The Flame board keeps its own 440-DPI setting and device overlays.

## Carried-over fixes

- Qualcomm Keymaster 4.0/default and Citadel 4.1/strongbox startup, with the
  missing QTI Gatekeeper implementation and recovery library checks.
- Installed-ROM version properties before crypto startup, including temporary
  fastboot boot, and support for both system build.prop layouts.
- Boot header and AVB descriptor report Android 17, with November system
  patch metadata and the 2022-10-05 boot and vendor firmware patch.
- Recovery storage becomes available on freshly formatted userdata. Existing
  Android FBE keys and PIN decryption follow their normal path.
- Normal-boot Health 2.1 startup for battery percentage and charging state.
- Slider handle rendering fix for Screen settings and console, plus host
  regression coverage for the original image-buffer overread.
- A/B recovery-as-boot configuration, dynamic-partition support, MTP/ADB,
  recovery repacking tools and compatible ROM ZIP installation support.
- Hecker maintainer label, selected cat avatar and corrected Telegram channel.
- Bounded build parallelism, swap, logs and verified kernel/DTB checkpoints.

Coral testing reported working PIN/data decryption, battery percentage and ROM
ZIP installation on Infinity Android 17. These are **Coral results**, and are
not recorded as successful Flame tests. The November Flame image must be tested
using [TESTING.md](TESTING.md).

## Build

Use **Actions → OrangeFox Flame → Run workflow**, selecting
`fix/november-asb-20261112`.
CI builds the pinned TeamWin Floral kernel first and saves a checkpoint; a
fresh runner verifies and packages that exact kernel and DTB bundle. If only
the recovery job fails, rerun the failed job to reuse the completed checkpoint.

For a local Linux build, install the dependencies listed in
`scripts/prepare_host.sh` and ensure `repo`, Java 11 and the listed Python
packages are available. From this checkout run:

```sh
bash scripts/build.sh /absolute/path/to/empty-build-directory
```

The script stages this common tree at `device/google/coral`, syncs its
additional dependencies and builds `twrp_flame-eng`. Use a fresh build directory.
The optional `kernel` and `recovery` stages share `kernel-checkpoint/`.

Output includes `OrangeFox-unofficial-flame.img`, `SHA256SUMS`, the Android
source manifest, the device-tree commit and kernel/port provenance. Image checks
require header v2, a maximum 64 MiB image, matching kernel/DTBs, Flame init,
the Flame product in the AVB fingerprint, matching boot metadata,
crypto/Health startup, the fresh-data storage fix and
the packaged maintainer, avatar and channel.

## Initial test

On a Pixel 4 with an unlocked bootloader, verify `fastboot getvar product`
reports **flame**, check `SHA256SUMS`, then temporarily boot:

```sh
fastboot boot OrangeFox-unofficial-flame.img
```

Follow [TESTING.md](TESTING.md) for PIN/data, screen, battery, USB and ROM ZIP
tests. After those checks pass, the recovery's **Flash current OrangeFox
recovery** option is the installation route carried over from Coral. Permanent
installation/repacking on Flame still needs verification with the installed
ROM kernel; the initial build does not distribute an installer ZIP.

`prepdecrypt` reads the installed ROM properties at runtime. The recovery
binaries retain their Android 12.1 security patch coverage.

Original TeamWin, OrangeFox and AOSP copyright and license notices are retained.
