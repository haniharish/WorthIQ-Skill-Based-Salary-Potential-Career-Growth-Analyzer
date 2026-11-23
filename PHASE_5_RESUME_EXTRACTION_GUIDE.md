# WORTHIQ — RESUME INTELLIGENCE & SKILL EXTRACTION GUIDE

---

### 1. Document Ingestion Pipeline

1. **File Upload:** Upload via drag-and-drop or file selector (`.pdf` or `.docx`, max 5MB).
2. **Text Parsing:**
   - PDF: Extracted using `pypdf` with UTF-8 normalization and fallback page-by-page extraction.
   - DOCX: Extracted using `python-docx` traversing paragraphs and table cell contents.
3. **Scanned PDF Handling:** If extracted plain text length is below 50 characters, the document is flagged with a warning indicating image-scanned text.

---

### 2. Skill Recognition & Taxonomy Normalization

Extracted plain text is processed through WorthIQ's canonical skill recognition engine:
1. **Token Boundary Regex:** Evaluates word boundaries while supporting special characters in tech terms (e.g. `C++`, `C#`, `.NET`, `Node.js`, `React.js`).
2. **Alias Disambiguation:** Resolves synonyms and shorthand (e.g. `k8s` -> `Kubernetes`, `react` -> `React.js`, `postgres` -> `PostgreSQL`, `aws` -> `AWS`).
3. **Snippet Extraction:** Captures 80 characters of contextual text surrounding the match.
4. **Confidence Scoring:** High (95-98%) for exact canonical matches; Medium (80-88%) for alias matches.

---

### 3. Review & Profile Synchronization

1. The frontend presents extracted skills partitioned into **New Skills Discovered** vs. **Already in Profile**.
2. Candidates select checkboxes for the skills they wish to import.
3. A confirmation modal provides explicit review of changes before triggering `/api/resumes/<id>/apply-to-profile/`.
