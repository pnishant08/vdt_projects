import pandas as pd

# Load Excel file
file_path = r'C:\Users\pnish\Desktop\VDT_Projects\vdt_projects\graph data.xlsx'  # Change path if needed
df = pd.read_excel(file_path)

# Step 1: Clean column names
df.columns = df.columns.str.strip()

# Step 2: Clean feature identification column
df['Feature Identification'] = df['Feature Identification'].astype(str).str.strip()

# Step 3: Filter for Corrosion defects
df_corrosion = df[df['Feature Identification'].str.contains('Corrosion', case=False, na=False)].copy()

# Debug: Show basic information
print("\n✅ Cleaned Columns:")
print(df.columns.tolist())

print("\n✅ Unique Feature Identifications:")
print(df['Feature Identification'].unique())

print("\n✅ Corrosion Defects Data (First 5 Rows):")
print(df_corrosion.head())

if df_corrosion.empty:
    print("\n❌ No Corrosion defects found in the file.")
    exit()

# Step 4: Check distance data
print("\n✅ Corrosion Distance Column Summary:")
print(df_corrosion['Abs. Distance (m)'].describe())

# Step 5: Create bins
bin_size = 500
max_distance = df_corrosion['Abs. Distance (m)'].max()
bins = list(range(0, int(max_distance) + bin_size + 1, bin_size))
print(f"\n✅ Bins Created: {bins}")

# Step 6: Apply binning
df_corrosion.loc[:, 'Distance Bin'] = pd.cut(df_corrosion['Abs. Distance (m)'], bins=bins, right=True)

print("\n✅ Corrosion Data with Bins (First 10 Rows):")
print(df_corrosion[['Abs. Distance (m)', 'Distance Bin']].head(10))

# Step 7: Group and count defects per bin
bin_counts = df_corrosion.groupby('Distance Bin', observed=False).size().reset_index(name='Metal Loss Count')

print("\n✅ Grouped Bin Counts:")
print(bin_counts)

# Final check
if bin_counts.empty:
    print("\n❌ Grouping failed. No bin counts found.")
else:
    print("\n✅ Grouping Successful! Data is ready for plotting.")
