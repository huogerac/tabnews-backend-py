from datetime import datetime, timezone
import sqlalchemy as sa

from ext.database import db
from models.users import User


class Tabnews(db.Model):

    __tablename__ = "tabnews"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.String(128), nullable=False)
    slug = sa.Column(sa.String(256), nullable=False, unique=True)
    description = sa.Column(sa.UnicodeText(), nullable=True)
    created_at = sa.Column(
        sa.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    author_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("users.id", onupdate="CASCADE", ondelete="SET NULL"),
        index=True,
    )

    author = db.relationship(User, backref=db.backref("tabnews", lazy="dynamic"))
