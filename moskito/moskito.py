#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .albums import build_album_hierarchy, AlbumsRepository
from flask import Flask, render_template
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
