"""add power

Revision ID: 135aec058ce1
Revises: 4400883a1249
Create Date: 2021-12-28 11:38:37.439383

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision = "135aec058ce1"
down_revision = "4400883a1249"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("preps", sa.Column("power", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("preps", "power")
    # ### end Alembic commands ###
