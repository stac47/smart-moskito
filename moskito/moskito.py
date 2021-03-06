#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from zipfile import ZipFile

from flask import Flask, render_template, send_file, session, request, flash,\
                  redirect, url_for
from PIL import Image

from .albums import build_album_hierarchy, AlbumsRepository


app = Flask(__name__)


def get_moskito_folder():
    MOSKITO_FOLDER = Path.home() / '.moskito'
    if not MOSKITO_FOLDER.exists():
        app.logger.info("Moskito folder created: [%s]", str(MOSKITO_FOLDER))
        MOSKITO_FOLDER.mkdir()
    return MOSKITO_FOLDER


SECRET_KEY = "development key"
MOSKITO_GALLERY_ROOT = "~/my_photos/"
MOSKITO_PASSWORD = "mypassword"
app.config.from_object(__name__)
app.config.from_pyfile(get_moskito_folder() / 'moskitorc', silent=True)


@app.route('/')
def display_root_album():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if AlbumsRepository.is_empty():
        root_album = build_album_hierarchy(app.config['MOSKITO_GALLERY_ROOT'])
        app.logger.info('Album built from %s', root_album.path)
    else:
        root_album = AlbumsRepository.get_root_album()
    return display_album(root_album.title)


@app.route('/login', methods=['GET', 'POST'])
def login():
    password = app.config['MOSKITO_PASSWORD']
    if not password:
        session['logged_in'] = True
        return redirect(url_for('display_root_album'))
    error = None
    if request.method == 'POST':
        if request.form['password'] != password:
            error = 'Wrong password'
        else:
            session['logged_in'] = True
            flash('You are logged in')
            return redirect(url_for('display_root_album'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))


@app.route('/album/<album_title>')
def display_album(album_title):
    album = AlbumsRepository.get_album_by_tile(album_title)
    return render_template('gallery.html', album=album)


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


@app.route('/album/<album_title>/download')
def download_album(album_title):
    zip_folder = get_moskito_folder() / 'zip'
    if not zip_folder.exists():
        zip_folder.mkdir()
    album = AlbumsRepository.get_album_by_tile(album_title)
    zip_file_path = zip_folder / (album.path.name + '.zip')
    if not zip_file_path.exists():
        with ZipFile(str(zip_file_path), 'w') as zip_file:
            for path in album.path.iterdir():
                if path.is_file() and path.suffixes \
                    and path.suffixes[-1] in ('.jpg,'):
                        zip_file.write(str(path), arcname=path.name)
    return send_file(str(zip_file_path), 'application/zip')

    
