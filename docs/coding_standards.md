# 💻 Coding Standards

VoltAudit AI maintains strict code styling across languages. Consistency in formatting, naming, and typing is key to repository maintainability.

---

## 🐍 Python Style Guidelines

All Python code must align with PEP 8 standards, enforced via `ruff` and `mypy` configurations.

### 1. Naming Conventions
- **Modules and Packages:** Lowercase with underscores (`invoice_parser.py`, `src/audit_engine/`).
- **Classes:** PascalCase (`InvoiceAuditor`, `RegulatoryComplianceRule`).
- **Functions and Methods:** snake_case (`calculate_total_amount()`, `validate_tax_id()`).
- **Variables and Parameters:** snake_case (`invoice_id`, `audit_result`).
- **Constants:** UPPERCASE with underscores (`MAX_RETRY_ATTEMPTS = 3`, `DEFAULT_TIMEOUT_SECONDS = 30`).

### 2. Type Hints are Mandatory
All public functions, methods, and class attributes must contain explicit type hints:
```python
# GOOD
def parse_invoice(file_path: Path, config: dict[str, str]) -> InvoiceData:
    ...

# BAD
def parse_invoice(file_path, config):
    ...
```
Avoid using `Any` wherever possible. Define Union types (`int | str`), Optionals (`str | None`), or specific generics instead.

### 3. Docstrings & Documentation
All modules, classes, and public methods must have docstrings using Google style:
```python
def extract_invoice_line_items(raw_text: str) -> list[LineItem]:
    """Extracts line items from raw text payload using structured regex patterns.

    Args:
        raw_text: The OCR text extracted from the physical invoice document.

    Returns:
        A list of parsed LineItem objects ready for database ingestion.

    Raises:
        InvoiceParsingError: If line items cannot be reliably parsed.
    """
    ...
```

---

## 📘 TypeScript Style Guidelines

All TypeScript/React frontend files must pass ESLint and Prettier formatting checks.

### 1. Naming Conventions
- **Component Files:** PascalCase (`InvoiceTable.tsx`, `AuditReportPanel.tsx`).
- **Functions & Hooks:** camelCase (`useInvoiceLoader`, `handleAuditSubmit`).
- **Variables & State:** camelCase (`invoices`, `setLoadingState`).
- **Types and Interfaces:** PascalCase (`AuditResult`, `UserRole`).
- **CSS Classes:** Kebab-case or CSS Modules (`audit-summary-container`, `item-status-pill`).

### 2. Strict Type Safety
- **No `any`:** Disallow the use of the `any` type. If a type is unknown, use `unknown` and assert types using user-defined type guards.
- **Interfaces for Models:** Prefer `interface` over `type` for defining data structures that might need to be extended.
  ```typescript
  interface InvoiceMetadata {
    vendorName: string;
    invoiceDate: string;
    taxRegistrationNumber: string;
  }
  ```
- **React Components:** Explicitly type component props:
  ```typescript
  interface AuditReportProps {
    reportId: string;
    onClose: () => void;
  }

  export const AuditReportPanel: React.FC<AuditReportProps> = ({ reportId, onClose }) => {
    ...
  }
  ```
