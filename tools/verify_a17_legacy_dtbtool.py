#!/usr/bin/env python3
"""Legacy Qualcomm QCDT utility source-only audit. Not DTBO or boot validation."""
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]

def check(ok,msg):
    if not ok: raise AssertionError(msg)
    print("PASS historical DTB tool:",msg)

try:
    bp=(ROOT/"Android.bp").read_text()
    source=(ROOT/"dtbtool.c").read_text()
    notes=(ROOT/"dtbtool.txt").read_text()
    check("cc_binary_host" in bp and 'name : "dtbToolLineage"' in bp,
          "legacy Qualcomm utility is an optional host tool")
    check('#define QCDT_MAGIC     "QCDT"' in source
          and "#define QCDT_VERSION   3" in source,
          "legacy Qualcomm QCDT header/version, not modern DTBO table")
    for tag in ("qcom,msm-id", "qcom,board-id", "qcom,pmic-id"):
        check(tag in source, "legacy board selection tag "+tag)
    check("O_TRUNC" in source, "old tool overwrites output rather than appending")
    check("--force-v2" in source and "--force-v3" in source,
          "old QCDT formatting modes")
    check('MAGIC ("QCDT")' in notes, "old documentation describes QCDT output")
    check("boot image" in notes, "old boot-header assumptions documented")
    check(not (ROOT/"mkdtimg.c").exists() and not (ROOT/"mkdtboimg.py").exists(),
          "old tool does not provide AOSP17 mkdtimg or mkdtboimg")
    print("PASS historical source-only check; no modern DTBO image generated, no board verified.")
except (AssertionError,OSError) as e:
    print("FAIL:",e,file=sys.stderr)
    sys.exit(1)
