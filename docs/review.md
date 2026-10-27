# Agent Assurance Atlas — workbook review

Review date: 22 October 2026. The packaged workbooks were inspected without changing their contents. This report supports a reviewed prerelease; it is not a claim of native Microsoft Excel acceptance.

## Outcome

The two workbooks form a coherent project. The LLM assessment determines whether a defined AI system has adequate controls and evidence. The SOC map determines which actions may receive which degree of autonomy under a chosen policy and readiness state. They share an audience and governance problem, but their scores should remain separate.

Both workbooks open and recalculate in headless LibreOffice without formula errors. Their central decision paths behave as documented in the tested cases. The principal issue is a configurable SOC confidence-ordering gap: a permitted configuration can award more autonomy to lower confidence. The LLM file also contains eight stale cached comparator counts that correct themselves on full recalculation. Its approval recommendation remains incomplete in the supplied blank state.

## Inventory

| File | Worksheets | Formula cells | Content and initial state |
| --- | ---: | ---: | --- |
| `LLM_Agent_Security_Assessment_v0_6_8_r4.xlsx` | 18 | 6,171 | 19 scoping questions, 68 controls in nine domains, four-candidate comparator, 16 MCP server and 20 MCP client checkpoints, maturity draft, migration staging. Blank assessment begins `INCOMPLETE`. |
| `SOC-Autonomy-Map-v1.4.3.xlsx` | 7 | 2,887 | 20 illustrative use cases, six steps each, 120 populated action rows. Capacity prepared for 30 use cases / 180 action rows. Initial view is `Released today`. |

ZIP integrity and XML parsing passed. No VBA project, external workbook link, external data connection, embedded comment payload or hidden worksheet was found in either file. All worksheets are visible. The LLM workbook has 48 validation rules and nine protected working sheets. Intended example input cells are unlocked, and representative formula/baseline cells are locked. The SOC workbook has 14 validation rules and no sheet protection.

## What was verified

1. All source formula caches were checked for error values. Both files contain zero cached errors.
2. Disposable copies were recalculated and saved by headless LibreOffice. Both recalculated files contain zero formula errors. Source files remained unchanged.
3. Source and recalculated caches were compared. All 2,887 SOC formula results agree. The LLM has eight stale source values, described below; the other 6,163 agree.
4. A purpose-limited read-only interpreter evaluated the source formulas. Its baseline agrees with every recalculated formula value: 6,171 LLM and 2,887 SOC results, with no mismatches or unsupported formulas in the supplied state. That baseline agreement does not make it a general replacement for Excel.
5. Thirty-nine targeted input scenarios were evaluated through that interpreter. All produced the recorded expected behavior, including scenarios that expose the known limitations. These were in-memory scenarios, not native Excel UI tests.
6. A separate Python standard-library reference check independently reconciles five SOC outputs for each of the 120 populated action rows, the three headline distribution shares, four autonomy boundaries, and four LLM baseline checks. Its 612 assertions pass and it separately reports the known issue observations.
7. Both workbooks were exported to PDF using LibreOffice. The SOC map and LLM dashboard were visually inspected. The LLM print output needs attention; details follow.

No native Microsoft Excel interaction, Windows/Mac Excel print acceptance, browser Excel acceptance or Google Sheets compatibility was performed. Evidence quality, named reviewers' authority, model calibration and actual operational controls cannot be established by spreadsheet calculation checks.

## Confirmed findings and precise remediation

### SOC-01 — Confidence adjustments do not enforce their intended order

**Priority: correct before advertising arbitrary policy customization as validated.**

`Scales!C43` accepts any three integers in `[-4,0]`. It does not require the adjustment for High confidence to be at least the Medium adjustment, or Medium to be at least Low. `Scales!D39:D41` checks each entry separately. `Register!K6:K185` uses those individual checks, so a red global configuration banner alone would not resolve this defect.

Reproduction: set `Scales!C39:C41` to `-2, -1, 0`. The configuration status remains `OK`. With the other values of `Register` row 7 unchanged, High confidence gives a release candidate of L2 and Low confidence gives L3. This contradicts the guide's stated rule that less evidence must never produce more autonomy. The shipped `0, -1, -2` configuration is correctly ordered and does not exhibit the issue.

Recommended correction: add `C39>=C40` and `C40>=C41` to the shared configuration check. Make the individual validity checks or the consuming confidence calculation also enforce that shared validity. Preserve the explicit read-only exemption as a separate policy decision. Test default values, equal adjacent values, inverted values, out-of-range values and blanks. Whether High must stay exactly zero is a policy choice: the prose currently says High creates no ceiling, while the input is editable.

### LLM-01 — Eight comparator caches are stale

**Priority: refresh before a final workbook release.**

| Cells | Saved values | Fresh calculation |
| --- | ---: | ---: |
| `Model Comparator!G6:J6` | 0 in each cell | 26 in each cell |
| `Model Comparator!G8:J8` | 1 in each cell | 0 in each cell |

