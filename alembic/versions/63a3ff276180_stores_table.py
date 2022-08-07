"""Stores table

Revision ID: 63a3ff276180
Revises: dc7dbef161a8
Create Date: 2022-08-07 18:36:59.585649

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63a3ff276180'
down_revision = 'dc7dbef161a8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stores',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('country_id', sa.Integer(), nullable=False),
    sa.Column('tax_id', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('legal_name', sa.String(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('zip_code', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('active', sa.Boolean(), server_default='true', nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['country_id'], ['countries.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stores')
    # ### end Alembic commands ###
