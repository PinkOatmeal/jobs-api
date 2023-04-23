"""Add review model

Revision ID: 158ba7f42034
Revises: 3713c4544b19
Create Date: 2023-04-23 22:28:50.118314

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "158ba7f42034"
down_revision = "3713c4544b19"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "reviews",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("text", sa.String(), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column("reviewer_id", sa.Integer(), nullable=False),
        sa.Column("employer_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["employer_id"],
            ["employers.id"],
        ),
        sa.ForeignKeyConstraint(
            ["reviewer_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_reviews_employer_id"), "reviews", ["employer_id"], unique=False)
    op.create_index(op.f("ix_reviews_reviewer_id"), "reviews", ["reviewer_id"], unique=False)
    op.drop_column("employers", "rating")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("employers", sa.Column("rating", sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_index(op.f("ix_reviews_reviewer_id"), table_name="reviews")
    op.drop_index(op.f("ix_reviews_employer_id"), table_name="reviews")
    op.drop_table("reviews")
    # ### end Alembic commands ###