#!/bin/bash

# Parameters
DB_NAME="sample.db"
TABLE_NAME="sample_table"
CSV_FILE="exported_data.csv"

# Export data from SQL table to CSV file
sqlite3 -header -csv $DB_NAME "SELECT * FROM $TABLE_NAME;" > $CSV_FILE

echo "Data exported from $TABLE_NAME to $CSV_FILE"