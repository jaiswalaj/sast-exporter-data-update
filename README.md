# SAST Exporter Data Update

A robust and efficient Python-based utility to update JSON data exported from SAST systems using project mappings defined in an Excel file. Ideal for data reconciliation, renaming, or filtering project metadata at scale.

---

## 🔧 Features

- ✅ Handles large datasets efficiently (100,000+ records)
- ✅ Reads and modifies JSON based on Excel mappings
- ✅ Removes entries without valid mappings
- ✅ Enterprise-grade logging for full traceability
- ✅ CLI support for automation and CI/CD integration
- ✅ Clear error messages for quick resolution

---

## 📁 Use Case

You have a large `projects.json` file exported from a SAST tool (e.g., Fortify, Checkmarx, SonarQube) and need to update or clean project names using a mapping defined in an Excel sheet.

---

## 📦 Prerequisites

- Python 3.7+
- `pandas`
- `openpyxl`

Install dependencies:

```bash
pip install -r requirements.txt
