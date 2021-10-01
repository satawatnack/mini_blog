import os
import time

from flask import Flask, request, abort, jsonify

from blog_db import Database

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    DEBUG = True


app = Flask(__name__)
app.config.from_object(Config())
db = Database(app)

BlogStatus = db.BlogStatus
BlogCategory = db.BlogCategory


"""
POST {url}/blog
create new blog
"""


@app.route("/blog", methods=["POST"])
def create_blog():
    req = request.get_json()

    name = req.get("name")
    content = req.get("content")
    category = req.get("category")
    author = req.get("author")

    if None in (name, content, category, author):
        return "invalid json body!", 400

    if not BlogCategory.has_value(category):
        return f"{category} not in category", 500

    new_blog = db.Blog(
        name=name,
        content=content,
        category=category,
        author=author,
        created_at=time.time(),
    )

    db.session.add(new_blog)
    db.session.commit()

    return f"{new_blog} successfully created!", 201


"""
GET {url}/blog
get all blogs
"""


@app.route("/blog", methods=["GET"])
def get_blogs():
    blogs = db.Blog.query.all()
    return jsonify([blog.as_dict() for blog in blogs])


"""
PATCH {url}/blog/:id
update blog by id (author name authentication!)
"""


@app.route("/blog/<id>", methods=["PATCH"])
def update_blog(id):
    req = request.get_json()

    blog = db.Blog.query.get(id)
    if blog is None:
        abort(404)

    # check for the ownership
    if req is None or req.get("author") != blog.author:
        return "unauthorized!", 401

    for key, value in req.items():
        if key == "id":
            return "do not patch id!", 400

        if not hasattr(blog, key):
            return "invalid json body!", 400

        setattr(blog, key, value)

    blog.updated_at = time.time()
    db.session.commit()

    return jsonify(blog.as_dict())


"""
DELETE {url}/blog/:id
delete blog by id (author name authentication!)
"""


@app.route("/blog/<id>", methods=["DELETE"])
def delete_blog(id):
    req = request.get_json()

    blog = db.Blog.query.get(id)
    if blog is None:
        abort(404)

    # check for the ownership
    if req is None or req.get("author") != blog.author:
        return "unauthorized!", 401

    db.session.delete(blog)
    db.session.commit()
    return "", 204


db.create_all()

# if call main.py directly
if __name__ == "__main__":
    app.run("0.0.0.0", port=int(os.getenv("PORT", 8080)))
