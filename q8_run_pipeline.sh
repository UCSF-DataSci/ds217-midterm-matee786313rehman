#!/bin/bash
# Assignment 5, Question 8: Pipeline Automation Script
# Run the clinical trial data analysis pipeline

# Create the reports directory if it doesn't exist
mkdir -p reports

echo "Starting clinical trial data pipeline..." > reports/pipeline_log.txt

# --- Run analysis notebooks in order (q4-q7) ---

# 1. q4_exploration.ipynb
echo "Executing q4_exploration.ipynb..." >> reports/pipeline_log.txt
jupyter nbconvert --execute --to notebook q4_exploration.ipynb --output q4_executed.ipynb \
|| { echo ">>> ERROR: q4_exploration.ipynb failed. Stopping pipeline." >> reports/pipeline_log.txt; exit 1; }
echo "q4_exploration.ipynb successfully completed." >> reports/pipeline_log.txt

# 2. q5_missing_data.ipynb
echo "Executing q5_missing_data.ipynb..." >> reports/pipeline_log.txt
jupyter nbconvert --execute --to notebook q5_missing_data.ipynb --output q5_executed.ipynb \
|| { echo ">>> ERROR: q5_missing_data.ipynb failed. Stopping pipeline." >> reports/pipeline_log.txt; exit 1; }
echo "q5_missing_data.ipynb successfully completed." >> reports/pipeline_log.txt

# 3. q6_transformation.ipynb
echo "Executing q6_transformation.ipynb..." >> reports/pipeline_log.txt
jupyter nbconvert --execute --to notebook q6_transformation.ipynb --output q6_executed.ipynb \
|| { echo ">>> ERROR: q6_transformation.ipynb failed. Stopping pipeline." >> reports/pipeline_log.txt; exit 1; }
echo "q6_transformation.ipynb successfully completed." >> reports/pipeline_log.txt

# 4. q7_aggregation.ipynb 
echo "Executing q7_aggregation.ipynb..." >> reports/pipeline_log.txt
jupyter nbconvert --execute --to notebook q7_aggregation.ipynb --output q7_executed.ipynb \
|| { echo ">>> ERROR: q7_aggregation.ipynb failed. Stopping pipeline." >> reports/pipeline_log.txt; exit 1; }
echo "q7_aggregation.ipynb successfully completed." >> reports/pipeline_log.txt

echo "Pipeline complete!" >> reports/pipeline_log.txt