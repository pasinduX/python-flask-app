from flask import Blueprint,request,jsonify
from bson.objectid import ObjectId
from app.models import get_user_collection


crud_blueprint = Blueprint("crud", __name__)


users=get_user_collection();

@crud_blueprint.route("/users",methods=["POST"])
def create_user():
    data=request.json
    if not data.get("name")or not data.get("email"):
        return jsonify({"error":"Missing required fields"}),400
    
    result=users.insert_one(data)
    return jsonify({"message":"user_created","id":str(result.inserted_id)}),200

@crud_blueprint.route("/users/<user_id>",methods=["DELETE"])
def delete_user(user_id):
    result=users.delete_one({"_id":ObjectId(user_id)})
    if result.deleted_count==0:
        return jsonify({"error:":"user Not found"}),404
    return jsonify({"message":"user deleted"}),200


@crud_blueprint.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    updated_user = users.find_one_and_update(
        {"_id": ObjectId(user_id)},
        {"$set": data},
        return_document=True
    )
    if not updated_user:
        return jsonify({"error": "User not found"}), 404
    updated_user["_id"] = str(updated_user["_id"])
    return jsonify({"message": "User updated", "user": updated_user}), 200


@crud_blueprint.route("/users/<user_id>",methods=["GET"])
def get_user(user_id):
    user=users.find_one({"_id":ObjectId(user_id)})
    if not user:
        return jsonify({"error":"user not found"}),404
    user["_id"] = str(user["_id"])
    return jsonify(user), 200 


@crud_blueprint.route("/users", methods=["GET"])
def get_users():
    user_list = list(users.find())
    for user in user_list:
        user["_id"] = str(user["_id"]) 
    return jsonify(user_list), 200


