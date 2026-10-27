# Validation scope

Review date: 22 October 2026. Package: `0.1.0-review.1`. Source versions: LLM assessment v0.6.8 r4; SOC Autonomy Map v1.4.3.

## Three distinct checks

| Check | What it establishes | What it does not establish |
| --- | --- | --- |
| Package integrity | ZIP/XML structure, internal relationships, source hashes, local documentation links and saved Excel error cells | Fresh calculation or correct decision logic |
| Model and scenario checks | The specific arithmetic, reference calculations and recorded input scenarios in this project's review | Every possible input, valid evidence or real-world model calibration |
| Native application acceptance | Input editing, recalculation, save/reopen, dropdowns, charts and print behavior in the named Excel version | Not performed in native Microsoft Excel; remains a release task. |

Read the [full review](review.md) for exact counts, known defects, test methods and limitations. [release-status.json](../validation/release-status.json) records the current readiness status. Source checksums are in [manifest.json](../validation/manifest.json).

Run the portable package check with:

```bash
python3 tools/validate_repository.py
```

The GitHub Actions workflow is named Repository checks. It runs package integrity, the independent reference calculations, the source-formula scenarios, and exact comparisons with the checked-in evidence. A green workflow reproduces the recorded baseline, including documented defects; it does not verify every workbook decision.

The workflow pins `actions/checkout` to the [v6.1.0 source commit](https://github.com/actions/checkout/commit/d23441a48e516b6c34aea4fa41551a30e30af803), uses a read-only token, and does not publish a release. The local commands were executed during preparation. After import, the repository's Actions tab is the authoritative record of hosted runs.

## Native Excel release acceptance

After correcting the documented issues, use the [native Excel acceptance record](../validation/native-excel-acceptance.md) to capture the Excel build and platform, disposable working-copy identity, normal and boundary scenarios, and save/close/reopen results. Check affected output cells, retained formulas and dropdowns, charts and print views. Confirm source changes against a cell-level change list. Keep a separate untouched source baseline for provenance.

The publication-metadata review is complete. Current public-copy identities and previous source hashes are recorded in [manifest.json](../validation/manifest.json) and [publication-metadata.json](../validation/publication-metadata.json). The LLM public copy was cleaned directly at OOXML level to preserve its sheet-protection configurations; the SOC copy was cleaned and reopened in Microsoft Excel. Full native Excel acceptance remains a separate release requirement.
