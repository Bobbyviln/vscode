#!/bin/bash

# Parameters
DB_NAME="sample.db"
TABLE_NAME="sample_table"
CSV_FILE="import_data.csv"

# Import data from CSV file to SQL table
sqlite3 $DB_NAME <<EOF
.mode csv
.import $CSV_FILE $TABLE_NAME
EOF

echo "Data imported from $CSV_FILE to $TABLE_NAME"
