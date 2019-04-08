#!/usr/bin/env python3
# coding: utf-8

from datetime import datetime

from flask import Flask
from flask import abort, request, make_response
from flask import render_template, redirect, url_for

app = Flask(__name__)
from data import IMAGES

def deal_with_post():
    # Get the form content
    form = request.form
    app.logger.debug(dict(form))
    # Do whatever you need with the data
    # Returns code 201 for "created" status
    return 'Hello, World! You posted {}'.format(dict(form.items())), 201


@app.route('/hello_world', methods=['GET', 'POST'])
def hello_world():
    # You may use this logger to print any variable in 
    # the terminal running the web server
    app.logger.debug('Running the hello_world function')
    app.logger.debug('Client request: method:"{0.method}'.format(request))
    if request.method == 'POST':
        # Use curl to post some data
        # curl -d"param=value" -X POST http://127.0.0.1:8000/hello_world
        return deal_with_post()
    # Open http://127.0.0.1:8000/hello_world?key=value&foo=bar&name=yourself
    # and have a look at the logs in the terminal running the server
    app.logger.debug('request arguments: {}'.format(request.args))
    if request.args:
        if 'name' in request.args.keys():
            # Use the query string argument to format the response
            return 'Hello {name} !'.format(**request.args), 200
    return 'Hello, World!', 200


@app.route('/')
def index():
    app.logger.debug('serving root URL /')
    return render_template('index.html')


@app.route('/latest')
def Latest():
    return render_template('latest.html',images=IMAGES)

@app.route('/trending')
def Trending():
    return render_template('trending.html',images=IMAGES)

@app.route('/random')
def Random():
    return render_template('random.html',images=IMAGES)

@app.route('/albums')
def Albums():
    return render_template('albums.html',images=IMAGES)

@app.route('/add/', methods=['POST','GET'])
def Add():
    app.logger.debug('add')
#    form=request.form
#    if str(form['themes'])!="NA" :
#        th=[str(form['themes'])]
#    else :
#        th=[]
#    path=form['url']
#    newImg={'title': form['title'], 'path': path, 'notes': [], 'themes': th}
#    IMAGES.append(newImg)
    response = render_template('add.html')
    return response
    
@app.route('/search/', methods=['POST','GET'])
def search():
    app.logger.debug('search')
    abort(make_response('Not implemented yet ;)', 501))
#    error = None
#    sw = request.args.get('pattern')
#    r = request.args.get('regexp')
#    RES=[]
#    if sw :
#        if r=="on" : # RECHERCHE PAR THEME
#            for img in IMAGES :
#                if sw in img['themes'] :
#                    RES.append(img)
#        else : # RECHERCHE PAR MOTS CLES
#            for img in IMAGES :
#                if sw.capitalize() in img['title'].capitalize() :
#                    RES.append(img)
#    if request.method == 'GET':
#        response = render_template('search.html',images=RES, sw=sw, r=r)
#    else :
#        response = render_template('search.html',error=error)
    return response

# Script starts here
if __name__ == '__main__':
    from os import environ
    DEBUG = environ.get('DEBUG')
    app.run(port=8000, debug=DEBUG)

# VIM MODLINE
# vim: ai ts=4 sw=4 sts=4 expandtab fileencoding=utf8
