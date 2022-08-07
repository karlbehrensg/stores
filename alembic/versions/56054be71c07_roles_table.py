"""Roles table

Revision ID: 56054be71c07
Revises: 63a3ff276180
Create Date: 2022-08-07 18:41:07.136563

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "56054be71c07"
down_revision = "63a3ff276180"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    roles_table = op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("active", sa.Boolean(), server_default="true", nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###

    op.bulk_insert(
        roles_table,
        [
            {'name':'Admin'},
            {'name': 'Manager'},
            {'name': 'Accountant'},
            {'name': 'Seller'},
        ]
    )


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("roles")
    # ### end Alembic commands ###
