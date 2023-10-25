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


app = flask.Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


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
            links, text = Crawler(url).run()
        except Exception as e:
            return {
                "message": str(e),
                "status": "ERROR"
            }

        return {
            "links": links,
            "text": text,
            "status": "SUCCESS",
        }


class Frequencies(Resource):
    def post(self):

        json_data = request.get_json(force=True)
        text = json_data['text']

        df_kmp, df_naive, df_suffix_array, df_suffix_tree, df_rabin_karp = get_word_counts(text)

        return {
            "data": "test",
            "status": "SUCCESS",
        }


api.add_resource(Home, "/")
api.add_resource(Crawl, "/crawl")
api.add_resource(Frequencies, "/frequencies")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)