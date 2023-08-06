import abc
import typing

from . import dataclasses


class DatabaseProvider(abc.ABC):
    @abc.abstractmethod
    def get_all_pages(self) -> typing.Iterable[dataclasses.StrippedPage]:
        pass

    @abc.abstractmethod
    def get_page(self, path) -> typing.Optional[dataclasses.Page]:
        pass

    @abc.abstractmethod
    def save_page(self, post: dataclasses.Page):
        pass

    @abc.abstractmethod
    def delete_page(self, path: str):
        pass

    @abc.abstractmethod
    def get_all_images(self) -> typing.Iterable[dataclasses.Image]:
        pass

    @abc.abstractmethod
    def get_images_for_page(self, path) -> typing.Iterable[dataclasses.Image]:
        pass

    @abc.abstractmethod
    def save_image(self, image: dataclasses.Image):
        pass

    @abc.abstractmethod
    def get_image(self, filename):
        pass

    @abc.abstractmethod
    def delete_image(self, filename: str):
        pass
