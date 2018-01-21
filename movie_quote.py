# -*- coding: utf-8 -*-

"""
Created on Fri Jan 12 20:39:02 2018

@author: pnadolny
"""

import logging
from flask import Flask, render_template

from flask_ask import Ask, question, session

app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

import pymysql
#rds settings
hostname  = "quotes-db.csha1uftlt6f.us-east-2.rds.amazonaws.com"
username = "admin"
password = "abcd1234"
database = "QuotesDB"

@ask.launch

def new_game():
    start_new_game = render_template('welcome')

    return question(start_new_game).reprompt(start_new_game)


@ask.intent("YesIntent")

def start():

    print ("Using pymysql…")
    myConnection = pymysql.connect( host=hostname, user=username, passwd=password, db=database )
    quote_movie = getQuote( myConnection )
    quote = quote_movie[0]
    movie = quote_movie[1]
    print("Movie is: " + movie)
    print("quote is: " + quote)
    session.attributes['movie'] = movie
    myConnection.close()

    start = render_template('start', quote=quote)
    
    return question(start).reprompt(start)


@ask.intent("MovieIntent")
def check_movie(movie):
    
    correctMovie = session.attributes['movie']
    if movie.lower() == correctMovie.lower():
        response = render_template('correctResponse')
    else:
        response = render_template('incorrectResponse')
        
    return question(response).reprompt(response)


def getQuote( conn ) :
    cur = conn.cursor()
    cur.execute( "SELECT quote, movie FROM quotes ORDER BY RAND() LIMIT 1;")
    list = []
    for  col1, col2 in cur.fetchall() :
        list.append(col1)
        list.append(col2)
    return list;



if __name__ == '__main__':

    app.run(debug=True)