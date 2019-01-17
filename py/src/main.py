#!/usr/bin/env python
# coding=utf-8

import time

from flask import Flask, jsonify, request

from .shakespeare.shakespeareMatches import ShakespeareMatches
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/matches', methods=['GET', 'POST'])
def get_matches():
    line_id = request.form.get('line_id')
    if line_id is None or line_id == '':
        line_id = 150 # give a default line_id
    print(line_id)
    line_number= request.form.get('line_number')
    if line_number is None or line_number == '':
        line_number = 10 # give a default line_number
    print(line_number)
    block_number= request.form.get('block_number')
    if block_number is None or block_number == '':
        block_number = 5 # give a default block_number
    print(block_number)
    inter_play= request.form.get('inter_play')
    if inter_play is None or inter_play == '':
        inter_play = True # give a default inter_play
    print(inter_play)
    seedlines, resultlines= ShakespeareMatches(line_id, line_number, block_number, inter_play)
    #print("Seed Lines: ", seedlines)
    #print("\n")

    return jsonify({"seedlines": seedlines, "resultlines": resultlines})
#app = Flask(__name__)



#@app.route('/')
#def index():
