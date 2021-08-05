"""Add users table

Revision ID: 009738b7b22a
Revises: 
Create Date: 2021-08-05 15:55:58.656882

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "009738b7b22a"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("password", sa.String(length=128), nullable=True),
        sa.Column("avatar", sa.UnicodeText(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )


def downgrade():
    op.drop_table("users")
