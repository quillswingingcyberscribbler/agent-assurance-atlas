# Methodology and interpretation

Agent Assurance Atlas groups two workbooks around the governance of AI-enabled actions. They answer related questions at different levels: whether a defined system is sufficiently assessed, and how much autonomy a specific operational action can receive. Their outputs remain separate.

This document describes the shipped files. Formula findings and their proposed corrections are in [known issues](known-issues.md). The original workbooks have not been patched in this reviewed prerelease.

## LLM and agent security assessment

### Assessment boundary and applicability

The assessment covers the complete system, including the model and provider, prompts, retrieval and vector storage, tools, access, data flows, logging and operations. Nineteen scoping questions derive applicability for 68 controls across nine domains. Missing scope keeps controls in play. Capability-specific agent controls can apply even if the stated autonomy level is None: tools, local device access, memory and MCP/multi-agent capabilities have their own triggers.

An explicit override needs a reason. Removing an automatically applicable Blocker also requires review information. Changing criticality below its shipped baseline has separate review requirements. A control awaiting another department's work remains applicable.

### Scores and exposure

| Input | Shipped convention |
| --- | --- |
| Answer | Yes = 1; Partial = 0.5; No = 0. |
| Criticality weight | Blocker = 5; Major = 4; Moderate = 3; Minor = 2. |
| Likelihood and impact | Each uses an assessor-selected integer from 1 to 5, with scale descriptions on `Lookups`. |
| Residual per answered applicable control | Weight × likelihood × impact × (1 − answer score). |
| Unanswered exposure | Full exposure is counted separately rather than presenting the missing answer as assessed. |

The dashboard's weighted residual exposure is a control-gap prioritization index. It is not an estimated loss, annual probability or empirically calibrated risk measure. Likelihood and impact ship with generic values; replace them with reasoned values for the system.

Policy thresholds depend on the system's role. The shipped readiness minima are 70% for Assist, 75% for Steer and 85% for Intervene. The corresponding per-control residual thresholds are 100, 80 and 60. These are governance conventions in `Lookups!B21:C23`. The workbook checks numeric bounds and the intended ordering; missing or invalid shared settings hold completion.

### Decision gates

| Condition | Intended result |
| --- | --- |
| Missing/invalid scope, unanswered applicable controls, failed integrity checks, inconsistent or incomplete required MCP assessment | `INCOMPLETE`. |
| Applicable Blocker answered No; Blocker Partial in Production; required MCP NO-GO | `BLOCKED`, once completion permits the main verdict. Confirmed failures also need to remain visible during incomplete work. |
| Blocker Partial in Pilot / PoC; Major No; eligible accepted gate risk; missing evidence; insufficient readiness; high residual; required MCP conditional result | `CONDITIONAL APPROVAL` when no stronger condition applies. |
| Required assessment complete with no blocking or conditional condition | `APPROVABLE`. |

Status and response have different purposes. Marking a control Remediated does not clear its gate; the control must be retested and re-answered. A formal gate exemption requires Accepted Risk plus reference, approver and date. It is counted and prevents silent unconditional approval. Evidence must support each Yes or Partial response; a missing reference is a conditional issue, while an error-valued input holds integrity.

The accountable risk owner's sign-off remains a separate decision. The workbook can check that information is present and coherent; it cannot verify the evidence or authenticate the reviewer.

### Comparator and MCP checklists

The four-candidate comparator supports sourcing. The shipped weighted-fit cutoffs are 80% for Suitable and 60% for Conditionally suitable, subject to its gates and review checks. Applicable controls are shared with the assessment, but operational metadata is not intended to contaminate model sourcing. `Suitable` does not authorize deployment.

Justified comparator exclusions remain pending until their current set is reviewed. The reviewed-set field must contain a value snapshot; formula-linked snapshots are rejected. Changing a reason changes the set and requires review again. This is a current-state review binding, not an authenticated or append-only audit trail.

The MCP server and client sheets have 16 and 20 checkpoints respectively. Each side has an explicit Required switch, context, evidence and exclusion review. A required side's open mandatory checkpoint or a compliance rate below the shipped 80% minimum can produce NO-GO. The main scope and side switches must agree. See LLM-02 for the case where missing context hides a confirmed-failure headline while keeping the result incomplete.

## SOC autonomy map

### Unit of decision

