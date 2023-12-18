#!/usr/bin/python
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS


# Utilities


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


def populate_tables():
    categories = [
        {"name": "Dark humor"},
        {"name": "Metahumor"},
        {"name": "Puns"}
    ]

    for i in categories:
        print(f"Inserted category: {insert_category(i)}")

    jokes = [
        {"category": 1, "text": "Where did Joe go after getting lost on a minefield? Everywhere."},
        {"category": 1, "text": "I threw a boomerang a few years ago. I now live in constant fear."},
        {"category": 3,
         "text": "I made a graph of all my past relationships... It has an \"ex\" axis and a \"why\" axis."},
        {"category": 2, "text": "A guy walks into a bar... Which is unfortunate because he has a drinking problem."},
        {"category": 3, "text": "To the guy who invented zero, thanks for nothing."}
    ]

    for i in jokes:
        print(f"Inserted joke: {insert_joke(i)}")


# DB General

def connect_to_db():
    conn = sqlite3.connect('database.db')
    conn.execute("PRAGMA foreign_keys = on")
    return conn


def create_db_tables():
    conn = connect_to_db()
    with open('create.sql') as f:
        try:
            conn.executescript(f.read())
            print("Tables created successfully")
        except Exception as e:
            print(f"Tables creation failed: {str(e)}")
    conn.close()


# Categories


def insert_category(category):
    inserted_category = {}

    conn = connect_to_db()
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO categories (name) VALUES (?)", (category['name'],))
        conn.commit()
        inserted_category = get_category_by_id(cur.lastrowid)
    except:
        conn.rollback()
    finally:
        conn.close()

    return inserted_category


def get_categories():
    categories = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM categories")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            categories.append(dict_factory(cur, i))

    except:
        categories = []

    return categories


def get_category_by_id(_id):
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM categories WHERE _id = ?", (_id,))
        row = cur.fetchone()

        # convert row object to dictionary
        category = dict_factory(cur, row)
    except:
        category = {}

    return category


# Jokes


def insert_joke(joke):
    conn = connect_to_db()
    inserted_joke = {}
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO jokes (text) VALUES (?)", (joke['text'],))
        conn.commit()
        inserted_joke = get_joke_by_id(cur.lastrowid)
    except:
        conn.rollback()
    finally:
        conn.close()

    return inserted_joke


def get_jokes():
    jokes = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM jokes")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            jokes.append(dict_factory(cur, i))

    except:
        jokes = []

    return jokes


def get_joke_by_id(_id):
    conn = connect_to_db()
    try:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM jokes WHERE _id = ?", (_id,))
        row = cur.fetchone()

        # convert row object to dictionary
        joke = dict_factory(cur, row)
    except Exception as e:
        print(f"Get joke by id failed: {str(e)}")
        joke = {}
    finally:
        conn.close()

    return joke


def get_joke_random():
    conn = connect_to_db()
    try:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM jokes ORDER BY RANDOM() LIMIT 1;")
        row = cur.fetchone()

        # convert row object to dictionary
        joke = dict_factory(cur, row)
    except:
        joke = {}
    finally:
        conn.close()

    return joke


def upvote_joke(_id):
    conn = connect_to_db()
    try:
        cur = conn.cursor()
        cur.execute("UPDATE jokes SET upvotes = upvotes + 1 WHERE _id = ?", (_id,))
        conn.commit()
        updated_joke = get_joke_by_id(_id)
    except:
        conn.rollback()
        updated_joke = {}
    finally:
        conn.close()

    return updated_joke


def downvote_joke(_id):
    conn = connect_to_db()
    try:
        cur = conn.cursor()
        cur.execute("UPDATE jokes SET downvotes = downvotes + 1 WHERE _id = ?", (_id,))
        conn.commit()
        updated_joke = get_joke_by_id(_id)
    except:
        conn.rollback()
        updated_joke = {}
    finally:
        conn.close()

    return updated_joke


# Jokes-Categories


def get_jokes_by_category(category):  # FIXME
    conn = connect_to_db()
    jokes = []
    try:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM jokes")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            jokes.append(dict_factory(cur, i))
    except:
        jokes = []
    finally:
        conn.close()

    return jokes


def get_joke_by_category_random(_id):
    conn = connect_to_db()
    try:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM jokes ORDER BY RANDOM() LIMIT 1;", (_id,))
        row = cur.fetchone()

        # convert row object to dictionary
        joke = dict_factory(cur, row)
    except:
        joke = {}
    finally:
        conn.close()

    return joke


def add_joke_to_category(_category_id, _joke_id):
    conn = connect_to_db()
    inserted_joke = {}
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO jokes_categories (joke_id, category_id) VALUES (?, ?)", (_joke_id, _category_id))
        conn.commit()
        inserted_joke = get_joke_by_id(cur.lastrowid)
    except:
        conn.rollback()
    finally:
        conn.close()

    return inserted_joke


def insert_joke_to_category(_category_id, joke):
    new_joke = insert_joke(joke)
    add_joke_to_category(new_joke["_id"], _category_id)


app = Flask(__name__)


# Jokes routes

@app.route('/api/jokes', methods=['GET'])
def api_get_jokes():
    return jsonify(get_jokes())  # Retrieve all jokes


@app.route('/api/jokes', methods=['POST'])
def api_insert_joke():
    joke = request.get_json()
    return jsonify(insert_joke(joke))  # Add a new joke without category


@app.route('/api/jokes/<_id>', methods=['GET'])
def api_get_joke(_id):
    return jsonify(get_joke_by_id(_id))  # Retrieve a joke by id


@app.route('/api/jokes/random', methods=['GET'])
def api_get_joke_random():
    return jsonify(get_joke_random())  # Retrieve a random joke from all jokes in the database


@app.route('/api/jokes/<_id>/upvote', methods=['POST'])
def api_upvote_joke(_id):
    return jsonify(upvote_joke(_id))  # Give a joke (by id) a vote of like


@app.route('/api/jokes/<_id>/downvote', methods=['POST'])
def api_downvote_joke(_id):
    return jsonify(downvote_joke(_id))  # Give a joke (by id) a vote of dislike


# Categories routes

@app.route('/api/categories', methods=['GET'])
def api_get_categories():
    return jsonify(get_categories())  # Retrieve a list of categories


@app.route('/api/categories', methods=['POST'])
def api_add_category():
    category = request.get_json()
    return jsonify(insert_category(category))  # Add a new category of jokes


# Jokes by category

@app.route('/api/categories/<_id>/jokes', methods=['GET'])
def api_get_jokes_by_category(_id):
    return jsonify(get_jokes_by_category(_id))  # Retrieve all jokes for a category # FIXME


@app.route('/api/categories/<_id>/jokes', methods=['GET'])
def api_insert_joke_to_category(_id):
    joke = request.get_json()
    return jsonify(insert_joke_to_category(_id, joke))  # Insert new joke to a category # FIXME


@app.route('/api/categories/<_category_id>/jokes/add/<_joke_id>', methods=['POST'])
def api_add_joke_to_category(_category_id, _joke_id):
    return jsonify(add_joke_to_category(_category_id, _joke_id))  # Add an existing joke to a category # FIXME


@app.route('/api/categories/<_category_id>/jokes/random', methods=['GET'])
def api_get_joke_by_category_random(_category_id):
    return jsonify(get_joke_by_category_random(_category_id))  # Retrieve a random joke from a category of jokes # FIXME


if __name__ == "__main__":
    # app.debug = True
    # app.run(debug=True)
    create_db_tables()
    populate_tables()

    CORS(app, resources={r"/*": {"origins": "*"}})
    app.run()
