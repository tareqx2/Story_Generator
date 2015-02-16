import requests
import os
from flask import Flask, jsonify
from flask import abort
from flask import request
from bs4 import BeautifulSoup
from flask.ext.cors import CORS


app = Flask(__name__)
cors = CORS(app)

IMDB_RANDOM = "http://www.imdb.com/random/title"

@app.route('/api/v1.0/story', methods=['GET'])
def get_story():
	resp = requests.get(IMDB_RANDOM)
	response = {}
	soup = BeautifulSoup(resp.text)
	description = soup.findAll("p", { "itemprop" : "description" })
	response = {"description":description}
	movieName = soup.findAll("span",{"itemprop": "name"})
	response["Name"] = movieName[0].get_text()
	soup2 = soup.findAll("div", { "itemprop" : "description" })
	
	if (soup2):
		storyline = BeautifulSoup(soup2[0].get_text())
		storyline = storyline.findAll("p")
		response["storyline"] = storyline
	return str(response), 200

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=int(os.getenv("PORT","5000")))