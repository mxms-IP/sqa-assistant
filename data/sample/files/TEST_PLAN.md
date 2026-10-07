# TEST_PLAN.md

**Project:** Amazon Product Details Chatbot  
**Version:** 1.0  
**Prepared by:** Riya Menon, QA Lead  
**Date:** 2026-09-01  
**Build under test:** v0.9.2

---

## 1. Scope

This test plan covers the Amazon product details chatbot as described in the Product Requirements Document (PRD), Team: Customer Experience, Status: In Development.

**In scope:**
- Chatbot icon placement and visibility on the product screen (Technical Requirement 1)
- Intent understanding — decision-making vs. discovery queries (Technical Requirement 2)
- Product information retrieval: specifications, technical details, warranty/guarantee, bank offers, delivery timelines, user reviews (Technical Requirement 3)
- Cross-device session continuity (Technical Requirement 4)
- NLP and multi-language support (Technical Requirement 5)
- Budget-friendly deal suggestions (Technical Requirement 6)
- Feedback/rating mechanism (Key Feature 6)

**Not in scope (PRD Non-Goals):**
- Order status queries
- Delivery tracking queries
- Return and refund process queries

These remain handled by existing customer support channels and will not be tested here.

---

## 2. Test Environment

| Dimension | Details |
|---|---|
| **Web browsers** | Chrome 124, Firefox 125, Safari 17 (macOS Sonoma) |
| **Mobile — Android** | Samsung Galaxy S22, Android 14, Chrome Mobile |
| **Mobile — iOS** | iPhone 14 Pro, iOS 17, Safari Mobile |
| **Languages tested** | English, Hindi, Tamil, Telugu |
| **Product page used** | Samsung Galaxy S22 listing (electronics category) |
| **Test accounts** | Three dedicated QA accounts with clean browsing history |
| **Backend / API** | Staging environment pointing to mock product database |

---

## 3. Entry Criteria

- Build v0.9.2 deployed to staging
- Mock product database populated with at least 10 products including specifications, reviews, warranty data, and bank offers
- All Technical Requirements (1–6) marked "Dev Complete" in the sprint tracker
- Test accounts created and verified

---

## 4. Exit Criteria

- All 14 test cases executed at least once
- Zero Critical-severity open bugs
- Pass rate ≥ 85% across all test cases
- All High-severity bugs either fixed or have an accepted workaround documented

---

## 5. Performance Requirement

The chatbot must return a response within **3 seconds** of a user submitting a query. This applies to all languages and all device types covered in the test environment. (Ref: PRD Key Metrics — Response Time)

---

## 6. Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Mock product database missing warranty/bank offer data | Medium | Verify data population before test execution starts |
| NLP accuracy varies by language; Hindi/Tamil may lag | High | Prepare fixed query scripts; do not rely on free-form phrasing for language tests |
| Cross-device session test requires two simultaneous devices | Medium | Assign two QA engineers per cross-device test run |
| Feedback widget not yet integrated in staging | Low | Confirm with engineering before TC-013 is executed |

---

## 7. Test Cases

| TC ID | PRD Req | Title | Steps | Expected Result |
|---|---|---|---|---|
| TC-001 | Technical Req 1 | Chatbot icon appears on product screen | 1. Log in. 2. Search for Samsung Galaxy S22. 3. Open the product page. | Chatbot icon is visible on the product page. It does not appear on search results or home page. |
| TC-002 | Technical Req 1 | Chatbot icon placement is intuitive | 1. Open product page on mobile (Android). 2. Note icon position without any guidance. | Icon is positioned where a first-time user would look without being prompted (e.g., bottom-right corner). No overlap with Buy Now or Add to Cart buttons. |
| TC-003 | Technical Req 2 | Chatbot understands a decision-making query | 1. Open chatbot. 2. Type: "Is this phone good for gaming?" | Response addresses the query as a purchase decision — cites specs relevant to gaming. Does not just list all specs. |
| TC-004 | Technical Req 2 | Chatbot understands a discovery query | 1. Open chatbot. 2. Type: "What else is similar to this?" | Response treats the query as a discovery intent and surfaces alternative products, not just the current product's specs. |
| TC-005 | Technical Req 3 | Product specification retrieval | 1. Open chatbot. 2. Ask: "What is the RAM and processor of this phone?" | Returns accurate RAM and processor information matching the product listing. Response delivered within 3 seconds. |
| TC-006 | Technical Req 3 | Warranty and guarantee details | 1. Open chatbot. 2. Ask: "What is the warranty on this product?" | Returns warranty type, duration, and any conditions. Does not say "I don't know" or redirect to customer support for this query. |
| TC-007 | Technical Req 3 | Bank offers retrieval | 1. Open chatbot. 2. Ask: "Are there any bank offers available?" | Lists currently available bank offers (e.g., cashback, EMI offers) for the viewed product. |
| TC-008 | Technical Req 3 | Delivery timeline information | 1. Open chatbot. 2. Ask: "When will this be delivered?" | Returns estimated delivery window. Does not redirect to order tracking (which is a non-goal only for existing orders, not pre-purchase timelines). |
| TC-009 | Technical Req 3 | User reviews summary | 1. Open chatbot. 2. Ask: "What are users saying about this phone?" | Returns a summary of user reviews, including common positives and negatives. Does not fabricate reviews. |
| TC-010 | Technical Req 4 | Cross-device session continuity | 1. Open chatbot on mobile, ask one question. 2. Log into same account on desktop browser. 3. Open chatbot. | Conversation history from mobile is visible on desktop. Session continues without requiring the user to repeat context. |
| TC-011 | Technical Req 5 | Multi-language: Tamil | 1. Open chatbot. 2. Select Tamil as preferred language. 3. Ask about product specs in Tamil. | Chatbot responds in Tamil. Response is accurate and not garbled. |
| TC-012 | Technical Req 5 | Multi-language: Hindi | 1. Open chatbot. 2. Select Hindi as preferred language. 3. Ask: "इस फ़ोन की बैटरी कितने mAh की है?" | Chatbot responds in Hindi with the correct battery capacity. Response is not in English. |
| TC-013 | Key Feature 6 | Feedback rating appears on session exit | 1. Open chatbot, ask one question. 2. Click Exit. | A feedback/rating widget appears after exit. User can submit a star rating. |
| TC-014 | Technical Req 6 | Budget deal suggestions | 1. Open chatbot. 2. Ask: "Is there anything cheaper with similar features?" | Chatbot returns at least one alternative product with photo, price, and percentage savings displayed. |
