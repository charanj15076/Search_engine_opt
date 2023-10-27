import os
import json
import datetime

import pandas as pd

import flask
from flask import request
from flask_restful import Resource, Api
from flask_cors import CORS

from crawler import Crawler
from word_count import get_word_counts
from word_search import get_occurrences


app = flask.Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

crawler = Crawler('')

# helper to object turn into json
class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


class Home(Resource):
    def get(self):
        data = {
            "message" : "Hello! API is running!"
        }

        return {
            "data": data,
        }


class Crawl(Resource):
    def get(self):
        args = request.args
        url = args['url']

        # url = "https://www.python.org/"

        try:
            links, text, img_name = crawler.run(url)
        except Exception as e:
            return {
                "message": str(e),
                "status": "ERROR"
            }

        return {
            "links": links,
            "text": text,
            "img_url": flask.url_for('static', filename=img_name),
            "status": "SUCCESS",
        }


class Frequencies(Resource):
    def post(self):

        json_data = request.get_json(force=True)
        text = json_data['text']

        res, times = get_word_counts(text)

        return {
            "data": {
                "kmp": res["kmp"].to_json(),
                "naive": res["naive"].to_json(),
                "suffix_array": res["suffix_array"].to_json(),
                "suffix_tree": res["suffix_tree"].to_json(),
                "rabin_karp": res["rabin_karp"].to_json(),
            },
            "times": {
                "kmp": times["kmp"],
                "naive": times["naive"],
                "suffix_array": times["suffix_array"],
                "suffix_tree": times["suffix_tree"],
                "rabin_karp": times["rabin_karp"],
            },
            "status": "SUCCESS",
        }


class Search(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        text = json_data['text']
        term = json_data['term']

        res, times = get_occurrences(text, term)

        return {
            "data": {
                "kmp": res["kmp"],
                "naive": res["naive"],
                "suffix_array": res["suffix_array"],
                "suffix_tree": res["suffix_tree"],
                "rabin_karp": res["rabin_karp"],
            },
            "times": {
                "kmp": times["kmp"],
                "naive": times["naive"],
                "suffix_array": times["suffix_array"],
                "suffix_tree": times["suffix_tree"],
                "rabin_karp": times["rabin_karp"],
            },
            "status": "SUCCESS",
        }


api.add_resource(Home, "/")
api.add_resource(Crawl, "/crawl")
api.add_resource(Frequencies, "/frequencies")
api.add_resource(Search, "/search")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)