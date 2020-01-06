from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import config

app = Flask(__name__)
# Enable CORS
CORS(app)
# Beautiful JSON
# app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# TODO Change this!
app.config['JWT_SECRET_KEY'] = 'Super_Secret_JWT_KEY'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
# Database manager
db = SQLAlchemy(app)
jwt = JWTManager(app)

# TODO Fix problem with circular import
from places_database import Place, Address

# TODO move it to the separate file
#  -------------------------------------------- Login ----------------------------------------------------------------
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    if not username:
        return jsonify({'success': False, 'message': 'Bad username or password'}), 400
    if not password:
        return jsonify({'success': False, 'message': 'Bad username or password'}), 400

    place = Place.query.filter_by(username=username).first()
    if place is None:
        return jsonify({'success': False, 'message': 'Bad username or password'}), 401
    # Identity by id
    access_token = create_access_token(identity=place.id)
    return jsonify({'success': True, 'token': access_token, 'place': place.to_dict()}), 200


@app.route('/current-place', methods=['GET'])
@jwt_required
def get_auth_info():
    """
    :return: info about currently authorized place
    """
    return get_place(get_jwt_identity())

# ------------------------------------------ // LOGIN ------------------------------------------------------------------


@app.route('/places')
def get_all_places():
    """
    :return: all places (restaurants) in the database in json
    """
    places = list(map(lambda place: place.to_dict(), Place.query.all()))
    return jsonify(places)


@app.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """
    :return: all places (restaurants) in the database in json
    """
    place = Place.query.get(place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app.route('/places', methods=['POST'])
def create_new_place():
    """
    Creates new place in places with info given in JSON
    :return: ID of the new place
    """
    data = request.json
    new_place = Place()
    new_place.address = Address()
    new_place.update_info(data)
    # TODO what if existing username
    res = {'place': new_place.to_dict(), 'token': create_access_token(identity=new_place.id)}
    return jsonify(res)


def check_access(place_id: int):
    """
    Checks if place_id is the same as the id of currently authorized place.
    If not - returns code 403.
    """
    # id of authorized restaurant account
    current_id = get_jwt_identity()
    # If it's not account of this restaurant then return 403 Forbidden
    if current_id != place_id:
        abort(403)


@app.route('/places/<place_id>', methods=['PATCH'])
@jwt_required
def patch_place(place_id: int):
    """
    Changes number of free seats of place with that id
    :param place_id: id of the place
    """
    place_id = int(place_id)
    check_access(place_id)
    place = Place.query.get(place_id)
    data = request.json
    place.update_info(data)
    return get_place(place_id)

@app.route('/places/<place_id>', methods=['DELETE'])
@jwt_required
def delete_place(place_id: int):
    """
    Changes number of free seats of place with that id
    :param place_id: id of the place
    :return info about deleted place
    """
    place_id = int(place_id)
    check_access(place_id)
    place = Place.query.get(place_id)
    info = place.to_dict()
    place.delete()
    return jsonify(info)

# TODO types endpoint


if __name__ == '__main__':
    app.run(config.address, port=config.port, debug=config.debug)
