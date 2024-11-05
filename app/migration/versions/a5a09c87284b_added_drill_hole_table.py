"""added drill_hole table

Revision ID: a5a09c87284b
Revises: 6368217b4db3
Create Date: 2024-11-03 16:26:10.916687

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a5a09c87284b'
down_revision: Union[str, None] = '6368217b4db3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create the drill_hole table
    op.create_table(
        'drill_hole',
        sa.Column('drill_hole', sa.String(), primary_key=True),
        sa.Column('geological_complex', sa.String(), nullable=True),
        sa.Column('ore_zone', sa.String(), nullable=True),
    )

    # Add new drill_hole column to sample table
    op.add_column('sample', sa.Column('drill_hole_new', sa.String(), nullable=True))
    op.create_foreign_key('fk_sample_drill_hole', 'sample', 'drill_hole', ['drill_hole_new'], ['drill_hole'])

    # Data Migration
    # Transfer unique drill_hole data to drill_hole table
    connection = op.get_bind()
    result = connection.execute(
        sa.text("""
            SELECT DISTINCT drill_hole, geological_complex, ore_zone
            FROM sample
            WHERE drill_hole IS NOT NULL
        """)
    )

    drill_holes = result.fetchall()

    # Insert into drill_hole table
    for dh in drill_holes:
        connection.execute(
            sa.text("""
                INSERT INTO drill_hole (drill_hole, geological_complex, ore_zone)
                VALUES (:drill_hole, :geological_complex, :ore_zone)
            """),
            {
                'drill_hole': dh.drill_hole,
                'geological_complex': dh.geological_complex,
                'ore_zone': dh.ore_zone
            }
        )

    # Update sample table to reference new drill_hole
    connection.execute(
        sa.text("""
            UPDATE sample
            SET drill_hole_new = drill_hole
        """)
    )

    # Drop old columns from sample table
    op.drop_column('sample', 'ore_zone')
    op.drop_column('sample', 'geological_complex')
    op.drop_column('sample', 'drill_hole')

    # Rename drill_hole_new to drill_hole
    op.alter_column('sample', 'drill_hole_new', new_column_name='drill_hole')


def downgrade():
    # Add old columns back to sample table
    op.add_column('sample', sa.Column('ore_zone', sa.String(), nullable=True))
    op.add_column('sample', sa.Column('geological_complex', sa.String(), nullable=True))
    op.add_column('sample', sa.Column('drill_hole_old', sa.String(), nullable=True))

    # Data Migration
    connection = op.get_bind()
    result = connection.execute(
        sa.text("""
            SELECT s.sample_name, s.drill_hole, dh.geological_complex, dh.ore_zone
            FROM sample s
            LEFT JOIN drill_hole dh ON s.drill_hole = dh.drill_hole
        """)
    )

    for row in result:
        connection.execute(
            sa.text("""
                UPDATE sample
                SET drill_hole_old = :drill_hole,
                    geological_complex = :geological_complex,
                    ore_zone = :ore_zone
                WHERE sample_name = :sample_name
            """),
            {
                'sample_name': row.sample_name,
                'drill_hole': row.drill_hole,
                'geological_complex': row.geological_complex,
                'ore_zone': row.ore_zone
            }
        )

    # Drop foreign key and drill_hole column
    op.drop_constraint('fk_sample_drill_hole', 'sample', type_='foreignkey')
    op.drop_column('sample', 'drill_hole')

    # Rename drill_hole_old back to drill_hole
    op.alter_column('sample', 'drill_hole_old', new_column_name='drill_hole')

    # Drop the drill_hole table
    op.drop_table('drill_hole')


