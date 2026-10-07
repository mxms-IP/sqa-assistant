# ANSWER_KEY.md

> This file is for the document QA tool developer only. It is not part of the test artifact set and should not be included in the sample document folder presented to end users.

---

## Section 1: Planted Facts

| # | Planted Fact | File |
|---|---|---|
| 1 | Response-time limit stated as **3 seconds** | TEST_PLAN.md, Section 5 (Performance Requirement) |
| 2 | BUG-009 is **Critical severity and still Open**, listed in RELEASE_CHECKLIST.md item 1 as a release blocker | BUG-009.md (status field) + RELEASE_CHECKLIST.md (item 1) — stated in both but blocker label is only in the checklist |
| 3 | Hindi language option shows English text | BUG-011.md |
| 4 | BUG-008 was fixed in build **v0.9.2** | BUG-008.md (Build (fixed) field) |
| 5 | TC-006 failed during execution but has no matching bug report | TEST_SUMMARY_REPORT.md, Section 3 (Note paragraph below the table) |

---

## Section 2: Deliberate Conflicts

| # | Conflict | File A | File B |
|---|---|---|---|
| 1 | **BUG-003 status vs. Release Checklist.** BUG-003.md lists the bug as **Open**. RELEASE_CHECKLIST.md item 2 lists BUG-003 as one of the unresolved High bugs — consistent — but the checklist's item 7 states "BUG-001 regression confirmed clean" and implies all fixed bugs are done. A reader who skims the checklist may interpret item 7 as also covering BUG-003 since both relate to Technical Requirement 1 (icon placement). The true conflict: BUG-003 is Open but TC-002 is listed as the only failing TC in the summary — the checklist does not separately flag TC-002 as blocked, creating an inconsistency between the summary's failed TC list and the checklist's per-bug tracking. | TEST_SUMMARY_REPORT.md (TC-002 failed, BUG-003 linked) | RELEASE_CHECKLIST.md (item 2 lists BUG-003 Open, but item 7 only mentions BUG-001 for icon-related regression — implying icon issues are otherwise resolved) |
| 2 | **Pass count discrepancy.** TEST_SUMMARY_REPORT.md states total passed = **9** out of 14. However, the per-requirement breakdown table in the same report sums to: TC-001✅, TC-003✅, TC-004✅, TC-005✅ (Req 3 shows 2 passed out of 5), TC-009✅ (confirmed), TC-011✅, TC-013✅, TC-014✅ = **8** passes accounted for explicitly. The summary headline says 9, but the table only explicitly tallies 8, leaving one pass unaccounted for in the breakdown. | TEST_SUMMARY_REPORT.md (headline: 9 passed) | TEST_SUMMARY_REPORT.md, Section 2 table (row totals sum to 8 explicit passes) — conflict is within the same document |
| 3 | **BUG-005 status vs. Release Checklist item 5.** BUG-005.md Status field is **Open**. RELEASE_CHECKLIST.md item 5 states "TC-007 (bank offers retrieval) passes — ❌ Not ready — Blocked by BUG-005" — this is consistent. However, BUG-006.md (the Duplicate) notes it is "Closing this ticket; all tracking to happen under BUG-005" and its own status is **Duplicate**. The conflict: TEST_SUMMARY_REPORT.md Section 3 lists TC-007 as Failed and links it to BUG-005, but does not mention BUG-006 at all — a reader using the summary to reconcile all open bugs against failed TCs will find BUG-006 in the bug reports with no mention in either the summary or the checklist, suggesting the Duplicate was filed and closed without the QA lead updating the summary's bug reference list. | TEST_SUMMARY_REPORT.md (only BUG-005 referenced for TC-007) | BUG-006.md (exists as a separate ticket, Duplicate, not referenced in summary or checklist) |

---

## Section 3: 20 Questions with Answers

### Single-file questions (12)