The first row counts applicable Blocker answers that are No, Partial or blank. A blank template has 26 such rows. The second row counts unjustified N/A entries; there are none in the blank template. Both formula definitions are consistent with the recalculated values. The comparator remains `PROVISIONAL - invalid scope/config` and the operational recommendation remains `INCOMPLETE`; there is no false approval from these caches.

Recommended correction: full recalculation in the intended Excel version, save, close and reopen, then verify these eight values. Preserve formulas and native workbook features. Until that is done, document that the file must be recalculated before interpreting its summaries.

### LLM-02 — Incomplete MCP context hides a confirmed-failure headline

**Priority: improve diagnostic clarity; the recommendation remains closed.**

When an applicable required MCP server checkpoint is Non-compliant, `MCP Server Checklist!D23` correctly counts one mandatory failure. With complete context the checklist returns `NO-GO` and `Dashboard!B21` returns `BLOCKED`.

If the same fixture also has a blank locality at `MCP Server Checklist!G3`, the checklist's `D25` first returns `INCOMPLETE - assessment context missing or invalid`. `Dashboard!H3` looks for a `NO-GO` verdict string, so the summary `B3` says only `INCOMPLETE`, without the otherwise available `confirmed blocking issue present` suffix. The count remains visible on the checklist. The equivalent client path has the same structural pattern.

Recommended correction: derive the headline's confirmed-mandatory-failure flag directly from the relevant required checklist's confirmed-failure count, while retaining the incomplete recommendation until required inputs are resolved. Test both server and client paths with simultaneous missing context and a mandatory failure.

### PRINT-01 — Full-workbook export is not a polished publication

The LibreOffice export produces 17 pages for SOC and 44 for the LLM workbook. The SOC overview is readable and includes the map, distribution table and chart. The LLM Dashboard spans pages 8–9; on the first page, right-hand decision-logic and interpretation text is clipped. The six empty `Old ...` migration worksheets also produce placeholder and blank pages in a whole-workbook export.

The LLM guide already says native print acceptance is pending. Its reference to an older approximately 20-page render is explicitly historical; it should not be presented as the current print length.

Recommended release guidance: share XLSX for interactive work, and export selected operational sheets for a report. Exclude migration placeholders and change history from routine reporting. A later print pass should fit the dashboard deliberately, wrap its explanatory text, and check both printed pages and the sign-off block. Do not distribute the audit PDFs as polished report templates.

## Behavioral results

| Scenario | Observed behavior |
| --- | --- |
| Blank LLM assessment | `INCOMPLETE`; 68 controls remain applicable until scope is declared. |
| Complete synthetic production scope, applicable answers Yes, evidence present | `APPROVABLE`; 36 applicable controls in this particular fixture. |
| Applicable Blocker Partial | `BLOCKED` in Production; `CONDITIONAL APPROVAL` in Pilot / PoC. |
| Blocker No with Status Remediated | Remains `BLOCKED`; status does not substitute for re-assessment. |
| Blocker No accepted with complete exemption reference, approver and date | Counted exemption; `CONDITIONAL APPROVAL`. |
| Missing exemption metadata, unreviewed Blocker de-scope, invalid likelihood, invalid scope or invalid thresholds | `INCOMPLETE`. |
| Yes/Partial without evidence | `CONDITIONAL APPROVAL`, with evidence count visible. |
| Tools, local access, memory and MCP with autonomy None | Relevant capability controls remain applicable. |
| Required MCP side complete | Checklist `GO`; operational fixture `APPROVABLE`. |
| Required MCP mandatory failure | `BLOCKED`; invalid protocol calendar date instead holds completion. |
| S19 No while a checklist is Required Yes | `INCOMPLETE`. |
| Complete comparator candidate | `Suitable`, meaning proceed to assessment rather than authorization. |
| Proposed comparator exclusion | `PENDING REVIEW`; approved matching value snapshot allows the reviewed result. |
| Changed exclusion reason or formula-linked snapshot | Returns to `PENDING REVIEW`. |
| Rejected comparator exclusion | `INCOMPLETE - re-answer rejected exclusions`. |
| Invalid shared comparator policy | `PROVISIONAL - invalid scope/config`. |
| Operational evidence error during model sourcing | Does not contaminate the separate comparator verdict. |
| Missing SOC action or current level | No target or release candidate; `Incomplete assessment`. |
| Broken SOC policy matrix | `Config error`, no release candidate. |
| SOC Low confidence with L4 policy | Tested state-changing action caps at L2. |
| Approved above-policy L4 choice on High blast radius | Non-waivable human-signature guardrail caps release at L3. |
| Read-only reduced gate `Signal + cost` | Releases Enrich to L4 in the five cases identified by the workbook guide. |

## Scope and method considerations for the public project

