#!/bin/bash
#
# Cleanup Old Analysis Files
#
# Removes timestamped analysis files, keeping only the _latest versions
#

set -e

ANALYSIS_DIR="tasks/analysis"

echo "Cleaning up old analysis files..."
echo "================================="
echo

# Count files before cleanup
BEFORE_COUNT=$(find "$ANALYSIS_DIR" -type f -name "*_202*.json" -o -name "*_202*.csv" | wc -l)

echo "Found $BEFORE_COUNT timestamped files"
echo

# Remove timestamped JSON files (keep _latest.json)
echo "Removing timestamped JSON files..."
find "$ANALYSIS_DIR" -type f -name "*_202*.json" ! -name "*_latest.json" -delete

# Remove timestamped CSV files (keep non-timestamped CSVs)
echo "Removing old timestamped CSV files..."
find "$ANALYSIS_DIR" -type f -name "*_202*.csv" -delete

# Count files after cleanup
AFTER_COUNT=$(find "$ANALYSIS_DIR" -type f -name "*_202*.json" -o -name "*_202*.csv" | wc -l)

echo
echo "Cleanup complete!"
echo "=================="
echo "Files removed: $((BEFORE_COUNT - AFTER_COUNT))"
echo "Files remaining: $AFTER_COUNT"
echo
echo "Kept files:"
ls -lh "$ANALYSIS_DIR"/*_latest.json "$ANALYSIS_DIR"/*.csv 2>/dev/null || true
