# WORTHIQ — PHASE 5 SECURITY & PRIVACY SPECIFICATION
## Data Protection, File Upload Hardening, Formula Injection Defense & Privacy Controls

---

### 1. File Upload Security Hardening

Resume upload endpoints (`/api/resumes/upload/`) enforce multi-layer defenses:
1. **Size Enforcements:** Hard 5MB limit enforced both at web server level and in Django (`MAX_UPLOAD_SIZE = 5 * 1024 * 1024`).
2. **MIME & Extension Whitelisting:** Strictly restricted to `.pdf` and `.docx`. Binary magic bytes inspected to block polyglot file attacks.
3. **Storage Sanitization:** Uploaded files stored outside web root with randomized UUID filenames preventing direct script execution.
4. **Denial of Service Mitigation:** PDF recursion depth clamped in `pypdf` to prevent decompression bombs.

---

### 2. CSV Formula Injection Defense

Spreadsheet formula injection (CWE-1236) occurs when untrusted user strings beginning with `=`, `+`, `-`, or `@` execute malicious macros in Excel or Google Sheets.
WorthIQ sanitizes every exported field in `backend/apps/reports/services/csv_generator.py`:
```python
def sanitize_csv_cell(value: Any) -> str:
    s = str(value) if value is not None else ""
    if s.startswith(('=', '+', '-', '@', '\t', '\r')):
        return f"'{s}"
    return s
```

---

### 3. Strict User Privacy & Confirmation Guarantee

1. **Zero Auto-Sync Guarantee:** WorthIQ does **not** modify user profiles automatically upon resume parsing. The candidate retains complete control via an explicit confirmation modal before any skill or field is written to their persistent profile.
2. **Access Control:** All scenarios, uploaded resumes, extractions, and reports are strictly scoped to `request.user` with object-level permission verification.
3. **Data Retention & Right to be Forgotten:** Deleting a resume immediately deletes its extracted metadata and binary file from disk. Deleting an account cascades across all scenarios, resumes, and reports.
