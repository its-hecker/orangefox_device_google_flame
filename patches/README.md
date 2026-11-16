# Recovery source patches

This Flame branch retains the Coral source patches unchanged. The host
slider harness also covers Flame's 1080x2280 aspect mismatch (96x96 loaded
handle versus 96x114 XML dimensions). `init.recovery.device.rc` is packaged
under the Flame target's name; installed-ROM properties, crypto startup and
Health startup are the same shared fixes. Coral device-test reports below
remain historical reference evidence.

`0001-fit-slider-handles-to-scaled-images.patch` applies to
`gui/slidervalue.cpp` in OrangeFox Recovery `fox_12.1`, tested at
`cbcc4f713dbef98d76d6d2cfd019b1ebfd9418e9`.

Coral's 1440x3040 screen scales the 1080x1920 theme by 4/3 horizontally and
19/12 vertically. The 96x96 handle SVG has `retainaspect`, so its loaded
surface is 128x128. The XML slider dimensions independently become 128x152.
The original renderer copies that larger rectangle without resizing, reading
past the image buffer. The Screen settings page and console both contain
these sliders, matching the pages opened before the three SIGSEGV/restart
events in the supplied logs. This makes the overread a plausible cause, but
those crashes have no backtrace confirming it. The tester subsequently
identified the phone as Flame, while the logs report Coral and 1440x3040;
the patch fixes the reproduced overread independently of that discrepancy.

The patch uses the loaded handle's dimensions for slider layout and the
selected normal/hover image's dimensions for each blit. Hover images remain
centered on the same track position. Sliders without images retain their XML
dimensions. The original source's copyright and GPL notices remain intact.

The build checks patch applicability before applying it, then compiles the
actual patched `SetRenderPos` and `Render` methods into a host harness. Image
buffers end at a protected memory page. Tests cover Coral's aspect mismatch,
uniform scaling, a wide screen, a larger hover image, a negative destination
coordinate, and an image-free slider. The unpatched Coral case reproduces
SIGSEGV; the patched cases pass. This test does not replace Android/device
testing.

`0002-read-system-properties-from-both-layouts.patch` applies to
`crypto/system/bin/prepdecrypt.sh` in TeamWin/android_device_qcom_twrp-common,
tested at `98506f7919102378c8d52ee7d6a94a867f1b4c55`. The Android 12.1 build
SDK selects `system/build.prop`, but newer system filesystems can put
`build.prop` at their root. The patch accepts either path after the temporary
read-only mount. If neither exists it uses the script's existing error cleanup
and signals `crypto.ready`, allowing startup to complete with a logged error.

Coral init separately enables the upstream `prepdecrypt.setpatch` override
before decryption services start, including temporary fastboot boots. The host
test runs the actual script with isolated property and mount substitutes,
verifies the OS/system/vendor values before `crypto.ready`, and verifies
cleanup. It does not exercise Keymaster, metadata keys or PIN decryption.

`0003-show-coral-maintainer-support.patch` updates the portrait About page to
show `Hecker (Maintainer)` with `Channel: t.me/pixel4seriesupdates` beneath it.
The build installs `theme/maintainer.png`, the maintainer's selected circular
cat avatar, in the existing 192x192 About image resource.
`OF_MAINTAINER := Hecker` in `twrp.mk` sets that name; the older
`FOX_MAINTAINER` environment variable does not set this About field. Image
validation checks the executable, packaged About XML and exact avatar bytes.

`0004-prepare-fresh-data-media.patch` prepares staging storage under
`/data/media` and `/sdcard` after recovery starts with freshly formatted
userdata or successfully formats it. It checks for a writable ext4 or f2fs
mount and refuses to initialize storage over an existing FBE layout. The host
test exercises the patched startup and Format Data paths.

`0005-match-boot-avb-os-version.patch` gives the boot AVB descriptor its own
OS version override. Flame declares Android 17 for the descriptor and boot
header, with a November 2026 header patch month and a 2022-10-05 firmware
patch. The recovery build SDK remains 32. The host test exercises the compiled
image validator against Make's footer arguments and real AVB descriptors.
