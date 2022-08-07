"""Workers table

Revision ID: 93a0bca2b6d6
Revises: 56054be71c07
Create Date: 2022-08-07 18:46:43.153299

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "93a0bca2b6d6"
down_revision = "56054be71c07"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "workers",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("store_id", sa.Integer(), nullable=False),
        sa.Column("rol_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["rol_id"],
            ["roles.id"],
        ),
        sa.ForeignKeyConstraint(
            ["store_id"],
            ["stores.id"],
        ),
        sa.PrimaryKeyConstraint("user_id", "store_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("workers")
    # ### end Alembic commands ###
