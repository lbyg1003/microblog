import os
import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()  # create env variables using vars in .env for local testing


def create_app():  # flask app factory pattern. ensure the app.py won't be run for multiple times during deployment
    app = Flask(__name__)
    mongodb_url = os.environ.get("MONGODB_URL")
    client = MongoClient(mongodb_url)  # connect to the cluster
    app.db = client.microBlog   # access the db in the cluster

    @app.route("/", methods=["GET", "POST"])  # tell flask this endpoint might receive POST/GET requests
    def home():
        if request.method == "POST":
            entry_content = request.form.get("content")  # request.form.get({input element *name* in html})
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            formatted_date_2 = datetime.datetime.today().strftime("%b %d")
            app.db.entries.insert({"content": entry_content,  # save data to db.collection
                                   "date": formatted_date,
                                   "formatted_date": formatted_date_2})
        entries = [(e['content'], e['date'], e['formatted_date'])
                   for e in app.db.entries.find({})]  # e is a dict. app.db.entries.find({}) return a cursor
        return render_template("home.html", entries=entries)

    return app

