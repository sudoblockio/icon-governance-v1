"""add delegations

Revision ID: f63d08ae31ae
Revises: 135aec058ce1
Create Date: 2022-01-06 20:35:11.680192

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision = "f63d08ae31ae"
down_revision = "135aec058ce1"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "delegations",
        sa.Column("address", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("prep_address", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("value", sa.Numeric(), nullable=False),
        sa.PrimaryKeyConstraint("address", "prep_address"),
    )
    op.create_index(op.f("ix_delegations_address"), "delegations", ["address"], unique=False)
    op.create_index(
        op.f("ix_delegations_prep_address"), "delegations", ["prep_address"], unique=False
    )
    op.create_index(op.f("ix_delegations_value"), "delegations", ["value"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_delegations_value"), table_name="delegations")
    op.drop_index(op.f("ix_delegations_prep_address"), table_name="delegations")
    op.drop_index(op.f("ix_delegations_address"), table_name="delegations")
    op.drop_table("delegations")
    # ### end Alembic commands ###