The LLM workbook's residual value is a weighted control-gap index. It is not an annual probability, monetary loss estimate or calibrated risk measure. The explicit README wording handles this distinction well. The comparator's security-fit score concerns model selection, not deployment authorization.

The SOC policy ratings, current levels and confidence are illustrative. They need replacement with a local baseline and supporting evidence. The guide correctly separates desired policy targets from release candidates, and correctly describes the critical-assets view as a target sensitivity rather than permission to operate on critical assets today.

SOC uses a deliberate confidence exemption for `No state change` steps. A nonblank unknown confidence label on such a row still receives the exemption and can produce L4, while a blank confidence label holds the row incomplete. This is consistent with the exemption in the formula, but the statement that any invalid rating caps at L1 needs to state that exception clearly. Validate labels independently if the intent is to reject pasted values on every row.

The `No state change` examples in `Scales!E24` include ticket creation and sandbox detonation. Whether these are safe to treat as read-only depends on their actual side effects and downstream integrations. Classify the concrete action and connected workflow. The reference to internal notification as fully reversible also needs contextual judgment, since a message cannot literally be unread. These are rating assumptions, not arithmetic defects.

The SOC `Exception approved` switch records Yes/No. It does not establish who approved, when, for which action version or for what duration. Use the Notes field and an external approval record for those facts. The guide already retains formal authorization with the Control Tower. The LLM reviewed-set snapshots similarly bind the current exclusion set, not reviewer authentication or an append-only history.

The two tools have no automatic data exchange. Record the same use-case identifier and version in both, then use assessment findings and evidence to inform SOC ratings. Do not average their scores or treat one workbook's positive result as sufficient to satisfy the other's criteria.

The SOC guide refers repeatedly to a briefing that was not included in this project input. The repository should explain the autonomy levels, six process steps, readiness criteria, assumptions and target/release distinction on its own. Those definitions already exist within `Scales` and can be summarized in documentation without depending on slide numbers.

## External reference spot-check

The LLM checklist's stated MCP `2026-07-28` baseline and deprecation statement for Roots, Sampling and Logging were checked against the official [release announcement](https://blog.modelcontextprotocol.io/posts/2026-07-28/) and [deprecated-features register](https://modelcontextprotocol.io/specification/2026-07-28/deprecated), accessed 22 October 2026. These sources support that specific statement. This review did not claim exhaustive coverage of the protocol, every framework mapping or each jurisdiction's legal obligations.

## Publication and licensing

Neither workbook embeds an overall software or documentation license grant. The LLM workbook’s `AI Defense Matrix!A2` contains a third-party attribution to Lenny Zeltser and Sounil Yu and identifies that framework as CC BY-SA 4.0; this is not a license grant for the workbook as a whole. See [license status](../LICENSE-STATUS.md). Their content contains no populated confidential assessment records, named customer systems, secrets or employer identifiers found in this inspection. Author names appear in document metadata. Framework and licensing references within assessment questions are subject matter, not a license for the workbook.

The LLM workbook is a genuine blank assessment. SOC is an example-filled model, which should be clearly labelled as such in the repository. No clean-start SOC variant has been silently created.

## Reproducing the recorded checks

Run the following from the repository root with Python 3.10 or later:

```sh
python tools/reference_checks.py > validation/reference-results.json
python -m pip install -r requirements-test.txt
python tools/scenario_eval.py --output validation/scenario-results.json
```

The reference check uses only the Python standard library. The optional scenario harness uses `openpyxl` to read formulas and tokenize expressions; it never saves workbooks. Both commands accept `--workbook-dir /path/to/workbooks`. The scenario harness fails with a nonzero exit status if a result differs from its recorded expectation. Expectations deliberately include the documented defects; passing them confirms reproducibility, not that those defects are fixed.

[Reference results](../validation/reference-results.json) contain 612 passing assertions and nine known-issue observations. [Scenario results](../validation/scenario-results.json) contain 39 cases. The [interpreter crosscheck](../validation/interpreter-crosscheck.json) records the comparison of all 9,058 source formulas against separately recalculated LibreOffice values. That crosscheck is a historical review record: running the scenario harness does not rerun LibreOffice or regenerate this record. Disposable recalculated copies and audit PDFs are not packaged.

## Publication preparation addendum — 26 October 2026

A subsequent repository-only inspection found Microsoft Information Protection label records in every supplied Office source in this repository. The identifiers are omitted from the [publication-metadata record](../validation/publication-metadata.json). Their presence alone is not a confidentiality determination. No source Office artifact was modified during this follow-up.

The GitHub workflow now reproduces the independent reference calculations and source-formula scenarios, then compares them with the recorded evidence. The [browser publishing guide](../PUBLISHING.md), [native Excel acceptance record](../validation/native-excel-acceptance.md), and release-evidence checks were added for publication preparation. These changes affect repository scaffolding and documentation; they do not change the functional findings or numerical/workbook baselines recorded above.