Autonomy belongs to an **action within a process step**, not an entire use case. The six steps are Enrich, Triage, Contain, Eradicate, Recover and Notify. They describe evidence gathering, case classification, limiting spread, removing the cause, restoring operation and informing affected parties. Real workflows may branch or notify earlier; the map's first human gate assumes the displayed linear sequence.

| Level | Decision and execution |
| --- | --- |
| L0 Manual | A human investigates, decides and acts; the system records. |
| L1 Assisted | The system gathers evidence; a human decides and acts. |
| L2 AI-recommended | The system proposes; a human decides and executes. |
| L3 Human-approved | A human approves the prepared action; the system executes. |
| L4 Autonomous | The system acts within pre-approved guardrails; a human is informed and can intervene. |

L5 Self-improving is described in `Scales` but is not selectable in the map.

### Policy target

The policy matrix maps risk appetite, reversibility and blast radius to a level from 0 to 4. A use case may override the default appetite. Reversibility has four classes: No state change, Fully reversible, Reversible with effort and Irreversible. Classify a compound action by its least reversible element. Blast radius describes the consequence of a wrong action, rather than incident severity.

`Register!J` is the pure policy recommendation. A valid explicit choice supplies the target in `Register!O`; otherwise the policy recommendation supplies it. A cautious choice applies immediately. An above-policy target is visible even before an exception is approved, but the release calculation retains the policy ceiling until approval is recorded.

The `Critical assets (target)` view re-rates rows at High blast radius and limits the displayed target accordingly. It is a sensitivity view; it does not calculate permission to execute on critical assets today.

### Release candidate

For a complete row, the release candidate is the minimum allowed by the chosen target, policy exception state, confidence ceiling, readiness staging and human-signature guardrail.

| Constraint | Shipped behavior |
| --- | --- |
| Model confidence | For state-changing actions, High imposes no additional ceiling; Medium and Low cap at one or two levels below policy, with a floor at L1. Default adjustments are `0, -1, -2`. |
| Readiness not passed | Holds the release at or below the recorded current level, subject to other ceilings. |
| Readiness passed | State-changing actions can rise by one level from current; No state change actions can release fully within the remaining constraints. |
| Human-signature guardrail | State-changing actions that are Irreversible or have High blast radius never release above L3, including approved policy exceptions. |
| Missing required row input | No target or release candidate; row reads `Incomplete assessment`. |
| Invalid policy matrix | No computed release; configuration error is shown. |

The confidence adjustment is a governance rule, not a measured conversion from error rate to safe autonomy. The shipped default ordering behaves as intended. The configurable ordering defect SOC-01 must be corrected before arbitrary adjustment policies can be treated as validated.

`No state change` is deliberately exempt from the confidence ceiling and one-level staging. Classification therefore matters greatly. Ticket creation, sandbox execution or collection may have downstream effects in a particular environment; inspect those effects before applying this label. An unknown nonblank confidence label on a No state change row currently still receives the exemption, while a blank required confidence field holds completion. This should be made explicit in guidance or tightened in a future validation change.

The six readiness criteria cover signal/context quality, documented and tested rollback, evidence capture before action, outcome verification, cost within budget, and resilience/degraded operation. By default all six must be Yes. The optional reduced read-only gate requires either signal/cost/resilience or signal/cost; state-changing actions always require all six.

`Limited by` lists the binding constraints. When several constraints bind at the same level it can list more than one. The result is a release **candidate**. The organization's authorized owner still decides whether the action may run; the workbook assumes the underlying access and data uses are permitted.

## Evidence and traceability

SOC's prefilled actions, confidence and current levels are illustrative proposals. Replace them with the local baseline and evidence such as measured error rates, calibration results and tested recovery paths. Record approvals with a decision reference, owner, date, action version and review period. The Yes/No exception field alone cannot provide that provenance.

When using both tools, record a common use-case identifier and version in their accompanying records. Use LLM assessment findings to inform operational readiness and ratings. Do not average the scores or infer that approval in one sheet satisfies the other workbook's gates.

## Validation boundary

The [review](review.md) covers structure, fresh LibreOffice recalculation, a formula-interpreter baseline, 39 in-memory scenarios, 612 independent reference assertions and selected print inspection. It does not establish native Excel acceptance, legal compliance, empirical calibration or the truth of entered evidence. The recorded expected scenarios include known defects so they can be reproduced and later replaced with regression tests for a corrected release.
