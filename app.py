from flask import Flask, render_template, request, redirect, flash
import pymongo
import os
import datetime
import random
from flask_moment import Moment
connection_string = os.environ.get("MONGO_URI")
if connection_string == None:
    file = open("connection_string.txt")
    connection_string = file.read().strip()
    file.close()
client = pymongo.MongoClient(connection_string)
database = client["Note_Manager_Database"]
collection = database["Note_Manager_Collection"]
app = Flask(__name__)
moment = Moment(app)
secret_key = os.environ.get("SECRET_KEY")
if secret_key == None:
    file = open("secretkey.txt")
    secret_key = file
app.secret_key = secret_key
colors = ["card text-white bg-primary mb-3", "card text-white bg-secondary mb-3", "card text-white bg-success mb-3", "card text-white bg-danger mb-3", "card text-dark bg-warning mb-3", "card text-dark bg-info mb-3",
          "card text-white bg-dark mb-3", "card border-primary mb-3", "card border-secondary mb-3", "card border-success mb-3", "card border-danger mb-3", "card border-warning mb-3", "card border-info mb-3", "card border-dark mb-3"]


@app.route("/", methods=["GET", "POST"])
def addnote():
    if request.method == "POST":
        note = request.form["Add Note"]
        user_name = request.form["Name"]
        record = {"Note": note, "Name": user_name,
                  "Post Time": datetime.datetime.utcnow()}
        collection.insert_one(record)
        flash("Your note has been recorded", "success")
        return redirect("/")
    else:
        return render_template("add_note.html")


@app.route("/notes")
def notes():
    all_documents = list()
    all_notes = collection.find()
    for i in all_notes:
        i["color"] = random.choice(colors)
        all_documents.append(i)
    return render_template("notes.html", all_documents=all_documents, colors=colors)

if __name__ == "__main__":
  app.run()