#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from flask import Flask, render_template, send_file
from PIL import Image

from .albums import build_album_hierarchy, AlbumsRepository


app = Flask(__name__)


def get_moskito_folder():
    MOSKITO_FOLDER = Path.home() / '.moskito'
    if not MOSKITO_FOLDER.exists():
        app.logger.info("Moskito folder created: [%s]", str(MOSKITO_FOLDER))
        MOSKITO_FOLDER.mkdir()
    return MOSKITO_FOLDER


@app.route('/')
def display_root_album():
    if AlbumsRepository.is_empty():
        root_album = build_album_hierarchy('/Users/stac/mes_photos/')
    else:
        root_album = AlbumsRepository.get_root_album()
    return display_album(root_album.title)


@app.route('/album/<title>')
def display_album(title):
    album = AlbumsRepository.get_album_by_tile(title)
    return render_template('base.html', album=album)


@app.route('/album/<album_title>/picture/<picture_title>')
def display_picture(album_title, picture_title):
    album = AlbumsRepository.get_album_by_tile(album_title)
    picture = album.get_picture(picture_title)
    return send_file(str(picture.path), mimetype='image/jpeg')


@app.route('/album/<album_title>/thumbnail/<picture_title>')
def display_thumbnail(album_title, picture_title):
    thumbnails_folder = get_moskito_folder() / 'thumbnails'
    if not thumbnails_folder.exists():
        thumbnails_folder.mkdir()
        app.logger.info("Thumbnails folder created: [%s]",
                        str(thumbnails_folder))

    album = AlbumsRepository.get_album_by_tile(album_title)
    picture = album.get_picture(picture_title)
    album_thumbnails = thumbnails_folder / picture.path.parent.name
    if not album_thumbnails.exists():
        album_thumbnails.mkdir()
        app.logger.info("Album thumbnails folder created: [%s]",
                        str(album_thumbnails))
    thumbnail_path = album_thumbnails / ( 'thumbnail.' + picture.path.name)
    if not thumbnail_path.exists():
        image = Image.open(str(picture.path))
        max_size = (252, 336)
        image.thumbnail(max_size)
        image.save(str(thumbnail_path), 'JPEG')
        app.logger.info("Thumbnail created: [%s]",
                        str(thumbnail_path))
    return send_file(str(thumbnail_path), mimetype='image/jpeg')

