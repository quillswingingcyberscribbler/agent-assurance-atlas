# Changelog

## Licensing and public-copy preparation — 2026-10-27

- Selected CC BY-SA 4.0 for all original material in Agent Assurance Atlas. Added the operative project `LICENSE` and updated the license status, citation metadata, third-party notice, README and issue drafts. AI Defense Matrix attribution and ShareAlike terms are preserved; `MIT.proposed.txt` remains historical only.
- Retained the visible Public sensitivity labels and removed document properties, `lastModifiedBy` and absolute local or SharePoint paths from both public workbooks.
- Cleaned the LLM workbook directly at OOXML level to preserve all 6,171 formulas, saved cell values and all nine sheet-protection configurations. Cleaned and reopened the SOC workbook in Microsoft Excel; all 2,887 formulas and saved cell values match the original source.
- New LLM SHA-256: `62e48e500ccbe75314076314d9e647fca8981c3d196d56e213962b20d36648a0`. New SOC SHA-256: `63a700e46346a6b9875cccce2b4b1a48df4f901f51877c9da604511de5cbe8c4`.
- Reference and scenario outputs reproduce the recorded baselines exactly, including documented defects. No formula errors were found.
- Updated the source manifest, publication-metadata record, release status, publishing guide, known issues, review and validation guide.

Formal native Excel acceptance and the documented SOC, comparator, MCP and print issues remain open.

## Web-publication preparation — 2026-10-26

Repository-only update before the initial GitHub import. The unpublished package version and functional-review baseline remain unchanged.

- Replaced the command-line import guide with browser-only repository, upload, Actions, visibility, and release instructions.
- Expanded CI to reproduce and compare the reference and scenario evidence. Added a local copy of the CC BY-SA 4.0 legal text for the identified third-party terms.
- Added an Office publication-metadata record, a native Excel acceptance template, and explicit evidence checks in the stable-release gate.
- Added the author ORCID to the primary citation metadata and clarified post-import repository status documentation.

No source workbook or manuscript bytes were changed. This preparation does not establish native Microsoft Excel acceptance, resolve licensing decisions, or close functional blockers.

## 0.1.0-review.1 — 2026-10-22

Initial repository preparation and independent review package.

- Included LLM assessment v0.6.8 r4; SOC Autonomy Map v1.4.3 with original source bytes preserved.
- Added project orientation, methodology, quick start and cell-specific known issues.
- Added recorded verification evidence and reproducible read-only checks.
- Added a project mascot, citation metadata and contribution/issue templates.
- Added a source checksum manifest and package-integrity workflow.

This package version describes the repository scaffolding and review. It does not increment the supplied workbook versions. Proposed corrections have not been applied to the source workbooks. See [release status](validation/release-status.json) and the [review](docs/review.md).
