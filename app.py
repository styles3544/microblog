import os
from flask import Flask, render_template, request
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)
    client = MongoClient(os.environ.get("MONGODB_URI"))
    app.db = client.microblog
    # entries = []

    @app.route("/", methods=["GET", "POST"])
    def home():
        # print([e for e in app.db.entries.find({})]) ---> used for retrieving
        if request.method == "POST":
            form_content = request.form.get("content")
            formatted_date = datetime.today().strftime("%d-%m-%Y")
            # entries.append((form_content, formatted_date)) ---> not using list anymore
            app.db.entries.insert_one({"content": form_content, "date": formatted_date})

        entries_with_date = [
            (
                entry['content'],
                entry['date'],
                datetime.strptime(entry['date'], "%d-%m-%Y").strftime("%b-%d")
            )
            for entry in app.db.entries.find({})
        ]
        return render_template("home.html", entries=entries_with_date)
    return app