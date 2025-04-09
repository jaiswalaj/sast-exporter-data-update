# SAST Exporter Data Update

A Python-based utility to update JSON data exported from SAST systems using mappings defined in an CSV file. Ideal for data reconciliation, renaming, or filtering project metadata at scale.

---

## 🔧 Features

- ✅ Reads and modifies JSON based on CSV mappings
- ✅ Removes entries without valid mappings
- ✅ Extensive logging for full traceability
- ✅ CLI support for automation and CI/CD integration
- ✅ Clear error messages for quick resolution

---

## 📁 Use Case

You have JSON files exported from SAST Exporter tool of Checkmarx and need to update or clean project names, team names, etc. using mappings defined in an CSV file.

---

## 📦 Prerequisites

- Python 3.7+
- `pandas`
- `openpyxl`

Install dependencies:

```bash
pip install pandas openpyxl
```

---

## 🛠 Usage

```bash
python sast_exporter_data_update.py --json_input_path example/projects.json --json_key_name name --json_output_path example/updated_projects.json --csv_path example/ProjectDetails.csv --old_data_col_name "Old Project Name" --new_data_col_name "New Project Name"
```

---
