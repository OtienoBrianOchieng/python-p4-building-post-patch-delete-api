#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


from models import db, User, Review, Game

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

@app.route('/games')
def games():

    games = []
    for game in Game.query.all():
        game_dict = {
            "title": game.title,
            "genre": game.genre,
            "platform": game.platform,
            "price": game.price,
        }
        games.append(game_dict)

    response = make_response(
        games,
        200
    )

    return response

@app.route('/games/<int:id>', methods = ['GET', 'PATCH', 'DELETE'])
def game_by_id(id):
    game = Game.query.filter(Game.id == id).first()

    if request.method == 'GET':
        game_dict = game.to_dict()
        response = make_response(
        game_dict,
        200
        )
        return response
    elif request.method == 'DELETE':
        db.session.delete(game)
        db.session.commit()

        response_body = {
            'delete_successful' : True,
            'message' : 'Review deleted'
        }

        response = make_response(
            jsonify(response_body),
            200
        )

        return response
    elif request.method == 'PATCH':
        review = Review.query.filter_by(id=id).first()
        for attr in request.form:
            setattr (review, attr, request.form.get(attr))

            db.session.add(review)
            db.session.commit()

            review_dict = review.to_dict()
            response = make_response(
                jsonify(review_dict),
                200
            )
            return response

@app.route('/reviews', methods = ['GET', 'POST'])
def reviews():

    if request.method == 'GET':
        reviews = []
        for review in Review.query.all():
            review_dict = review.to_dict()
            reviews.append(review_dict)
        response = make_response(
            jsonify(reviews),
            200
        )
        return response
    elif request.method == 'POST':
        new_review = Review(
            score = request.form.get('score'),
            comment = request.form.get('comment'),
            game_id = request.form.get('game_id'),
            user_id = request.form.get('user_id'),
        )

        db.session.add(new_review)
        db.session.commit()

        review_dict = new_review.to_dict()
        response = make_response (
            jsonify(new_review),
            201
        )
        return response

@app.route('/users')
def users():

    users = []
    for user in User.query.all():
        user_dict = user.to_dict()
        users.append(user_dict)

    response = make_response(
        users,
        200
    )

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
