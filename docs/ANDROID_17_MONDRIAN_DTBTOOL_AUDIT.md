# P1 — Legacy PE Qualcomm dtbToolLineage vs AOSP17 DTB/DTBO packaging

Date: 2026-11-04. **Obsolete tool inventory, NOT an Android17 production integration.**

## Source ownership / explicit architectural distinction

- Historical PixelExperience-Reborn `system_tools_dtbtool` branch `seventeen`, revision `ffd4bcb0e07a135e9bb65b07e33f6c8f5f1c47b9` (last tool change 2020). Contains only `Android.bp`, `dtbtool.c` and `dtbtool.txt`. Its `cc_binary_host` is named `dtbToolLineage`, chosen explicitly to avoid conflicting with other older device dtbtool copies.
- **It is a PE supplementary build tool, NOT a replacement for an official AOSP17 `platform/system/tools/dtbtool` project.** That path is absent from the reviewed effective AOSP17 reference manifest.
- `dtbtool.c` writes legacy Qualcomm `QCDT` multi-DTB table images with `QCDT_VERSION 3` and legacy `qcom,msm-id`, `qcom,board-id`, `qcom,pmic-id` tags, with `--force-v2`/`--force-v3` and `O_TRUNC` for output. Its bundled `dtbtool.txt` documents old boot-image header slots for QCDT size/layout.
- **Modern AOSP17 uses a different table format and tools** for DTB/DTBO partition images in official `platform/system/libufdt`, which *is already selected* in staged manifest. Exact AOSP17 r1 `system/libufdt` tree: `4647c80f1cdb7269980158b72ab2d7f8e5d4e33f`. Official `utils/src/Android.bp` provides `mkdtimg` and `mkdtboimg` host tools. Source: https://android.googlesource.com/platform/system/libufdt/+/refs/tags/android-17.0.0_r1/utils/src/Android.bp .
- The Android DTB/DTBO table header starts with `0xd7b7ab1e` rather than old QCDT ASCII magic. A separate DTBO partition image must not be constructed with the old `QCDT` writer. See https://source.android.com/docs/core/architecture/dto/partitions .

## Device-specific requirement before deciding if old tool is needed

For independent PE-Reborn Android17 `device/xiaomi/mondrian` + `device/xiaomi/sm8450-common` product:
1. Inspect actual *official image and kernel layout* of mondrian: boot header version; `boot.img`, `vendor_boot.img`, `dtbo.img`, any distinct DTB partition; device-tree concatenation vs `dt_table_header` wrapping; page alignment and offsets. This must be based on verified board-specific evidence, not on Android17 defaults or old LineageOS product makefiles.
2. Determine the correct build-tool linkage in native BoardConfig, `MKDTIMG_DTBOS`, `BOARD_PREBUILT_DTBOIMAGE`/`BOARD_PREBUILT_DTBIMAGE` or kernel-generated images, and avoid conflicting simultaneous image sources.
3. For `mkdtimg`/`mkdtboimg`, validate each board id/revision/custom field, entry count, DT overlay applicability and `dtc` alignment; compare generated dump to known-good images. Record tool SHA, input digests and output bytes.
4. If an older QCDT payload is **actually required** for a separate, verified boot interface, isolate `dtbToolLineage` as host-only with its own build/fixture tests, explicit consumer and approved image type. Never substitute QCDT for modern DTBO table and never infer necessity from repository history alone.
5. Run boot/recovery/AVB, bootloader rollback, OTA and all board revisions on physical mondrian. Existing LF52406 LineageOS-derived trees are **hardware references only**.

## Status and decision

- [x] Exact old PE host-tool sources and QCDT magic/version identified.
- [x] Verified no archived `dtbtool` manifest project is selected; official AOSP17 `system/libufdt` is selected.
- [x] Official AOSP17 libufdt tag tree and `mkdtimg` / `mkdtboimg` Soong targets identified.
- [x] Host-only source integrity workflows added (historic QCDT + official AOSP17 libufdt tags).
- [ ] Compile and test official DTBO tools on synthetic DTB/DTBO fixtures with actual output headers; compare to board-specific known-good images.
- [ ] Verify boot image header/DTBO/VBMeta on independent PE-Reborn mondrian product.
- [ ] Android17 Soong image build, bootloader, recovery and physical hardware tests.

**Decision: do not activate `dtbToolLineage` in staged AOSP17. This PE-specific supplement is not a required Android17 port unless the independently created device product demonstrates a real QCDT consumer.**
