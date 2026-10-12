import json
from pathlib import Path

def test_field_rules_json():
    # Adjust path relative to tools/ directory
    json_path = Path(__file__).resolve().parent.parent / "config" / "field_rules.json"
    
    print(f"Checking file: {json_path}")
    
    if not json_path.exists():
        print("❌ FAIL: config/field_rules.json does not exist!")
        return

    # 1. Syntax Check (Valid JSON)
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        print("✅ PASS: Syntax check (Valid JSON format)")
    except json.JSONDecodeError as e:
        print(f"❌ FAIL: Syntax error in JSON: {e}")
        return

    # 2. Structural Checks
    errors = []
    warnings = []
    seen_field_names = set()

    if "placeholder_values" not in data or not isinstance(data["placeholder_values"], list):
        errors.append("Missing or invalid 'placeholder_values' array.")

    sections = data.get("sections", [])
    if not isinstance(sections, list) or len(sections) == 0:
        errors.append("Missing or empty 'sections' array.")

    for s_idx, section in enumerate(sections, 1):
        sec_title = section.get("section", f"Section #{s_idx}")
        
        # Check standard fields
        fields = section.get("fields", [])
        for f_idx, field in enumerate(fields, 1):
            name = field.get("name")
            label = field.get("label")
            field_type = field.get("type")

            if not name:
                errors.append(f"[{sec_title}] Field #{f_idx} is missing 'name'.")
            elif name in seen_field_names:
                errors.append(f"[{sec_title}] Duplicate field name found: '{name}'.")
            else:
                seen_field_names.add(name)

            if not label:
                errors.append(f"[{sec_title}] Field '{name}' is missing 'label'.")

            if not field_type:
                errors.append(f"[{sec_title}] Field '{name}' is missing 'type'.")

        # Check checkbox groups if present
        checkbox_groups = section.get("checkbox_groups", [])
        for g_idx, group in enumerate(checkbox_groups, 1):
            grp_label = group.get("label")
            grp_fields = group.get("fields", [])

            if not grp_label:
                errors.append(f"[{sec_title}] Checkbox group #{g_idx} is missing 'label'.")
            if not grp_fields or not isinstance(grp_fields, list):
                errors.append(f"[{sec_title}] Checkbox group '{grp_label}' has no fields defined.")

    # 3. Print Results
    print("\n--- Validation Report ---")
    if errors:
        print(f"❌ Found {len(errors)} error(s):")
        for err in errors:
            print(f"  - {err}")
    else:
        print(f"✅ PASS: All {len(seen_field_names)} fields across {len(sections)} sections are structured correctly!")

if __name__ == "__main__":
    test_field_rules_json()