# Draft GitHub issues

These are prepared issue bodies for a maintainer to review and open. Copy the items you want to track into GitHub Issues; the issue tracker becomes authoritative once an item has been created there. Scope is the two original workbooks in reviewed prerelease `0.1.0-review.1`.

## 1. Enforce monotonic SOC confidence adjustments in every consuming calculation

**Suggested labels:** `bug`, `priority-high`, `workbook-soc`  
**Finding:** SOC-01

### Problem

`Scales!C43` accepts High/Medium/Low adjustments of `-2, -1, 0`. The state-changing action in `Register` row 7 releases at L2 when High and L3 when Low. Less confidence can therefore produce more autonomy under an accepted configuration. The shipped defaults `0, -1, -2` work as intended.

### Proposed scope

Add the intended `High >= Medium >= Low` ordering check to global and consumed confidence validity. `Register!K6:K185` currently consumes the individual `Scales!D39:D41` checks, so updating only a banner cannot fix the result. Keep the read-only exemption explicit. Resolve whether High must always equal zero and align editable policy with its prose.

### Acceptance criteria

- The default configuration continues to produce the same release candidates.
- Equal adjacent adjustments are either accepted consistently or rejected according to an explicitly documented policy.
- Both ordering inversions are rejected and cannot produce a more permissive release.
- Missing, text, fractional, positive and below-range adjustments cannot pass validation.
- With other inputs fixed, every state-changing test row is nonincreasing in release level as confidence decreases.
- Read-only policy exemption, gate staging, policy exceptions and human-signature ceilings retain their intended behavior.
- Native Excel and an independent recalculation reproduce the corrected results; the known-defect scenarios become regression assertions for the fix.

## 2. Refresh the eight LLM comparator caches in a versioned native Excel save

**Suggested labels:** `bug`, `release`, `workbook-llm`  
**Finding:** LLM-01

### Problem

The blank source caches 0 in `Model Comparator!G6:J6` and 1 in `G8:J8`. Fresh calculations produce 26 and 0 respectively. Cached-only previews and consumers can show misleading counts even though the comparator remains provisional and the assessment incomplete.

### Proposed scope

Perform a full recalculation in the supported Excel version, save and reopen the workbook. Retain source history and publish a versioned corrected file; avoid silently replacing the original bytes in this reviewed prerelease.

### Acceptance criteria

- All four candidate blocker counts are 26 and all four unjustified N/A counts are 0 in the blank template.
- Comparator remains `PROVISIONAL - invalid scope/config`; Dashboard remains `INCOMPLETE`.
- Reopening with a cached-value reader gives those values.
- Other formulas, validations, protection, groups and print settings are preserved and checked.
- Workbook hash and release notes identify the new artifact.

## 3. Show confirmed mandatory MCP failures alongside missing context

**Suggested labels:** `bug`, `usability`, `workbook-llm`  
**Finding:** LLM-02

### Problem

A required MCP server can have a confirmed mandatory failure in `D23` while missing locality makes `D25` incomplete. `Dashboard!H3` recognizes NO-GO verdict strings, so the summary omits its confirmed-blocking-issue suffix. The client path has the same structural risk. The main recommendation remains incomplete.

### Proposed scope

Use the explicit confirmed-failure counts of applicable required sides to drive the diagnostic flag. Keep context completeness, policy validity and final recommendation logic separate.

### Acceptance criteria

- Complete required server with mandatory failure: BLOCKED and failure clearly visible.
- Same failure plus missing context: INCOMPLETE with a confirmed-failure diagnostic.
- Equivalent client scenarios give equivalent results.
- Nonrequired sides do not create an unrelated deployment block.
- Invalid policy, input errors, evidence gaps and exclusion review continue to hold or qualify the decision as designed.

## 4. Define and verify the LLM operational print report

**Suggested labels:** `documentation`, `usability`, `workbook-llm`  
**Finding:** PRINT-01

### Problem

The current whole-workbook LibreOffice export is 44 pages. Dashboard explanation text is clipped, and migration staging adds placeholder pages. Native Excel interaction and printing have not been accepted.

### Proposed scope

Select a deliberate operational report set, adjust dashboard widths/wrapping/page setup and document the export procedure. Keep migration and history available in the workbook without including them in routine reports.

### Acceptance criteria

- Every selected page is readable at the intended paper size.
- Dashboard interpretation and sign-off areas are fully visible.
- Repeating headers work on multipage assessment/checklist outputs.
- Native Excel open, recalculate, save, reopen and PDF export are checked on the supported release.
- Documentation identifies the tested version and actual report page set; no historical page count is presented as current.

## 5. Clarify read-only classification and invalid-confidence behavior

**Suggested labels:** `documentation`, `policy-decision`, `workbook-soc`

### Problem

The broad statement that invalid confidence caps at L1 does not describe the explicit No state change exemption. A nonblank unknown confidence label can still release L4 on a read-only row. Some example actions, including ticket creation and sandbox detonation, may have consequential side effects in a connected workflow.

### Proposed scope

Choose whether unknown labels must fail validation on every row, independently of the confidence ceiling. Clarify the exception and qualify example actions by actual effects and recovery evidence. Add a structured evidence reference for reversibility/recovery if this is adopted as a policy enhancement.

### Acceptance criteria

- Blank, unknown and valid confidence labels have documented, tested behavior for both read-only and state-changing actions.
- Read-only examples state their assumptions about downstream effects.
- Any policy behavior change is explicit in release notes and does not appear as an incidental formula cleanup.

## 6. Complete release ownership and third-party license allocation

**Suggested labels:** `release`, `documentation`

### Problem

No overall workbook license grant is embedded. `AI Defense Matrix!A2` expressly identifies a framework by Lenny Zeltser and Sounil Yu licensed CC BY-SA 4.0. A project-wide license must preserve that attribution and any applicable terms for derived material.

### Proposed scope and acceptance

Confirm ownership and the intended license of original workbook, code, documentation and artwork components. Identify the framework-derived material and review the applicable allocation rather than assuming the entire workbook's ShareAlike scope is settled. Preserve the workbook notice and [third-party notice](../THIRD-PARTY-NOTICES.md), link the source and license, and state relevant modifications. Record the final decision in `LICENSE-STATUS.md` and the appropriate license files before representing the project as licensed for public reuse.

## Review Office publication metadata

**Problem:** Every supplied Office source contains a Microsoft Information Protection label record. The earlier package review did not give this portfolio-wide metadata finding a separate publication task.

**Change:** Review the Sensitivity setting and applicable policy in the intended Office applications. Decide whether public release copies retain or remove the label. Preserve original sources separately and update hashes and validation evidence if any artifact changes. Do not copy label or site identifiers into public explanatory documents.

**Acceptance:** `validation/publication-metadata.json` records the reviewer, date, decision, and evidence. `validation/release-status.json` changes `publication_metadata_reviewed` only after that decision. Any changed release artifact has a reviewed hash and passing repository checks.
