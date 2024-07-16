"""create table location

Revision ID: 341e376e911f
Revises: 
Create Date: 2024-07-15 21:22:26.070985

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '341e376e911f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('location',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('latitude_longitude', geoalchemy2.types.Geometry(geometry_type='POINT', srid=4326, from_text='ST_GeomFromEWKT', name='geometry', nullable=False), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('house_number', sa.String(), nullable=False),
    sa.Column('city', sa.String(), nullable=False),
    sa.Column('state', sa.String(), nullable=False),
    sa.Column('abbreviation_state', sa.String(), nullable=False),
    sa.Column('country', sa.String(), nullable=False),
    sa.Column('abbreviation_country', sa.String(), nullable=False),
    sa.Column('postal_code', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_location_latitude_longitude', 'location', ['latitude_longitude'], unique=False, postgresql_using='gist')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_location_latitude_longitude', table_name='location', postgresql_using='gist')
    op.drop_table('location')
    # ### end Alembic commands ###
