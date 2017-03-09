# -*- coding: utf-8 -*-
"""User models"""
import datetime as dt

from buggy.database import Column, Model, SurrogatePK, db, reference_col,\
    relationship


class Comment(SurrogatePK, Model):
    __tablename__ = 'comments'

    name = Column(db.String(80), nullable=True)
    email = Column(db.String(80), unique=True, nullable=True)
    text = Column(db.Text(500), nullable=False)
    post_id = reference_col('posts', nullable=False)
    post = relationship('Post', backref='comments')
    created_at = Column(db.DateTime, default=dt.datetime.utcnow)

    def __repr__(self):
        return '<Comment({title})>'.format(title=self.id)

    @property
    def cute_date(self):
        return self.created_at.strftime('%B %d, %Y at %I:%M %p')
