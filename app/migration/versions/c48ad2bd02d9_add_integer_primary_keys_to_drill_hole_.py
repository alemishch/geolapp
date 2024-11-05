"""Add integer primary keys to drill_hole and sample

Revision ID: c48ad2bd02d9
Revises: a5a09c87284b
Create Date: 2024-11-04 01:20:47.105845

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c48ad2bd02d9'
down_revision: Union[str, None] = 'a5a09c87284b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    ### Step 1: Add 'id' Columns to 'drill_hole' and 'sample' Tables ###
    op.add_column('drill_hole', sa.Column('id', sa.Integer(), nullable=True))
    op.add_column('sample', sa.Column('id', sa.Integer(), nullable=True))

    ### Step 2: Create Sequences and Populate 'id' Columns ###
    # For 'drill_hole' table
    op.execute('CREATE SEQUENCE drill_hole_id_seq OWNED BY drill_hole.id')
    op.execute("ALTER TABLE drill_hole ALTER COLUMN id SET DEFAULT nextval('drill_hole_id_seq')")
    op.execute("SELECT setval('drill_hole_id_seq', COALESCE((SELECT MAX(id) FROM drill_hole), 0) + 1)")
    op.execute("UPDATE drill_hole SET id = nextval('drill_hole_id_seq')")

    # For 'sample' table
    op.execute('CREATE SEQUENCE sample_id_seq OWNED BY sample.id')
    op.execute("ALTER TABLE sample ALTER COLUMN id SET DEFAULT nextval('sample_id_seq')")
    op.execute("SELECT setval('sample_id_seq', COALESCE((SELECT MAX(id) FROM sample), 0) + 1)")
    op.execute("UPDATE sample SET id = nextval('sample_id_seq')")

    ### Step 3: Set 'id' Columns as NOT NULL ###
    op.alter_column('drill_hole', 'id', nullable=False)
    op.alter_column('sample', 'id', nullable=False)

    ### Step 4: Drop Foreign Key Constraints ###
    # Replace <constraint_name> with the actual constraint names from your database

    # Drop foreign key from 'sample' to 'drill_hole'
    op.drop_constraint('fk_sample_drill_hole', 'sample', type_='foreignkey')

    # Drop foreign keys from related tables to 'sample'
    op.drop_constraint('photos_sample_name_fkey', 'photos', type_='foreignkey')
    op.drop_constraint('mineral_composition_sample_name_fkey', 'mineral_composition', type_='foreignkey')
    op.drop_constraint('ore_mineralization_sample_name_fkey', 'ore_mineralization', type_='foreignkey')
    op.drop_constraint('veins_sample_name_fkey', 'veins', type_='foreignkey')
    op.drop_constraint('metasomatites_sample_name_fkey', 'metasomatites', type_='foreignkey')
    op.drop_constraint('rare_ore_mineralization_sample_name_fkey', 'rare_ore_mineralization', type_='foreignkey')
    op.drop_constraint('accessory_minerals_sample_name_fkey', 'accessory_minerals', type_='foreignkey')

    ### Step 5: Drop Old Primary Keys ###
    op.drop_constraint('drill_hole_pkey', 'drill_hole', type_='primary')
    op.drop_constraint('sample_pkey', 'sample', type_='primary')

    ### Step 6: Create New Primary Keys on 'id' Columns ###
    op.create_primary_key('drill_hole_pkey', 'drill_hole', ['id'])
    op.create_primary_key('sample_pkey', 'sample', ['id'])

    ### Step 7: Add Unique Constraints ###
    op.create_unique_constraint('uq_drill_hole_drill_hole', 'drill_hole', ['drill_hole'])
    op.create_unique_constraint('uq_sample_sample_name', 'sample', ['sample_name'])

    ### Step 8: Update Foreign Keys in 'sample' Table ###
    # Rename 'drill_hole' column to 'drill_hole_name'
    op.alter_column('sample', 'drill_hole', new_column_name='drill_hole_name')

    # Add 'drill_hole_id' column
    op.add_column('sample', sa.Column('drill_hole_id', sa.Integer(), nullable=True))

    # Update 'drill_hole_id' based on 'drill_hole_name'
    op.execute('''
        UPDATE sample
        SET drill_hole_id = dh.id
        FROM drill_hole dh
        WHERE sample.drill_hole_name = dh.drill_hole
    ''')

    # If 'drill_hole_id' should be NOT NULL, uncomment the following line
    # op.alter_column('sample', 'drill_hole_id', nullable=False)

    # Create new foreign key constraint
    op.create_foreign_key('sample_drill_hole_id_fkey', 'sample', 'drill_hole', ['drill_hole_id'], ['id'])

    # Drop 'drill_hole_name' column if no longer needed
    op.drop_column('sample', 'drill_hole_name')

    ### Step 9: Update Foreign Keys in Related Tables ###
    related_tables = [
        'photos',
        'mineral_composition',
        'ore_mineralization',
        'veins',
        'metasomatites',
        'rare_ore_mineralization',
        'accessory_minerals'
    ]

    for table_name in related_tables:
        # Rename 'sample_name' to 'sample_name_old'
        op.alter_column(table_name, 'sample_name', new_column_name='sample_name_old')

        # Add 'sample_id' column
        op.add_column(table_name, sa.Column('sample_id', sa.Integer(), nullable=True))

        # Update 'sample_id' based on 'sample_name_old'
        op.execute(f'''
            UPDATE {table_name}
            SET sample_id = s.id
            FROM sample s
            WHERE {table_name}.sample_name_old = s.sample_name
        ''')

        # If 'sample_id' should be NOT NULL, uncomment the following line
        # op.alter_column(table_name, 'sample_id', nullable=False)

        # Create new foreign key constraint
        op.create_foreign_key(f'{table_name}_sample_id_fkey', table_name, 'sample', ['sample_id'], ['id'])

        # Drop 'sample_name_old' column
        op.drop_column(table_name, 'sample_name_old')


def downgrade():
    ### Reverse the Upgrade Steps ###

    ### Step 1: Add Back Old Columns ###
    op.add_column('sample', sa.Column('drill_hole_name', sa.String(), nullable=True))

    related_tables = [
        'photos',
        'mineral_composition',
        'ore_mineralization',
        'veins',
        'metasomatites',
        'rare_ore_mineralization',
        'accessory_minerals'
    ]

    for table_name in related_tables:
        op.add_column(table_name, sa.Column('sample_name_old', sa.String(), nullable=True))

    ### Step 2: Repopulate Old Columns ###
    # Repopulate 'drill_hole_name' in 'sample' table
    op.execute('''
        UPDATE sample
        SET drill_hole_name = dh.drill_hole
        FROM drill_hole dh
        WHERE sample.drill_hole_id = dh.id
    ''')

    # Repopulate 'sample_name_old' in related tables
    for table_name in related_tables:
        op.execute(f'''
            UPDATE {table_name}
            SET sample_name_old = s.sample_name
            FROM sample s
            WHERE {table_name}.sample_id = s.id
        ''')

    ### Step 3: Drop New Foreign Key Constraints ###
    op.drop_constraint('sample_drill_hole_id_fkey', 'sample', type_='foreignkey')
    for table_name in related_tables:
        op.drop_constraint(f'{table_name}_sample_id_fkey', table_name, type_='foreignkey')

    ### Step 4: Drop New Columns ###
    op.drop_column('sample', 'drill_hole_id')
    for table_name in related_tables:
        op.drop_column(table_name, 'sample_id')

    ### Step 5: Rename Old Columns Back ###
    op.alter_column('sample', 'drill_hole_name', new_column_name='drill_hole')
    for table_name in related_tables:
        op.alter_column(table_name, 'sample_name_old', new_column_name='sample_name')

    ### Step 6: Recreate Old Foreign Key Constraints ###
    op.create_foreign_key('fk_sample_drill_hole', 'sample', 'drill_hole', ['drill_hole'], ['drill_hole'])
    for table_name in related_tables:
        op.create_foreign_key(f'{table_name}_sample_name_fkey', table_name, 'sample', ['sample_name'], ['sample_name'])

    ### Step 7: Drop New Primary Keys ###
    op.drop_constraint('drill_hole_pkey', 'drill_hole', type_='primary')
    op.drop_constraint('sample_pkey', 'sample', type_='primary')

    ### Step 8: Drop 'id' Columns ###
    op.drop_column('drill_hole', 'id')
    op.drop_column('sample', 'id')

    ### Step 9: Recreate Old Primary Keys ###
    op.create_primary_key('drill_hole_pkey', 'drill_hole', ['drill_hole'])
    op.create_primary_key('sample_pkey', 'sample', ['sample_name'])

    ### Step 10: Drop Unique Constraints ###
    op.drop_constraint('uq_drill_hole_drill_hole', 'drill_hole', type_='unique')
    op.drop_constraint('uq_sample_sample_name', 'sample', type_='unique')

    ### Step 11: Drop Sequences ###
    op.execute('DROP SEQUENCE IF EXISTS drill_hole_id_seq')
    op.execute('DROP SEQUENCE IF EXISTS sample_id_seq')