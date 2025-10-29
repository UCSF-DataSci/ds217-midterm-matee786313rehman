# TODO: Add shebang line: #!/bin/bash
# Assignment 5, Question 1: Project Setup Script
# This script creates the directory structure for the clinical trial analysis project
#!/usr/bin/env bash

# q1_setup_project.sh
# Creates the required directory structure, runs the data generator, and
# saves a directory listing to reports/directory_structure.txt

set -euo pipefail

BASE_DIR="$(pwd)"

# Parse arguments
FORCE=0
while [ "$#" -gt 0 ]; do
	case "$1" in
		--force|-f)
			FORCE=1
			shift
			;;
		*)
			# ignore unknown args
			shift
			;;
	esac
done

echo "Creating directories..."
mkdir -p "$BASE_DIR/data"
mkdir -p "$BASE_DIR/output"
mkdir -p "$BASE_DIR/reports"

echo "Running data generation script..."
DATA_FILE="$BASE_DIR/data/clinical_trial_raw.csv"
if [ "$FORCE" -eq 1 ]; then
	echo "--force passed: will (re)generate data."
fi

if [ -f "$DATA_FILE" ] && [ "$FORCE" -ne 1 ]; then
	echo "Data file $DATA_FILE found — skipping generation. Use --force to regenerate."
else
	# Prefer python3 if available, otherwise fall back to python
	if command -v python3 >/dev/null 2>&1; then
		python3 "$BASE_DIR/generate_data.py"
	else
		python "$BASE_DIR/generate_data.py"
	fi
fi

# -----------------------------
# CSV validation
# -----------------------------
echo "Validating generated CSV: $DATA_FILE"
if [ ! -f "$DATA_FILE" ]; then
	echo "ERROR: data file not found: $DATA_FILE" >&2
	exit 1
fi

# Expected columns (lowercase)
expected_cols=(
	patient_id age sex bmi enrollment_date systolic_bp diastolic_bp
	cholesterol_total cholesterol_hdl cholesterol_ldl glucose_fasting
	site intervention_group follow_up_months adverse_events outcome_cvd
	adherence_pct dropout
)

# Read header, normalize
header_line=$(head -n1 "$DATA_FILE" | tr -d '\r')
IFS=',' read -r -a header_arr <<< "$header_line"

# Normalize header entries: trim and lowercase
declare -A header_map
for col in "${header_arr[@]}"; do
	# trim spaces
	col_clean=$(echo "$col" | sed 's/^ *//; s/ *$//' | tr '[:upper:]' '[:lower:]')
	header_map["$col_clean"]=1
done

missing_count=0
for ec in "${expected_cols[@]}"; do
	if [ -z "${header_map[$ec]:-}" ]; then
		echo "  MISSING COLUMN: $ec"
		missing_count=$((missing_count+1))
	fi
done

# Row count check (exclude header)
total_lines=$(wc -l < "$DATA_FILE" | tr -d ' ')
data_rows=$((total_lines-1))
min_rows=1000
if [ "$data_rows" -lt "$min_rows" ]; then
	echo "  TOO FEW ROWS: $data_rows (minimum expected $min_rows)"
	missing_count=$((missing_count+1))
else
	echo "  Row count OK: $data_rows rows"
fi

if [ "$missing_count" -gt 0 ]; then
	echo "CSV validation FAILED ($missing_count problems)" >&2
	exit 1
else
	echo "CSV validation PASSED"
fi

echo "Saving directory structure to reports/directory_structure.txt"
if command -v tree >/dev/null 2>&1; then
	tree -a -I '__pycache__' "$BASE_DIR" > "$BASE_DIR/reports/directory_structure.txt"
else
	# Fallback to ls-based listing
	(cd "$BASE_DIR" && ls -laR | sed '/^\./d') > "$BASE_DIR/reports/directory_structure.txt"
fi

echo "Done. Directory structure written to reports/directory_structure.txt"
