# TEST_SUMMARY_REPORT.md

**Project:** Amazon Product Details Chatbot  
**Test Cycle:** Cycle 1  
**Build tested:** v0.9.2  
**Execution period:** 2026-09-08 to 2026-09-12  
**Prepared by:** Riya Menon, QA Lead  
**Date:** 2026-09-13

---

## 1. Summary

| Metric | Count |
|---|---|
| Total test cases executed | 14 |
| Passed | 9 |
| Failed | 5 |
| Blocked | 0 |
| Not executed | 0 |

---

## 2. Results by PRD Requirement

| PRD Requirement | TCs Covered | Passed | Failed |
|---|---|---|---|
| Technical Requirement 1 (Icon placement) | TC-001, TC-002 | 1 | 1 |
| Technical Requirement 2 (Intent understanding) | TC-003, TC-004 | 2 | 0 |
| Technical Requirement 3 (Product information) | TC-005, TC-006, TC-007, TC-008, TC-009 | 2 | 3 |
| Technical Requirement 4 (Cross-device session) | TC-010 | 0 | 1 |
| Technical Requirement 5 (NLP / Multi-language) | TC-011, TC-012 | 1 | 1 |
| Key Feature 6 (Feedback rating) | TC-013 | 1 | 0 |
| Technical Requirement 6 (Budget deals) | TC-014 | 1 | 0 |

**Total passed: 9 / 14**

---

## 3. Failed Test Cases

| TC ID | Title | Bug Report |
|---|---|---|
| TC-002 | Chatbot icon placement is intuitive | BUG-003 |
| TC-007 | Bank offers retrieval | BUG-005 |
| TC-008 | Delivery timeline information | BUG-007 |
| TC-010 | Cross-device session continuity | BUG-009 |
| TC-012 | Multi-language: Hindi | BUG-011 |

> **Note:** TC-006 (Warranty and guarantee details) was recorded as **Failed** during execution on 2026-09-10. No bug report was filed at the time. This gap should be reviewed before Cycle 2 begins.

---

## 4. Exit Criteria Assessment

| Criterion | Status |
|---|---|
| All 14 test cases executed | ✅ Met |
| Zero Critical-severity open bugs | ❌ Not met — BUG-009 is Critical and Open |
| Pass rate ≥ 85% | ❌ Not met — current pass rate is 64% (9/14) |
| All High bugs fixed or have accepted workaround | ❌ Not met — BUG-005 and BUG-011 are High and Open |

**Exit criteria: NOT MET. Build v0.9.2 is not cleared for release.**

---

## 5. Recommendation

Do not proceed to release. Address BUG-009 (Critical, cross-device session) as first priority. Re-execute TC-010, TC-007, TC-008, TC-012, and TC-002 after fixes are deployed. Investigate and file a bug for TC-006 failure before Cycle 2.
