from flask import Flask, render_template, request, redirect
from replit import db
from random import choice
from threading import Thread
from validators import url as urlcheck
from pyperclip import copy

domain = "purr.dzhanoev.repl.co/"
#domain = "www.cutcut.cf/"

app = Flask('app')

def random_string(length):
  chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKlMNOPQRSTUVWXYZ1234567890'
  ret = ''
  for i in range(length):
    ret += choice(chars)
  return ret

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/new', methods=['POST'])
def new():
  url = request.form['url']
  if urlcheck(url):
    if not domain[:-1] in url:
      r   = random_string(4)
      while r in db:
        r = random_string(4)
      db[r] = url
      return render_template('index.html', res=domain + r)
      copy(domain+r)
    else:
      return render_template('index.html', res="It's already a CutCut link")
  elif not domain in url:
    return render_template('index.html', res='Invalid URL')  


@app.route('/<short>')
def move(short):
  try:
    return redirect(db[short])
  except KeyError:
    return render_template('index.html', res='URL doesn\'t exist')

def main():
  app.run('0.0.0.0', 8080)

thread = Thread(target=main)
thread.start()
