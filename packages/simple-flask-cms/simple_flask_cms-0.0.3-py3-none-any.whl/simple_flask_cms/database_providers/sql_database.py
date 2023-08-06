import typing

import flask_sqlalchemy
import traceback
from simple_flask_cms import dataclasses
from simple_flask_cms.db import DatabaseProvider


class SQLDatabaseProvider(DatabaseProvider):

    def __init__(self, app, db=None):
        if db is None:
            db = flask_sqlalchemy.SQLAlchemy(app)

        self.db = db

        class Post(db.Model):
            __tablename__ = "cms_post"
            id = db.Column(db.Integer, primary_key=True)
            path = db.Column(db.String(), index=True, unique=True)
            title = db.Column(db.String())
            nav_title = db.Column(db.String())
            sort_order = db.Column(db.Integer)
            hidden = db.Column(db.Boolean)
            content = db.Column(db.UnicodeText)

        self.Post = Post

        class Image(db.Model):
            __tablename__ = "cms_image"
            id = db.Column(db.Integer(), primary_key=True)
            file = db.Column(db.String(), index=True)
            page = db.Column(db.String())
            mime_type = db.Column(db.String())
            size = db.Column(db.String)

        self.Image = Image

        db.create_all()

    def get_page(self, path) -> typing.Optional[dataclasses.Page]:
        row = self.Post.query.filter_by(
            path=path
        ).first()
        if not row:
            return None
        return dataclasses.Page(
            path=row.path,
            title=row.title,
            nav_title=row.nav_title,
            sort_order=row.sort_order,
            content=row.content
        )

    def get_all_pages(self) -> typing.Iterable[dataclasses.StrippedPage]:
        for row in self.db.session.execute(self.db.select(
                self.Post.title,
                self.Post.path,
                self.Post.nav_title,
                self.Post.sort_order
        ).order_by(
            self.Post.path
        )):
            yield dataclasses.StrippedPage(
                title=row.title,
                path=row.path,
                nav_title=row.nav_title,
                sort_order=row.sort_order

            )

    def save_page(self, post: dataclasses.Page):
        result = self.db.session.execute(
            self.db.update(
                self.Post
            ).where(
                self.Post.path == post.path
            ).values(
                path=post.path,
                title=post.title,
                nav_title=post.nav_title,
                sort_order=post.sort_order,
                content=post.content
            )
        )
        if not result.rowcount:
            self.db.insert(
                self.Post
            ).values(
                path=post.path,
                title=post.title,
                nav_title=post.nav_title,
                sort_order=post.sort_order,
                content=post.content
            )

        self.db.session.commit()

    def delete_page(self, path):
        self.db.session.execute(
            self.db.delete().where(
                self.Post.path == path
            )
        )

    def delete_image(self, filename):
        self.db.session.execute(
            self.db.delete().where(
                self.Image.file == filename
            )
        )

    def get_image(self, file):
        return self.Image.query.where(
            file == file
        ).first()

    def get_all_images(self) -> typing.Iterable[dataclasses.Image]:
        for image in self.db.session.execute(
                self.db.select(
                    self.Image
                )
        ):
            yield dataclasses.Image(
                file=image.Image.file,
                page=image.Image.page,
                size=image.Image.size,
                mime_type=image.Image.mime_type

            )

    def get_images_for_page(self, path) -> typing.Iterable[dataclasses.Image]:
        for image in self.Image.query.where(
                self.Image.page == path
        ):
            yield dataclasses.Image(
                file=image.file,
                page=image.page,
                size=image.size,
                mime_type=image.mime_type
            )

    def save_image(self, image: dataclasses.Image):
        self.db.session.execute(
            self.db.insert(
                self.Image
            ).values(
                **image.dict()
            )
        )
        self.db.session.commit()
