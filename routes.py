from flask import Blueprint, jsonify, request
from models import Hero, Power, HeroPower, db

api = Blueprint("api", __name__)

# HEROES ROUTES
@api.route("/heroes", methods=["GET"])
def get_heroes():
    heroes = Hero.query.all()
    result = [hero.to_dict(only=("id", "name", "super_name")) for hero in heroes]
    return jsonify(result), 200


@api.route("/heroes/<int:id>", methods=["GET"])
def get_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404

    hero_dict = hero.to_dict()
    hero_dict["hero_powers"] = []

    for hp in hero.hero_powers:
        hero_dict["hero_powers"].append({
            "id": hp.id,
            "hero_id": hp.hero_id,
            "power_id": hp.power_id,
            "strength": hp.strength,
            "power": {
                "id": hp.power.id,
                "name": hp.power.name,
                "description": hp.power.description
            }
        })

    return jsonify(hero_dict), 200

# POWERS ROUTES
@api.route("/powers", methods=["GET"])
def get_powers():
    powers = Power.query.all()
    return jsonify([power.to_dict() for power in powers]), 200


@api.route("/powers/<int:id>", methods=["GET"])
def get_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404
    return jsonify(power.to_dict()), 200


@api.route("/powers/<int:id>", methods=["PATCH"])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    data = request.get_json()
    description = data.get("description")

    try:
        power.description = description  # triggers validation in model
        db.session.commit()
        return jsonify(power.to_dict()), 200
    except Exception as e:
        return jsonify({"errors": [str(e)]}), 400

# HEROPOWERS ROUTE

@api.route("/hero_powers", methods=["POST"])
def create_hero_power():
    data = request.get_json()
    hero_id = data.get("hero_id")
    power_id = data.get("power_id")
    strength = data.get("strength")

    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)

    errors = []

    if not hero:
        errors.append("Hero not found")
    if not power:
        errors.append("Power not found")
    if strength not in ["Strong", "Weak", "Average"]:
        errors.append("Strength must be Strong, Weak, or Average")

    if errors:
        return jsonify({"errors": errors}), 400

    try:
        hero_power = HeroPower(hero_id=hero_id, power_id=power_id, strength=strength)
        db.session.add(hero_power)
        db.session.commit()
        return jsonify({
            "id": hero_power.id,
            "hero_id": hero_power.hero_id,
            "power_id": hero_power.power_id,
            "strength": hero_power.strength,
            "hero": hero.to_dict(only=("id", "name", "super_name")),
            "power": power.to_dict()
        }), 201
    except Exception as e:
        return jsonify({"errors": [str(e)]}), 400
