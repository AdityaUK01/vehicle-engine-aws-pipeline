import pandas as pd

# Read the Excel file you downloaded from Kaggle
df = pd.read_excel('dataset/Engine Data.xlsx')

# Select only the useful columns and rename them cleanly
key_cols = {
    'id': 'engine_id',
    'Title': 'engine_title',
    'production years': 'production_years',
    'displacement, cc': 'displacement_cc',
    'fuel system': 'fuel_system',
    'power output, hp': 'power_output_hp',
    'torque output, nm': 'torque_output_nm',
    'cylinder block': 'cylinder_block',
    'compression ratio': 'compression_ratio',
    'turbocharging': 'turbocharging',
    'fuel type': 'fuel_type',
    'euro standards': 'euro_standard',
    'engine lifespan, km': 'engine_lifespan_km',
    'recommended engine oil': 'recommended_oil'
}

df_raw = df[list(key_cols.keys())].rename(columns=key_cols)

# Extract manufacturer name from the title column
df_raw['manufacturer'] = df_raw['engine_title'].str.extract(r'Engine\s+([A-Za-z\-]+)')

# Extract the start year from production_years column
df_raw['year_start'] = df_raw['production_years'].str.extract(r'(\d{4})')

# Save as CSV
df_raw.to_csv('engine_data_raw.csv', index=False)

print('Done. Rows:', len(df_raw))
print('Columns:', df_raw.columns.tolist())