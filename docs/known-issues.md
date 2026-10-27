# Known issues

Applies to `LLM_Agent_Security_Assessment_v0_6_8_r4.xlsx` and `SOC-Autonomy-Map-v1.4.3.xlsx` in prerelease `0.1.0-review.1`. The source workbooks are preserved unchanged. The scenarios below are reproducible through the optional read-only harness; native Excel verification remains pending.

| ID | Priority and scope | Current guidance |
| --- | --- | --- |
| SOC-01 | Blocker for claiming arbitrary confidence-policy customization is validated | Retain the default High/Medium/Low adjustments `0, -1, -2`. |
| LLM-01 | Refresh before a final workbook release | Fully recalculate, save and reopen a working copy before interpreting summaries. |
| LLM-02 | Diagnostic clarity | Review mandatory failure counts alongside incomplete MCP headlines. |
| PRINT-01 | Publication layout | Export selected operational sheets and inspect the pages. |

## SOC-01 — Confidence configuration can reward lower confidence

**Affected cells:** `Scales!C39:C43`, `Scales!D39:D41`, and consuming `Register!K6:K185`.

The global configuration check accepts three integers from −4 through 0 without checking their order. Individual checks validate each adjustment separately. A valid-looking configuration can therefore make Low confidence less restrictive than High confidence, contradicting the workbook's stated evidence principle.

### Reproduction and observed result

1. On a disposable copy, set High, Medium and Low adjustments at `Scales!C39:C41` to `-2, -1, 0`.
2. Observe `Scales!C43 = OK`.
3. Keep the other values of `Register` row 7 unchanged. Set `H7` to High: confidence ceiling `L7 = 2` and release `T7 = 2`.
4. Set `H7` to Low: ceiling `L7 = 4` and release `T7 = 3` after the one-level readiness limit.

The supplied `0, -1, -2` defaults are correctly ordered and do not exhibit this defect.

### Proposed correction

Enforce `C39 >= C40 >= C41` in the shared configuration check and in the validity state consumed by each confidence calculation. Changing only the global banner is insufficient because `Register!K` uses the individual validity checks. Retain the intentional `No state change` policy exemption separately. Decide explicitly whether High must stay zero, since the current prose says High has no ceiling while the value is editable.

Regression cases should include default and equal adjacent values, both kinds of inversion, blank/text/fractional/positive/out-of-range inputs, and every confidence class in a state-changing row. Assert that reducing confidence never raises the release candidate with other inputs fixed. Include read-only cases separately so their exemption is deliberate.

## LLM-01 — Eight comparator caches need a full recalculation

**Affected cells:** `Model Comparator!G6:J6` and `G8:J8`.

| Cells | Cached source value, each cell | Fresh LibreOffice and reference result, each cell |
| --- | ---: | ---: |
| `G6:J6` | 0 | 26 |
| `G8:J8` | 1 | 0 |

The first group counts applicable Blocker answers that are No, Partial or blank. The second counts unjustified N/A entries. The source is blank, so the recalculated values are consistent with its formulas. All other 6,163 LLM formula results agree with the freshly recalculated copy.

The comparator still says `PROVISIONAL - invalid scope/config`, and the main assessment says `INCOMPLETE`; the stale counts do not yield a false approval in the supplied state. They can still mislead previews or consumers that read cached values only.

### Proposed correction

Open the file in the intended Excel version, perform a full recalculation, save, close and reopen. Verify these eight cells, the provisional comparator result and the incomplete dashboard. Keep formulas, validations, protection, grouping and print settings intact. Publish a versioned recalculated file only after checking the native result; this prerelease retains the uploaded bytes.

## LLM-02 — Confirmed MCP failure is less visible when context is incomplete

**Affected path:** `MCP Server Checklist!D23/D25` to `Dashboard!H3/B3/B21`; the client formula structure has the same pattern.

In the synthetic scenario with a required, fully assessed MCP server, a Non-compliant mandatory checkpoint at `E6` yields one confirmed failure in `D23`, a NO-GO checklist verdict and a BLOCKED dashboard. If locality `G3` is also blank, `D23` stays 1 but `D25` becomes `INCOMPLETE - assessment context missing or invalid`. The dashboard's confirmed-failure flag looks for the NO-GO string, so `B3` says only `INCOMPLETE` and omits the confirmed-blocking-issue suffix.

The recommendation stays closed as `INCOMPLETE`; the failure has not been approved or erased. It is visible in the checklist count but less clear in the summary.

### Proposed correction

Derive the dashboard's confirmed-failure flag directly from each applicable required checklist's confirmed mandatory-failure count. Keep the incomplete recommendation until required context is resolved. Test both server and client with simultaneous missing context and failure, as well as invalid policy, incomplete evidence and nonrequired-side cases.

## PRINT-01 — Whole-workbook LLM export needs layout work

The review's LibreOffice export produced 44 LLM pages and 17 SOC pages. The LLM Dashboard spans two pages, with some right-hand interpretation and decision text clipped on the first. Six empty `Old ...` staging sheets also create placeholder or blank pages when the entire workbook is exported.

The guide already identifies native Excel print acceptance as pending. Its approximately 20-page reference is explicitly for the older v0.6.3 render, not this release.

### Proposed correction

Define the intended operational report sheets, fit and wrap the dashboard deliberately, then inspect every output page in the intended Excel version. Ensure headers and sign-off fields remain readable. Exclude migration staging and history from routine reports. Until then, use selected-sheet export and a visual check for each report.

## Additional interpretation limits

The SOC `No state change` exemption currently allows a nonblank unrecognized confidence label to produce the read-only ceiling, while a blank required confidence field holds completion. Clarify the guide's broad statement about invalid ratings, or validate labels separately if all pasted unknown values should be rejected.

Examples such as ticket creation and sandbox detonation require local review of side effects before being labelled `No state change`. Neither the SOC exception switch nor LLM review snapshots authenticate the approver or create an append-only history. Record the external approval evidence and action/system version. These limitations are documented rather than silently changed in the source files.

See [draft issues](issues-to-open.md) for concrete proposed work and [review](review.md) for test evidence.

## PUB-01 — Office sensitivity-label metadata

A follow-up inspection on 26 October 2026 found a Microsoft Information Protection label record in every supplied Office source in this repository. The record contains label/site metadata; its presence alone does not establish confidentiality or unsuitability for publication. The source artifacts remain unchanged.

Before public distribution, review the Sensitivity setting and applicable policy in the intended Office applications. Decide deliberately whether release copies retain or remove the label and record the decision in the [publication-metadata record](../validation/publication-metadata.json). If an artifact changes, update its source hash and rerun the package and project-specific checks. Stable readiness also requires the completed [native Excel acceptance record](../validation/native-excel-acceptance.md).
