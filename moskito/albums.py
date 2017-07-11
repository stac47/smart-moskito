#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pathlib
import logging
logger = logging.getLogger(__name__)


class AlbumItem(object):

    def __init__(self, path):
        if isinstance(path, pathlib.Path):
            self.path = path
        elif isinstance(path, str):
            self.path = pathlib.Path(path)
        else:
            raise TypeError()
        logger.debug('AlbumItem created: %s', path)


class Picture(AlbumItem):

    def __init__(self, path):
        super().__init__(path)
        self.title = self.path.parts[-1]

    def __str__(self):
        return 'Picture [{}]'.format(self.path)


class AlbumsRepository(object):

    albums = []

    @staticmethod
    def get_root_album():
        root_albums = list(filter(lambda album: album.parent is None,
                                  AlbumsRepository.albums))
        assert(len(root_albums) == 1)
        return root_albums[0]

    @staticmethod
    def get_album_by_tile(title):
        result = list(filter(lambda album: album.title == title,
                             AlbumsRepository.albums))
        assert(len(result) == 1)
        return result[0]

    @staticmethod
    def is_empty():
        return len(AlbumsRepository.albums) == 0


class Album(AlbumItem):

    def __init__(self, path):
        super().__init__(path)
        self.parent = None
        self.title = self.path.parts[-1]
        self.albums = []
        self.pictures = []
        AlbumsRepository.albums.append(self)

    def add_album(self, album):
        album.parent = self
        self.albums.append(album)

    def add_picture(self, picture):
        self.pictures.append(picture)

    def get_picture(self, picture_title):
        pictures = list(filter(lambda pic: pic.title == picture_title,
                               self.pictures))
        if not pictures:
            pass #Raise an error
        if len(pictures) > 1:
            pass # raise an error
        return pictures[0]

    def is_root(self):
        return self.parent == None

    def __str__(self):
        return 'Album {} [{}]'.format(self.title, self.path)


def fill_album(album):
    for path in album.path.iterdir():
        if path.is_file() and path.suffixes and path.suffixes[-1] in ('.jpg,'):
            picture = Picture(path)
            album.add_picture(picture)
            logger.debug("Picture [%s] added into album [%s]", picture, album)
        if path.is_dir():
            child_album = Album(path)
            album.add_album(fill_album(child_album))
            logger.debug('Album [%s] added into album [%s]', child_album,
                                                             album)
    return album


def build_album_hierarchy(root_folder):
    root_path = pathlib.Path(root_folder)
    root_album = Album(root_path)
    return fill_album(root_album)


if __name__ == '__main__':
    album = build_album_hierarchy('/Users/stac/mes_photos')
    print(album.title)
    for child_album in album.albums:
        print("{} contains {} pictures".format(child_album.title,
                                               len(child_album.pictures)))
    for album in AlbumsRepository.albums:
        print(album.title)
    print(AlbumsRepository.get_root_album().path)
