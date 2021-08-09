"""Add tabnews table

Revision ID: 436579b76a10
Revises: 009738b7b22a
Create Date: 2021-08-08 22:16:31.382651

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "436579b76a10"
down_revision = "009738b7b22a"
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        "tabnews",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(length=128), nullable=False),
        sa.Column("description", sa.UnicodeText(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("author_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["author_id"], ["users.id"], onupdate="CASCADE", ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_tabnews_author_id"), "tabnews", ["author_id"], unique=False
    )


def downgrade():
    op.drop_index(op.f("ix_tabnews_author_id"), table_name="tabnews")
    op.drop_table("tabnews")
