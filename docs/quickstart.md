# Quick start

This prerelease contains two different workflows. Work from a copy so that the original version remains available for comparison. The LLM workbook starts blank; the SOC workbook contains illustrative examples.

## Assess an LLM or agent system

Open [LLM_Agent_Security_Assessment_v0_6_8_r4.xlsx](../workbooks/LLM_Agent_Security_Assessment_v0_6_8_r4.xlsx) and read `README & Logic`. Assess the complete integration: provider and model, prompts, retrieval, data flows, tools, identities, logging and operations.

1. **Declare the assessment.** In `Scoping`, enter the system/use-case name, assessor or accountable owner, date and assessment version. Complete all 19 profile questions using the offered values. Unanswered questions keep controls applicable; they do not narrow the assessment.
2. **Answer applicable controls.** In `Assessment Matrix`, use Yes, Partial or No. Every Yes or Partial needs an evidence reference. Adjust the generic likelihood and impact values to the system. Expand the grouped columns when you need scoring, remediation or exemption details.
3. **Explain scope changes.** Use the Override and Notes fields for a deliberate applicability variation. An automatically applicable Blocker requires the documented review information before it can be removed. Another team's ownership is a reason to obtain its review, not to remove the control.
4. **Complete required MCP sides.** If S19 is Yes, declare both server and client `Required` switches explicitly. Document why an unneeded side is excluded. Fill the context fields, assess every applicable checkpoint and record evidence. Required checklists and S19 must agree. Check the mandatory-failure count even if the checklist headline is incomplete; [LLM-02](known-issues.md#llm-02--confirmed-mcp-failure-is-less-visible-when-context-is-incomplete) describes a diagnostic limitation.
5. **Resolve the dashboard.** Correct incomplete inputs and integrity flags, then review open gates, evidence gaps and residual exposure. Setting Status to Remediated does not close a failed control: retest it and update the response. Accepted Risk needs a reference, approver and date, and qualifying gate exemptions remain counted.
6. **Recalculate and record the decision.** Perform a full recalculation in the Excel version you use, then save, close and reopen your working copy. Check `Model Comparator!G6:J6` and `G8:J8` as described in [LLM-01](known-issues.md#llm-01--eight-comparator-caches-need-a-full-recalculation). Have the accountable risk owner record the final decision and date in the dashboard sign-off area.

The dashboard recommendation is `INCOMPLETE`, `BLOCKED`, `CONDITIONAL APPROVAL` or `APPROVABLE`. `APPROVABLE` means ready for accountable review and authorization; it is not the signed authorization itself.

### Compare models before selection

Use `Model Comparator` for up to four candidates. Its applicable controls follow the declared scope. An N/A answer needs a per-model explanation; reviewed exclusions require the on-sheet decision, reviewer, date and current reviewed-set snapshot. Paste the snapshot **as a value**. A formula link to the current set is not a review record, and changing an exclusion requires review again.

`Suitable` is a sourcing result. Carry the selected model into the complete operational assessment, including controls and evidence that depend on its deployment.

### Carry data from an older version

The optional `Migration` sheet documents a values-only workflow using the six `Old ...` staging sheets. Follow that workflow on a copy. Check its status lines before copying any blue output block to the named destination. Formula cells, criticality baselines and template-owned policy are not general-purpose paste targets.

## Map SOC autonomy

Open [SOC-Autonomy-Map-v1.4.3.xlsx](../workbooks/SOC-Autonomy-Map-v1.4.3.xlsx). Read `Guide` and `Scales` before changing the examples. The repository's [methodology](methodology.md) supplies the definitions needed to use the workbook without the briefing mentioned in its guide.

1. **Choose the policy context.** Set the default risk appetite in `Autonomy map!C4`. Review the `Policy` matrix. Keep confidence adjustments at their shipped `0, -1, -2` values until [SOC-01](known-issues.md#soc-01--confidence-configuration-can-reward-lower-confidence) is corrected; arbitrary confidence customization has not passed acceptance.
2. **Identify the use cases.** In `Use cases`, replace example names and domains and set any use-case-specific appetite. Keep IDs unique and stable across `Use cases`, `Register` and `Readiness gate`.
3. **Assess each action.** For each of the six steps, enter the actual action, reversibility, blast radius, model confidence and current autonomy level. A missing required field holds the row incomplete. Rate the actual connected workflow, including indirect side effects, rather than treating the examples as measured facts.
4. **Record choices and exceptions.** A lower chosen level applies immediately. An above-policy choice stays visible as a target but needs `Exception approved = Yes` before that policy exception can contribute to release. Record the owner, date, action version, rationale and evidence in Notes or an external decision record; the Yes/No switch alone is not approval provenance.
5. **Complete readiness.** Answer the six readiness criteria for every use case. The default requires all six explicit Yes answers. A deliberately selected reduced gate applies only to `No state change` steps; state-changing actions still require all six.
6. **Compare the three views.** `Standard assets (target)` shows the chosen policy target. `Critical assets (target)` treats every row as High blast radius. `Released today` shows the release candidate after constraints. Review `Limited by`, incomplete rows, current-above-permitted flags and exceptions with the operational owner.

The 20 supplied use cases are examples, with prepared space up to 30 use cases. For UC21–UC30, complete the corresponding six register rows and readiness row. Beyond that capacity, copying rows alone is insufficient: every named range and bound across the related sheets would need a separate change and review.

## Use both tools together

Record the same use-case identifier, system version and review date in both workbooks or their accompanying decision records. Use security findings and measured evidence to inform the SOC ratings and readiness answers. Keep the assessment's weighted exposure, the comparator's fit score and the SOC autonomy levels separate; no conversion between them is defined.

## Share a report

Share the XLSX for interactive work. For a PDF, select the operational sheets you intend to present and inspect every resulting page. Whole-workbook export includes migration placeholders and history; the reviewed LLM dashboard also has a print-layout limitation. Native Excel interaction and print acceptance remain outstanding. See the [review](review.md) for the checks that have actually been completed.
