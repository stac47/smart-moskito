#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .albums import build_album_hierarchy, AlbumsRepository
from flask import Flask, render_template, send_file
app = Flask(__name__)


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
