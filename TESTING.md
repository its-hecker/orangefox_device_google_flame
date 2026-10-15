# Pixel 4 (flame) validation

Current status: Flame hardware tests are pending. Source, build and ramdisk
checks do not establish device functionality. The Coral results remain in the
preserved Git history and the source pins are in `port/provenance.json`.

## First temporary boot

1. Save the exact boot image for the installed Flame ROM and back up important
   data. Confirm the unlocked device reports `flame` with `fastboot getvar product`.
2. Download the image artifact from the Flame build and verify `SHA256SUMS`.
3. Run `fastboot boot OrangeFox-unofficial-flame.img`. Pixel 4 uses recovery in
   boot; it has no separate recovery partition.
4. Record the build/run ID and ROM version. Confirm display and touch, including
   the screen edges. Open Screen settings, adjust brightness, open/close the
   console several times, reload the theme and leave recovery idle for five minutes.
5. Check ADB and MTP. Confirm the phone identifies as Flame:

   ```sh
   adb shell getprop ro.product.device
   adb shell getprop ro.product.model
   adb shell getprop ro.boot.hardware
   ```

## Decryption and internal storage

Use the phone's existing PIN/password on the recovery screen. Confirm existing
recognizable filenames under `/sdcard/Download` or `/data/media/0/Download`.
Read a small existing file over MTP or `adb pull`; capacity or an empty directory
alone does not prove decryption. Do not format data as a decryption workaround.

Check the version properties after startup:

```sh
adb shell getprop prepdecrypt.setpatch
adb shell getprop ro.build.version.release
adb shell getprop ro.build.version.security_patch
adb shell getprop ro.vendor.build.security_patch
```

The first property should be `true`; the others should match the installed
ROM. The carried-over Infinity defaults are Android 17, 2026-09-01 system patch
and 2022-10-05 vendor patch. Recovery's compiled SDK remains 32.

## Battery, USB and reboot targets

Compare recovery's battery percentage and charging icon against:

```sh
adb shell cat /sys/class/power_supply/battery/capacity
adb shell cat /sys/class/power_supply/battery/status
adb shell getprop init.svc.health-hal-2-1
```

Health should be running without a manual `start`. Connect/disconnect a charger,
then test ADB, MTP file copy, OTG, reboot to bootloader, reboot to Android and
reboot to fastbootd separately. For a copied file run `adb shell sync` and check
it remains accessible after reboot to Android.

## Installation tests

After basic boot, storage and USB checks pass, test a **Flame-compatible** ROM
ZIP using the ROM's documented procedure. Record installation success, active
slot and successful Android boot; test internal-storage install and ADB sideload
separately. Confirm backup/restore on a non-critical test before relying on it.

The persistent installation route inherited from Coral is to boot OrangeFox and
select **Flash current OrangeFox recovery**. Test this only after temporary
boot works, with the installed ROM's original boot image available. Repacking
can interact with the ROM kernel and root; neither persistent installation nor
A/B OTA persistence has been established on Flame by the source port.

| Check | Flame result |
|---|---|
| Boot, panel, touch, brightness | Pending |
| Settings, console, theme reload, idle stability | Pending |
| PIN/metadata/file decryption | Pending |
| Internal storage, MTP, ADB, OTG | Pending |
| Battery and charging updates | Pending |
| Reboot targets and fastbootd | Pending |
| ROM ZIP install and Android boot | Pending |
| ADB sideload | Pending |
| Backup/restore | Pending |
| Flash current recovery and reboot | Pending |

## Failure logs

Collect these from the same test session:

```sh
adb pull /tmp/recovery.log
adb logcat -d > logcat.txt
adb shell dmesg > dmesg.txt
adb pull /FFiles/temp/system_build_prop system-build.prop
adb pull /FFiles/temp/vendor_build_prop vendor-build.prop
```

Include the Flame image SHA256, Actions run, `device-tree-commit.txt`, the
installed ROM and `fastboot getvar product`. Property copies may be absent if
startup failed before reading the ROM; report that rather than changing keys.
