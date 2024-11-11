import os
import pandas as pd
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, func
from alembic.config import Config
from alembic import command
import sys
import numpy as np

# Add the project root directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from app.config import get_db_url
from app.samples.models import Sample, MineralComposition, OreMineralization, Vein, Metasomatite, RareOreMineralization, AccessoryMineral

# Load environment variables from .env if needed
from dotenv import load_dotenv
load_dotenv()

# Database connection and session
DATABASE_URL = get_db_url()
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Define paths to the Excel files
file_paths = {
    "metadata": "app/scripts/metadata.xlsx",
    "mineral_composition": "app/scripts/mineral_composition.xlsx",
    "ore_mineralization": "app/scripts/ore_mineralization.xlsx",
    "veins": "app/scripts/veins.xlsx",
    "metasomatites": "app/scripts/metasomatites.xlsx",
    "rare_ore_mineralization": "app/scripts/rare_ore_mineralization.xlsx",
    "accessory_minerals": "app/scripts/accessory_minerals.xlsx"
}

# Function to apply Alembic migrations
def apply_migrations():
    alembic_cfg = Config(os.path.join(os.path.dirname(__file__), "../../alembic.ini"))
    command.upgrade(alembic_cfg, "head")

# Helper function to clean and handle non-numeric 'percentage' values
def handle_percentage(column):
    return pd.to_numeric(column, errors='coerce')  # Convert non-numeric to NaN, which SQLAlchemy will interpret as NULL

async def is_database_empty(session: AsyncSession) -> bool:
    # Example: Check if the 'samples' table is empty
    result = await session.execute(select(func.count(Sample.id)))
    sample_count = result.scalar_one()
    return sample_count == 0

# Function to load data into the database
async def load_data():
    async with async_session() as session:
        if not await is_database_empty(session):
            print("Database already contains data. Skipping data loading.")
            return  # Exit the function to prevent duplicate data

        async with session.begin():
            # Sample Table
            df_metadata = pd.read_excel(file_paths["metadata"]).dropna(how='all')
            df_metadata = df_metadata.replace({np.nan: None})
            df_metadata['№'] = df_metadata['№'].astype(str)  # Ensure 'sample_name' is string
            for _, row in df_metadata.iterrows():
                sample = Sample(
                    sample_name=row['№'],
                    ore_zone=row.get('Рудная зона'),
                    drill_hole=row.get('Скважина'),
                    depth_m=row.get('Глубина, м'),
                    sample_number=row.get('№'),
                    rock_type=row.get('Порода (основное название)'),
                    geological_complex=row.get('Комплекс'),
                    code=row.get('Код'),
                    full_name=row.get('Полное название'),
                    texture=row.get('Текстура'),
                    structure=row.get('Структура'),
                    macro_description=row.get('Макроописание'),
                    micro_description=row.get('Микроописание'),
                    ore_mineralization=row.get('Рудная минерализация')
                )
                session.add(sample)

            # Mineral Composition Table
            df_mineral_composition = pd.read_excel(file_paths["mineral_composition"]).dropna(how='all')
            df_mineral_composition = df_mineral_composition.replace({np.nan: None})
            df_mineral_composition['Sample Name'] = df_mineral_composition['Sample Name'].astype(str)
            df_mineral_composition['Percentage'] = handle_percentage(df_mineral_composition['Percentage'])
            for _, row in df_mineral_composition.iterrows():
                mineral_composition = MineralComposition(
                    sample_name=row['Sample Name'],
                    mineral_name=row['Mineral Name'],
                    percentage=row.get('Percentage'),
                    main_secondary=row.get('Main/Secondary')
                )
                session.add(mineral_composition)

            # Ore Mineralization Table
            df_ore_mineralization = pd.read_excel(file_paths["ore_mineralization"]).dropna(how='all')
            df_ore_mineralization = df_ore_mineralization.replace({np.nan: None})
            df_ore_mineralization['Sample Name'] = df_ore_mineralization['Sample Name'].astype(str)
            df_ore_mineralization['Percentage'] = handle_percentage(df_ore_mineralization['Percentage'])
            for _, row in df_ore_mineralization.iterrows():
                ore_mineralization = OreMineralization(
                    sample_name=row['Sample Name'],
                    mineral_name=row['Mineral Name'],
                    percentage=row.get('Percentage'),
                    main_secondary=row.get('Main/Secondary')
                )
                session.add(ore_mineralization)

            # Veins Table
            df_veins = pd.read_excel(file_paths["veins"]).dropna(how='all')
            df_veins = df_veins.replace({np.nan: None})
            df_veins['Sample Name'] = df_veins['Sample Name'].astype(str)
            df_veins['Percentage'] = handle_percentage(df_veins['Percentage'])
            for _, row in df_veins.iterrows():
                vein = Vein(
                    sample_name=row['Sample Name'],
                    vein_name=row['Vein Name'],
                    percentage=row.get('Percentage')
                )
                session.add(vein)

            # Metasomatites Table
            df_metasomatites = pd.read_excel(file_paths["metasomatites"]).dropna(how='all')
            df_metasomatites = df_metasomatites.replace({np.nan: None})
            df_metasomatites['Sample Name'] = df_metasomatites['Sample Name'].astype(str)
            df_metasomatites['Percentage'] = handle_percentage(df_metasomatites['Percentage'])
            for _, row in df_metasomatites.iterrows():
                metasomatite = Metasomatite(
                    sample_name=row['Sample Name'],
                    metasomatite_type=row['Metasomatite Type'],
                    percentage=row.get('Percentage')
                )
                session.add(metasomatite)

            # Rare Ore Mineralization Table
            df_rare_ore_mineralization = pd.read_excel(file_paths["rare_ore_mineralization"]).dropna(how='all')
            df_rare_ore_mineralization = df_rare_ore_mineralization.replace({np.nan: None})
            df_rare_ore_mineralization['Sample Name'] = df_rare_ore_mineralization['Sample Name'].astype(str)
            for _, row in df_rare_ore_mineralization.iterrows():
                rare_ore_mineralization = RareOreMineralization(
                    sample_name=row['Sample Name'],
                    rare_ore_mineral=row['Rare Ore Mineral']
                )
                session.add(rare_ore_mineralization)

            # Accessory Minerals Table
            df_accessory_minerals = pd.read_excel(file_paths["accessory_minerals"]).dropna(how='all')
            df_accessory_minerals = df_accessory_minerals.replace({np.nan: None})
            df_accessory_minerals['Sample Name'] = df_accessory_minerals['Sample Name'].astype(str)
            for _, row in df_accessory_minerals.iterrows():
                accessory_mineral = AccessoryMineral(
                    sample_name=row['Sample Name'],
                    accessory_mineral=row['Accessory Mineral']
                )
                session.add(accessory_mineral)

        # Commit the transaction
        await session.commit()

# Main function to apply migrations and load data
def main():
    #print("Applying migrations...")
    #apply_migrations()
    #print("Migrations applied.")
    
    print("Loading data...")
    asyncio.run(load_data())
    #print("Data loaded successfully.")

if __name__ == "__main__":
    main()