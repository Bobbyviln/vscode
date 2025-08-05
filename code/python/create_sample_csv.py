import pandas as pd

# Create a sample DataFrame
data = {
    'id': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35]
}
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
csv_file = 'import_data.csv'
df.to_csv(csv_file, index=False)

print(f"Sample CSV file created: {csv_file}")
