#!/usr/bin/env python3
"""Reject mismatched device targets or drift in the inherited recovery fixes."""
import hashlib
import json
import pathlib
import re


def validate(root):
    provenance = json.loads((root / 'port/provenance.json').read_text())
    if provenance['device'] != 'flame' or provenance['lunch_target'] != 'twrp_flame-eng':
        raise ValueError('This branch must select the Flame recovery product')
    checks = {
        'twrp_flame.mk': (
            r'^PRODUCT_DEVICE\s*:=\s*flame\s*$',
            r'^PRODUCT_NAME\s*:=\s*twrp_flame\s*$',
            r'inherit-product, device/google/coral/device-flame\.mk',
        ),
        'device-flame.mk': (r'^PRODUCT_HARDWARE\s*:=\s*flame\s*$',),
        'flame/BoardConfig.mk': (
            r'^\s*TARGET_BOOTLOADER_BOARD_NAME\s*:=\s*flame\s*$',
            r'^\s*TARGET_SCREEN_DENSITY\s*:=\s*440\s*$',
            r'include device/google/coral/ci/prebuilt-kernel\.mk',
        ),
        'vendorsetup.sh': (
            r'^export FOX_BUILD_DEVICE=flame$',
            r'^export OF_DEFAULT_KEYMASTER_VERSION=4\.x$',
            r'^export FOX_AB_DEVICE=1$',
        ),
        'scripts/build.sh': (
            r'^lunch twrp_flame-eng$',
            r'^out=out/target/product/flame$',
        ),
        'scripts/validate_recovery_runtime.py': (r'init\.recovery\.flame\.rc',),
    }
    for name, patterns in checks.items():
        source = (root / name).read_text()
        for pattern in patterns:
            if not re.search(pattern, source, re.MULTILINE):
                raise ValueError(f'Device selection check failed: {name}: {pattern}')
    for name, expected in provenance['inherited_sha256'].items():
        actual = hashlib.sha256((root / name).read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError(f'Inherited Coral fix or shared firmware changed: {name}')
    workflows = {p.name for p in (root / '.github/workflows').glob('*.yml')}
    if workflows != {'build.yml'} or (root / 'release/latest.json').exists():
        raise ValueError('Stale Coral release publication configuration is present')
    print('Source checks passed: Flame target, checkpoint hook and inherited Coral fixes')


if __name__ == '__main__':
    validate(pathlib.Path(__file__).resolve().parent.parent)
