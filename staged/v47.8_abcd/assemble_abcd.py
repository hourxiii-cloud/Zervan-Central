#!/usr/bin/env python3
"""Reassemble and verify the four Zervan v47.8 GitHub upload job ZIPs."""
import hashlib,json,sys,zipfile,os
from pathlib import Path
from tempfile import NamedTemporaryFile
root=Path(sys.argv[1] if len(sys.argv)>1 else '.')
# Obtain the manifest/assembler from extracted Job A. The user supplies the jobs folder.
manifest_path=root/'ASSEMBLY_MANIFEST.json'
if not manifest_path.exists(): raise SystemExit('Missing ASSEMBLY_MANIFEST.json; extract Job A into the jobs folder first.')
m=json.loads(manifest_path.read_text())
target=root/m['final_archive']
with NamedTemporaryFile(dir=root,delete=False) as f: tmp=Path(f.name)
try:
 with tmp.open('wb') as out:
  for part in m['parts']:
   zpath=root/part['archive']
   if not zpath.is_file(): raise SystemExit(f"Missing ordered upload job {part['job']}: {zpath.name}")
   with zipfile.ZipFile(zpath) as z:
    assert z.testzip() is None, f"ZIP CRC failure: {zpath.name}"
    payload=z.read(part['payload_member'])
    meta=json.loads(z.read('PART.json'))
   assert meta['job']==part['job'] and meta['order']==part['order']
   assert len(payload)==part['bytes'] and hashlib.sha256(payload).hexdigest()==part['sha256'], f"Part {part['job']} integrity failure"
   out.write(payload)
 data=tmp.read_bytes()
 assert len(data)==m['final_bytes'], 'assembled size mismatch'
 assert hashlib.sha256(data).hexdigest()==m['final_sha256'], 'assembled SHA-256 mismatch'
 assert hashlib.sha512(data).hexdigest()==m['final_sha512'], 'assembled SHA-512 mismatch'
 with zipfile.ZipFile(tmp) as z: assert z.testzip() is None, 'assembled freeze ZIP CRC failure'
 os.replace(tmp,target)
 print(f"PASS: A→B→C→D assembled and verified {target.name} ({target.stat().st_size} bytes)")
 print(f"SHA-256: {m['final_sha256']}")
finally:
 if tmp.exists(): tmp.unlink()
