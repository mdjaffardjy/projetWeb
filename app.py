#!/usr/bin/env python3
# coding: utf-8

from datetime import datetime

from flask import Flask, flash
from flask import abort, request, make_response
from flask import render_template, redirect, url_for
from random import choice
from werkzeug.utils import secure_filename
import json
import copy

app = Flask(__name__, static_url_path='/static')
from data import Images, Themes, get_fields

IMAGES=copy.deepcopy(Images)
print(type(IMAGES))
THEMES=copy.deepcopy(Themes)
BUTTONS=["submit"]*len(IMAGES)
NB_IMAGES=len(IMAGES)
UPLOAD_FOLDER = '/static/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    app.logger.debug('serving root URL /')
    return render_template('index.html')


@app.route('/latest', methods=['POST','GET'])
def latest():
    app.logger.debug(request.form)
    if request.method == 'POST':
        ID=request.form['ID']
        if ID :
            upvote(int(ID))
    RES = sorted(IMAGES, key=lambda k: k['date'], reverse=True) 
    return render_template('latest.html',images=RES,themes=THEMES,buttons=BUTTONS)

@app.route('/trending', methods=['POST','GET'])
def trending():
    app.logger.debug('trending')
    if request.method == 'POST':
        ID=request.form['ID']
        if ID :
            upvote(int(ID))
    RES = sorted(IMAGES, key=lambda k: k['note'], reverse=True) 
    return render_template('trending.html',images=RES,themes=THEMES,buttons=BUTTONS)

@app.route('/random', methods=['POST','GET'])
def random():
    app.logger.debug('random')
    new=[]
    randomImg = choice(IMAGES)
    new.append(randomImg)
    if request.method == 'POST':
        ID=request.form['ID']
        if ID :
            upvote(int(ID))
    return render_template('random.html',images=new,themes=THEMES, buttons=BUTTONS)

@app.route('/albums', methods=['POST','GET'])
def albums():
    app.logger.debug('albums')
    if request.method == 'POST':
        ID=request.form['ID']
        if ID :
            upvote(int(ID))
    return render_template('albums.html',themes=THEMES,images=IMAGES)


@app.route('/form', methods=['POST','GET'])
def form():
    response = render_template('form.html')
    return response

def upvote(IDimg):
    for img in IMAGES :
        if IDimg == img['id'] :
            img["note"]+=1
            BUTTONS[IDimg]="hidden"
    save(IMAGES,THEMES)


@app.route('/add/', methods=['POST','GET'])
def add():
    print("\nADD\n")
    NB_IMAGES=len(IMAGES)
    app.logger.debug('add')
    form=request.form
    if str(form['themes'])!="NA" :
        print("\nhey\n")
        th=str(form['themes']).split(";")
    else :
        th=[]
    for t in th :
        if t in THEMES.keys():
            THEMES[t].append(NB_IMAGES)
        else :
            THEMES[t]=[NB_IMAGES]
    url=form['url']
    newImg={'id': NB_IMAGES, 'date': str(datetime.now()), 'title': form['title'], 'url': url, 'note': 0}
    IMAGES.append(newImg)
    BUTTONS.append("submit")
    NB_IMAGES=len(IMAGES)
    save(IMAGES,THEMES)
    response = render_template('form.html')
    return response

@app.route('/search/', methods=['POST','GET'])
def search():
    app.logger.debug('search')
    #abort(make_response('Not implemented yet ;)', 501))
    if request.method == 'POST':
        ID=request.form['ID']
        if ID :
            upvote(int(ID))
            response = render_template('latest.html',images=IMAGES, themes=THEMES, buttons=BUTTONS)
    if request.method == 'GET':
        sw = request.args.get('pattern')
        r = request.args.get('regexp')
        RES=[]
        if sw :
            if r=="on" : # RECHERCHE PAR THEME
                for img in IMAGES :
                    if sw in get_fields(img['id']) :
                        RES.append(img)
            else : # RECHERCHE PAR MOTS CLES
                for img in IMAGES :
                    if sw.capitalize() in img['title'].capitalize() :
                        RES.append(img)
            response = render_template('search.html',images=RES,themes=THEMES, sw=sw, r=r,buttons=BUTTONS)
        else :
            response = render_template('search.html')
    return response

def save(tab1,tab2):
    print("\nSAVE\n")
    print(len(tab1))
    app.logger.debug('save')
    with open("data.json","w",encoding="utf-8") as file:
        json.dump({"Images": tab1,"Themes": tab2}, file, indent=4)

# Script starts here
if __name__ == '__main__':
    from os import environ
    DEBUG = environ.get('DEBUG')
    app.run(port=8000, debug=DEBUG)

# VIM MODLINE
# vim: ai ts=4 sw=4 sts=4 expandtab fileencoding=utf8
