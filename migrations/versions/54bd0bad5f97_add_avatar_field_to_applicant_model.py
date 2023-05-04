"""Add avatar field to applicant model

Revision ID: 54bd0bad5f97
Revises: af8cefece387
Create Date: 2023-05-05 00:41:22.910179

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "54bd0bad5f97"
down_revision = "af8cefece387"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("applicants", sa.Column("avatar", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("applicants", "avatar")
    # ### end Alembic commands ###