| # | Question | Answer | Source file |
|---|---|---|---|
| Q1 | What is the maximum response time allowed for the chatbot? | 3 seconds | TEST_PLAN.md, Section 5 |
| Q2 | Which PRD requirement covers cross-device session continuity? | Technical Requirement 4 | TEST_PLAN.md, test case table (TC-010) |
| Q3 | What is the status of BUG-009? | Open | BUG-009.md |
| Q4 | Which bug was fixed in build v0.9.2? | BUG-008 (fabricated review content) | BUG-008.md |
| Q5 | What language does BUG-011 affect? | Hindi | BUG-011.md |
| Q6 | Which test case has no corresponding bug report despite failing? | TC-006 (Warranty and guarantee details) | TEST_SUMMARY_REPORT.md, Section 3 note |
| Q7 | How many test cases passed in Cycle 1? | 9 | TEST_SUMMARY_REPORT.md, Section 1 |
| Q8 | What is the severity of BUG-003? | High | BUG-003.md |
| Q9 | Which test cases are listed as blocked in the release checklist? | TC-010, TC-012, TC-007 | RELEASE_CHECKLIST.md, items 3, 4, 5 |
| Q10 | What device was used to reproduce BUG-003? | iPhone SE (3rd gen), iOS 17, Safari Mobile, 375px screen width | BUG-003.md |
| Q11 | What is the status of BUG-006? | Duplicate (of BUG-005) | BUG-006.md |
| Q12 | Were the exit criteria met after Cycle 1? | No — zero Critical open bugs criterion not met; pass rate below 85% | TEST_SUMMARY_REPORT.md, Section 4 |

### Multi-file questions (4)

| # | Question | Answer | Source files |
|---|---|---|---|
| Q13 | Is the release blocked, and if so by which specific bug? | Yes — BUG-009 is the release blocker (Critical, Open, cross-device session failure) | BUG-009.md + RELEASE_CHECKLIST.md item 1 |
| Q14 | TC-012 failed in testing. What bug covers it, and what is that bug's current status? | BUG-011; status is Open | TEST_SUMMARY_REPORT.md + BUG-011.md |
| Q15 | BUG-001 was found in an earlier build. Which build fixed it, and did Cycle 1 testing confirm the fix held? | Fixed in v0.9.1; confirmed clean in v0.9.2 per RELEASE_CHECKLIST.md item 7 | BUG-001.md + RELEASE_CHECKLIST.md |
| Q16 | How many High-severity bugs remain open going into the release decision, and what are their IDs? | 3 open High bugs: BUG-003, BUG-005, BUG-011 | BUG-003.md + BUG-005.md + BUG-011.md + RELEASE_CHECKLIST.md item 2 |

### Unanswerable questions (4) — no answer exists in any document

| # | Question | Why unanswerable |
|---|---|---|
| Q17 | What is the planned fix date for BUG-009? | No ETA is given in any document. BUG-009.md explicitly states "No ETA provided yet." |
| Q18 | What NLP framework or library is used by the chatbot? | Technical Requirement 5 says to use NLP libraries and frameworks but no specific library is named anywhere in the PRD or test documents. |
| Q19 | What is the chatbot's uptime SLA? | The PRD Key Metrics lists Uptime as a metric but no target percentage is defined anywhere in the PRD or test documents. |
| Q20 | Was Cycle 2 testing ever completed? | These documents only cover Cycle 1. No Cycle 2 documents exist in this set. |

---

## Section 4: PRD's Own Inconsistencies

| # | Inconsistency | Location in PRD |
|---|---|---|
| 1 | **Flipkart branding in an Amazon document.** The wireframes are labelled "Flipkart's Chatbot" (not Amazon). Technical Requirement 6 says the budget deals feature will "help users build trust on **Flipkart**." One user story says "remember my preferences and browsing history in **Flipkart** across devices." The document header and logo are Amazon. | Wireframes section; Technical Requirement 6; User Stories section |
| 2 | **Delivery timelines are both in scope and out of scope.** The Non-Goals state: "The chatbot will not handle queries related to order status, delivery tracking, or return processes." However, Technical Requirement 3 explicitly lists "delivery timelines" as information the chatbot should provide. These directly contradict each other. | Non-Goals section vs. Technical Requirement 3 |
| 3 | **Multi-channel availability (messaging platforms) has no Technical Requirement.** Key Feature 5 states the chatbot should be available via "Amazon's website, mobile app, and popular messaging platforms." No Technical Requirement covers messaging platform integration. The wireframes only show mobile app screens. | Key Features section (Feature 5) vs. Technical Requirements (none cover messaging platforms) |
