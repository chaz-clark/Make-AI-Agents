# BYUI Career Gap Analyst — Implementation Guide

Configure and deploy this Gem in the Gemini interface using the tool settings and knowledge files below.

---

## Gemini Tools

| Tool | Recommendation | Rationale |
|------|---------------|-----------|
| **Google Search** | ✅ Enable | Required — Gem must read the live BYUI catalog (byui.edu/catalog) and find real entry-level job postings. Without this, the Gem cannot fulfill its core task. |
| **Deep Research** | ⚡ Optional | Useful when a student wants a thorough industry landscape analysis (e.g., "What does the data analytics job market look like in Idaho?") but not needed for the core 9-step workflow. Enable if your users tend to ask broad industry questions. |
| **Canvas** | ⚡ Optional | The Gap Analysis Report and Next Steps Plan are structured documents the student may want to save, edit, or iterate on. Enable if you want students to refine their plan collaboratively in-session. |
| **Image Generation** | ❌ Not Needed | No visual output in the Gem's task. |
| **Create Music** | ❌ Not Needed | No audio component. |
| **Guided Learning** | ❌ Not Needed | The Gem's own 9-step sequential workflow handles progression. A separate guided learning layer would conflict with the explicit interaction chain. |

---

## Knowledge Files

| File | Purpose | Status |
|------|---------|--------|
| `byui_catalog_index.md` | Direct catalog URLs for every BYUI major, minor, and certificate — prevents the Gem from guessing URL patterns and landing on wrong pages | ⚠️ Needs User Input — scaffold provided, URLs need verification |
| `byui_employer_reference.md` | 2-3 companies per industry that commonly hire BYUI grads, with typical entry-level role titles — used in Step 5 when students don't know where to target | ✅ Generated — ready to upload, review for accuracy |

---

## Deployment Checklist

1. Open the Gemini Gem interface and create a new Gem
2. Paste the full contents of `byui_gap_analyst.txt` into the **Instructions** field
3. **Enable**: Google Search
4. **Enable if desired**: Deep Research, Canvas (both optional)
5. **Leave off**: Image Generation, Create Music, Guided Learning
6. Upload `byui_catalog_index.md` to the **Knowledge** section (complete the `<!-- USER: -->` URL entries first)
7. Upload `byui_employer_reference.md` to the **Knowledge** section
8. Run the three validation test cases from `byui_gap_analyst.json` to confirm behavior
9. Test the mission-specific case: mention a 2-year LDS mission and confirm the Gem frames it as a strength
