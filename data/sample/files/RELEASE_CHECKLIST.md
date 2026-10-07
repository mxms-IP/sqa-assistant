# RELEASE_CHECKLIST.md

**Project:** Amazon Product Details Chatbot  
**Target build:** v0.9.2  
**Checklist owner:** Riya Menon, QA Lead  
**Date:** 2026-09-13

---

## Pre-Release Checklist

| # | Item | Status | Notes |
|---|---|---|---|
| 1 | All Critical-severity bugs resolved and regression-tested | ❌ BLOCKED | BUG-009 (cross-device session failure) is Critical and **Open** — this is a release blocker |
| 2 | All High-severity bugs resolved or have accepted workaround | ❌ Not ready | BUG-003, BUG-005, BUG-011 are High and Open |
| 3 | TC-010 (cross-device session continuity) passes | ❌ Not ready | Blocked by BUG-009 |
| 4 | TC-012 (Hindi language response) passes | ❌ Not ready | Blocked by BUG-011 |
| 5 | TC-007 (bank offers retrieval) passes | ❌ Not ready | Blocked by BUG-005 |
| 6 | Exit criteria from Test Plan met (pass rate ≥ 85%, zero Critical open bugs) | ❌ Not ready | Current pass rate 64%; Critical bug open |
| 7 | BUG-001 (icon on search results page) regression confirmed clean | ✅ Done | Fixed in v0.9.1; confirmed clean in v0.9.2 |
| 8 | BUG-008 (fabricated review content) regression confirmed clean | ✅ Done | Fixed in v0.9.2; TC-009 passes |
| 9 | BUG-012 (budget deal missing product photo) regression confirmed clean | ✅ Done | Fixed in v0.9.2; TC-014 passes |
| 10 | Performance requirement verified: chatbot responds within 3 seconds across all tested languages and devices | ⚠️ Partial | Passes for English, Tamil, Telugu; BUG-010 (Tamil timeout) marked Cannot Reproduce but not fully cleared — re-test pending |
| 11 | Feedback/rating widget confirmed functional on session exit (TC-013) | ✅ Done | Passes on all tested browsers |
| 12 | Sign-off obtained from Product, Engineering, and Data Science leads | ❌ Not ready | Pending resolution of blockers above |

---

**Release decision: HOLD.** Do not release until BUG-009 is fixed and exit criteria are met.
