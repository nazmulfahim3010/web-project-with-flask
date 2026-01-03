from sqlalchemy import Enum
from flask_login import UserMixin
from sqlalchemy.sql import func
from . import db

class UserInfo(db.Model, UserMixin):
    __tablename__ = 'user_info'

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)

    user_name = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)

    contact = db.Column(db.String(150))
    bio = db.Column(db.Text)

    # ✅ PASSWORD (HASHED)
    password = db.Column(db.String(255), nullable=False)

    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now()
    )

    # relationships
    blogs = db.relationship(
        'Blog',
        backref='author',
        cascade='all, delete',
        passive_deletes=True
    )

    comments = db.relationship(
        'BlogComment',
        backref='user',
        cascade='all, delete',
        passive_deletes=True
    )

    reactions = db.relationship(
        'BlogReaction',
        backref='user',
        cascade='all, delete',
        passive_deletes=True
    )


class Blog(db.Model):
    __tablename__ = 'blog'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(255), nullable=False)
    mini_blog = db.Column(db.Text, nullable=False)

    created_by = db.Column(
        db.Integer,
        db.ForeignKey('user_info.id', ondelete='CASCADE'),
        nullable=False
    )

    dlt = db.Column(db.Boolean, default=False)

    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now()
    )

    comments = db.relationship(
        'BlogComment',
        backref='blog',
        cascade='all, delete',
        passive_deletes=True
    )

    reactions = db.relationship(
        'BlogReaction',
        backref='blog',
        cascade='all, delete',
        passive_deletes=True
    )


class BlogComment(db.Model):
    __tablename__ = 'blog_comments'

    id = db.Column(db.Integer, primary_key=True)

    blog_id = db.Column(
        db.Integer,
        db.ForeignKey('blog.id', ondelete='CASCADE'),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user_info.id', ondelete='CASCADE'),
        nullable=False
    )

    comment_text = db.Column(db.Text, nullable=False)

    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now()
    )

class BlogReaction(db.Model):
    __tablename__ = 'blog_reactions'

    id = db.Column(db.Integer, primary_key=True)

    blog_id = db.Column(
        db.Integer,
        db.ForeignKey('blog.id', ondelete='CASCADE'),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user_info.id', ondelete='CASCADE'),
        nullable=False
    )

    reaction = db.Column(
        Enum('like', 'dislike', name='reaction_enum'),
        nullable=False
    )

    __table_args__ = (
        db.UniqueConstraint('blog_id', 'user_id', name='unique_react'),
    )
