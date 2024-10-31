import pandas as pd
import psycopg2

# Load the Excel document
file_path = '/mnt/data/Амазар_описания 2024.xlsx'
df = pd.read_excel(file_path)

# Establish a connection to the PostgreSQL database
connection = psycopg2.connect(
    host="localhost",
    database="your_database",
    user="your_user",
    password="your_password"
)

cursor = connection.cursor()

# Insert data into the wells table
def insert_well(well, depth, ore_zone, code):
    cursor.execute(
        """
        INSERT INTO wells (well, depth_m, ore_zone, code)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
        """, (well, depth, ore_zone, code)
    )
    return cursor.fetchone()[0]

# Insert data into the samples table
def insert_sample(sample_number, well_id, rock_type_main, complex, full_rock_name, structure, macro_description, ore_mineralization, texture, micro_description):
    cursor.execute(
        """
        INSERT INTO samples (sample_number, well_id, rock_type_main, complex, full_rock_name, structure, macro_description, ore_mineralization, texture, micro_description)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
        """, (sample_number, well_id, rock_type_main, complex, full_rock_name, structure, macro_description, ore_mineralization, texture, micro_description)
    )
    return cursor.fetchone()[0]

# Insert data into metasomatic_types table
def insert_metasomatic_type(sample_id, type_name, degree_of_metasomatic_working):
    cursor.execute(
        """
        INSERT INTO metasomatic_types (sample_id, type_name, degree_of_metasomatic_working)
        VALUES (%s, %s, %s);
        """, (sample_id, type_name, degree_of_metasomatic_working)
    )

# Insert data into rock compositions table
def insert_rock_composition(sample_id, mineral_name, composition_type_main, accessory_type, percentage_volume):
    cursor.execute(
        """
        INSERT INTO rock_compositions (sample_id, mineral_name, composition_type_main, accessory_type, percentage_volume)
        VALUES (%s, %s, %s, %s, %s);
        """, (sample_id, mineral_name, composition_type_main, accessory_type, percentage_volume)
    )

# Insert data into ore compositions table
def insert_ore_composition(sample_id, mineral_name, composition_type_main, rare, percentage_volume):
    cursor.execute(
        """
        INSERT INTO ore_compositions (sample_id, mineral_name, composition_type_main, rare, percentage_volume)
        VALUES (%s, %s, %s, %s, %s);
        """, (sample_id, mineral_name, composition_type_main, rare, percentage_volume)
    )

# Insert data into photos table
def insert_photo(sample_id, macro_photo, photo_with_analyzer, photo_without_analyzer, normal_light_photo, reflected_light_photo):
    cursor.execute(
        """
        INSERT INTO photos (sample_id, macro_photo, thin_section_photo_with_analyzer, thin_section_photo_without_analyzer, normal_light_photo, reflected_light_photo)
        VALUES (%s, %s, %s, %s, %s, %s);
        """, (sample_id, macro_photo, photo_with_analyzer, photo_without_analyzer, normal_light_photo, reflected_light_photo)
    )

# Process the Excel file and insert data into the respective tables
for index, row in df.iterrows():
    # Example of extracting data from the row and inserting into the database
    well_id = insert_well(row['well'], row['depth_m'], row['ore_zone'], row['code'])
    sample_id = insert_sample(row['sample_number'], well_id, row['rock_type_main'], row['complex'], row['full_rock_name'], row['structure'], row['macro_description'], row['ore_mineralization'], row['texture'], row['micro_description'])
    
    insert_metasomatic_type(sample_id, row['type_name'], row['degree_of_metasomatic_working'])
    insert_rock_composition(sample_id, row['mineral_name'], row['composition_type_main'], row['accessory_type'], row['percentage_volume'])
    insert_ore_composition(sample_id, row['mineral_name'], row['composition_type_main'], row['rare'], row['percentage_volume'])
    
    insert_photo(sample_id, row['macro_photo'], row['thin_section_photo_with_analyzer'], row['thin_section_photo_without_analyzer'], row['normal_light_photo'], row['reflected_light_photo'])

# Commit the transaction and close the connection
connection.commit()
cursor.close()
connection.close()



'''
-- Create wells table
CREATE TABLE wells (
    id SERIAL PRIMARY KEY,
    well VARCHAR(255),
    depth_m NUMERIC,
    ore_zone VARCHAR(255),
    code VARCHAR(50)
);

-- Create samples table
CREATE TABLE samples (
    id SERIAL PRIMARY KEY,
    sample_number VARCHAR(50),
    well_id INTEGER REFERENCES wells(id),
    rock_type_main VARCHAR(255),
    complex VARCHAR(255),
    full_rock_name TEXT,
    structure TEXT,
    macro_description TEXT,
    ore_mineralization TEXT,
    texture TEXT,
    micro_description TEXT
);

-- Create metasomatic types table
CREATE TABLE metasomatic_types (
    id SERIAL PRIMARY KEY,
    sample_id INTEGER REFERENCES samples(id),
    type_name VARCHAR(255),
    degree_of_metasomatic_working NUMERIC  -- Percentage for metasomatic working
);

-- Create rock compositions table
CREATE TABLE rock_compositions (
    id SERIAL PRIMARY KEY,
    sample_id INTEGER REFERENCES samples(id),
    mineral_name VARCHAR(255),
    composition_type_main VARCHAR(50),  -- 'Main' or 'Secondary'
    accessory_type BOOLEAN,  -- TRUE if accessory mineral
    percentage_volume NUMERIC
);

-- Create ore compositions table
CREATE TABLE ore_compositions (
    id SERIAL PRIMARY KEY,
    sample_id INTEGER REFERENCES samples(id),
    mineral_name VARCHAR(255),
    composition_type_main VARCHAR(50),  -- 'Main' or 'Secondary'
    rare BOOLEAN,  -- TRUE if rare mineral
    percentage_volume NUMERIC
);

-- Create photos table (with 5 fields for different types of photos)
CREATE TABLE photos (
    id SERIAL PRIMARY KEY,
    sample_id INTEGER REFERENCES samples(id),
    macro_photo TEXT,  -- Macro photo
    thin_section_photo_with_analyzer TEXT,  -- Photo with polarizing analyzer
    thin_section_photo_without_analyzer TEXT,  -- Photo without polarizing analyzer
    normal_light_photo TEXT,  -- Photo in normal light
    reflected_light_photo TEXT  -- Photo in reflected light
);

'''
