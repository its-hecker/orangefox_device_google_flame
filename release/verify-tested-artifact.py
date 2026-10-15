#!/usr/bin/env python3
"""Verify the tested CI artifact without changing or rebuilding the recovery."""
import hashlib
import json
import pathlib
import struct
import sys

root = pathlib.Path(sys.argv[1])
source = '087074222fd0be43b5f32115e198f5fb2825ee14'
expected = '175a22f205257bf030a942bfe8559e3a4d7b7b886046d86890849d488e8435a9'
image = root / 'OrangeFox-unofficial-flame.img'
data = image.read_bytes()
assert len(data) == 67108864
assert data[:8] == b'ANDROID!'
assert struct.unpack_from('<I', data, 40)[0] == 2
assert hashlib.sha256(data).hexdigest() == expected
assert (root / 'SHA256SUMS').read_text().split() == [expected, image.name]
assert (root / 'device-tree-commit.txt').read_text().strip() == source
identity = json.loads((root / 'kernel-metadata.json').read_text())['identity']
assert identity['product'] == 'flame' and identity['device_commit'] == source
assert identity['sources']['kernel/google/msm-4.14'] == '9d2fb45d1fc6e11ac7e03e73c772b69ce158ea0a'
assert json.loads((root / 'port-provenance.json').read_text())['device'] == 'flame'
print('Exact tested Flame image and source identity verified:', expected)
