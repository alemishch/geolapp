import pandas as pd

# Load the Excel file
file_path = 'Амазар_описания 2024.xlsx'
sheet_data = pd.read_excel(file_path, sheet_name='Магматические')

# Step 1: Extract Metadata (Columns B-K, U, W, Z)
metadata = sheet_data.iloc[:, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 22, 25]]
metadata.to_excel('metadata.xlsx', index=False)

# Step 2: Mineral Composition (Columns L-O) - Write only if there is a name or name with percentage
mineral_composition = []
for idx, row in sheet_data.iterrows():
    sample_name = row[4]  # Column №
    if pd.notnull(sample_name):
        for i in range(11, 15, 2):  # L-O: mineral name and percentage
            for j in range(0, 10):  # Up to 10 values per sample
                if idx + j < len(sheet_data):
                    mineral_name = sheet_data.iloc[idx + j, i]
                    percentage = sheet_data.iloc[idx + j, i + 1]
                    main_or_secondary = "Основной" if i == 11 else "Второстепенный"
                    if pd.notnull(mineral_name):  # Write only if name exists
                        mineral_composition.append([sample_name, mineral_name, percentage, main_or_secondary])

mineral_composition_df = pd.DataFrame(mineral_composition, columns=["Sample Name", "Mineral Name", "Percentage", "Main/Secondary"])
mineral_composition_df.to_excel('mineral_composition.xlsx', index=False)

# Step 3: Accessory Minerals (Column P) - Write only if there is a mineral name
accessory_minerals = []
for idx, row in sheet_data.iterrows():
    sample_name = row[4]  # Column №
    if pd.notnull(sample_name):
        for j in range(0, 10):
            if idx + j < len(sheet_data):
                accessory_mineral = sheet_data.iloc[idx + j, 15]
                if pd.notnull(accessory_mineral):  # Write only if mineral name exists
                    accessory_minerals.append([sample_name, accessory_mineral])

accessory_minerals_df = pd.DataFrame(accessory_minerals, columns=["Sample Name", "Accessory Mineral"])
accessory_minerals_df.to_excel('accessory_minerals.xlsx', index=False)

# Step 4: Veins (Columns Q and R) - Write only if there is a vein name or vein name with percentage
veins = []
for idx, row in sheet_data.iterrows():
    sample_name = row[4]  # Column №
    if pd.notnull(sample_name):
        for j in range(0, 10):  # Up to 10 rows per sample
            if idx + j < len(sheet_data):
                vein_name = sheet_data.iloc[idx + j, 16]
                vein_percentage = sheet_data.iloc[idx + j, 17]
                if pd.notnull(vein_name):  # Write only if vein name exists
                    veins.append([sample_name, vein_name, vein_percentage])

veins_df = pd.DataFrame(veins, columns=["Sample Name", "Vein Name", "Percentage"])
veins_df.to_excel('veins.xlsx', index=False)

# Step 5: Metasomatites (Columns S and T) - Write only if there is a metasomatite name or name with percentage
metasomatites = []
for idx, row in sheet_data.iterrows():
    sample_name = row[4]  # Column №
    if pd.notnull(sample_name):
        for j in range(0, 10):
            if idx + j < len(sheet_data):
                meta_name = sheet_data.iloc[idx + j, 18]
                meta_percentage = sheet_data.iloc[idx + j, 19]
                if pd.notnull(meta_name):  # Write only if metasomatite name exists
                    metasomatites.append([sample_name, meta_name, meta_percentage])

metasomatites_df = pd.DataFrame(metasomatites, columns=["Sample Name", "Metasomatite Type", "Percentage"])
metasomatites_df.to_excel('metasomatites.xlsx', index=False)

# Step 6: Ore Mineralization (Columns AA-AD) - Write only if there is a mineral name or mineral name with percentage
ore_mineralization = []
for idx, row in sheet_data.iterrows():
    sample_name = row[4]  # Column №
    if pd.notnull(sample_name):
        for i in range(26, 30, 2):  # AA-AD: alternating between mineral name and percentage
            for j in range(0, 10):
                if idx + j < len(sheet_data):
                    mineral_name = sheet_data.iloc[idx + j, i]
                    mineral_percentage = sheet_data.iloc[idx + j, i + 1]
                    main_or_secondary = "Основной" if i == 26 else "Второстепенный"
                    if pd.notnull(mineral_name):  # Write only if mineral name exists
                        ore_mineralization.append([sample_name, mineral_name, mineral_percentage, main_or_secondary])

ore_mineralization_df = pd.DataFrame(ore_mineralization, columns=["Sample Name", "Mineral Name", "Percentage", "Main/Secondary"])
ore_mineralization_df.to_excel('ore_mineralization.xlsx', index=False)

# Step 7: Rare Ore Mineralization (Column AE) - Write only if there is a rare ore mineral name
rare_ore_mineralization = []
for idx, row in sheet_data.iterrows():
    sample_name = row[4]  # Column №
    if pd.notnull(sample_name):
        for j in range(0, 10):
            if idx + j < len(sheet_data):
                rare_ore = sheet_data.iloc[idx + j, 30]
                if pd.notnull(rare_ore):  # Write only if rare ore mineral name exists
                    rare_ore_mineralization.append([sample_name, rare_ore])

rare_ore_mineralization_df = pd.DataFrame(rare_ore_mineralization, columns=["Sample Name", "Rare Ore Mineral"])
rare_ore_mineralization_df.to_excel('rare_ore_mineralization.xlsx', index=False)

# Step 8: Save All to a Single Excel File
with pd.ExcelWriter('processed_amazar_data_final.xlsx', engine='xlsxwriter') as writer:
    metadata.to_excel(writer, sheet_name="Sheet1_Metadata", index=False)
    mineral_composition_df.to_excel(writer, sheet_name="Sheet2_Mineral_Composition", index=False)
    accessory_minerals_df.to_excel(writer, sheet_name="Sheet7_Accessory_Minerals", index=False)
    veins_df.to_excel(writer, sheet_name="Sheet3_Veins", index=False)
    metasomatites_df.to_excel(writer, sheet_name="Sheet4_Metasomatites", index=False)
    ore_mineralization_df.to_excel(writer, sheet_name="Sheet5_Ore_Mineralization", index=False)
    rare_ore_mineralization_df.to_excel(writer, sheet_name="Sheet6_Rare_Ore", index=False)
