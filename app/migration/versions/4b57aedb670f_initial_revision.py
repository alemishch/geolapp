"""Initial revision

Revision ID: 4b57aedb670f
Revises: 
Create Date: 2024-10-31 00:33:47.204362

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4b57aedb670f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sample',
    sa.Column('sample_name', sa.String(), nullable=False),
    sa.Column('ore_zone', sa.String(), nullable=True),
    sa.Column('drill_hole', sa.String(), nullable=True),
    sa.Column('depth_m', sa.Float(), nullable=True),
    sa.Column('sample_number', sa.String(), nullable=True),
    sa.Column('rock_type', sa.String(), nullable=True),
    sa.Column('geological_complex', sa.String(), nullable=True),
    sa.Column('code', sa.String(), nullable=True),
    sa.Column('full_name', sa.String(), nullable=True),
    sa.Column('texture', sa.String(), nullable=True),
    sa.Column('structure', sa.String(), nullable=True),
    sa.Column('macro_description', sa.Text(), nullable=True),
    sa.Column('micro_description', sa.Text(), nullable=True),
    sa.Column('ore_mineralization', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('sample_name'),
    sa.UniqueConstraint('sample_name')
    )
    op.create_table('accessory_minerals',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sample_name', sa.String(), nullable=False),
    sa.Column('accessory_mineral', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['sample_name'], ['sample.sample_name'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('metasomatites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sample_name', sa.String(), nullable=False),
    sa.Column('metasomatite_type', sa.String(), nullable=False),
    sa.Column('percentage', sa.Float(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['sample_name'], ['sample.sample_name'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('mineral_composition',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sample_name', sa.String(), nullable=False),
    sa.Column('mineral_name', sa.String(), nullable=False),
    sa.Column('percentage', sa.Float(), nullable=True),
    sa.Column('main_secondary', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['sample_name'], ['sample.sample_name'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ore_mineralization',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sample_name', sa.String(), nullable=False),
    sa.Column('mineral_name', sa.String(), nullable=False),
    sa.Column('percentage', sa.Float(), nullable=True),
    sa.Column('main_secondary', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['sample_name'], ['sample.sample_name'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rare_ore_mineralization',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sample_name', sa.String(), nullable=False),
    sa.Column('rare_ore_mineral', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['sample_name'], ['sample.sample_name'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('veins',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sample_name', sa.String(), nullable=False),
    sa.Column('vein_name', sa.String(), nullable=False),
    sa.Column('percentage', sa.Float(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['sample_name'], ['sample.sample_name'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('veins')
    op.drop_table('rare_ore_mineralization')
    op.drop_table('ore_mineralization')
    op.drop_table('mineral_composition')
    op.drop_table('metasomatites')
    op.drop_table('accessory_minerals')
    op.drop_table('sample')
    # ### end Alembic commands ###
