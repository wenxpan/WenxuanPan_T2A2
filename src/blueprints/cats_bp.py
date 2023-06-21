from flask import Blueprint
from init import db
from models.cat import Cat, CatSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from blueprints.auth_bp import admin_required, admin_or_owner_required
from flask import request


cats_bp = Blueprint('cat', __name__, url_prefix='/cats')


@cats_bp.route('/')
def all_cats():
    stmt = db.select(Cat)
    cats = db.session.scalars(stmt)
    return CatSchema(many=True).dump(cats)


@cats_bp.route('/', methods=['POST'])
@jwt_required()
def create_cat():
    user_id = get_jwt_identity()
    cat_info = CatSchema().load(request.json)
    cat = Cat(
        name=cat_info['name'],
        year_born=cat_info['year_born'],
        year_adopted=cat_info['year_adopted'],
        breed=cat_info['breed'],
        owner_id=user_id
    )
    db.session.add(cat)
    db.session.commit()
    return CatSchema().dump(cat), 201


@cats_bp.route('/<int:cat_id>')
def get_one_cat(cat_id):
    stmt = db.select(Cat).filter_by(id=cat_id)
    cat = db.session.scalar(stmt)
    if cat:
        return CatSchema().dump(cat)
    else:
        return {'error': 'Cat not found'}, 404


@cats_bp.route('/<int:cat_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_cat(cat_id):
    stmt = db.select(Cat).filter_by(id=cat_id)
    cat = db.session.scalar(stmt)
    owner_id = cat.owner.id
    cat_info = CatSchema().load(request.json)
    if cat:
        admin_or_owner_required(owner_id)
        cat.name = cat_info.get('name', cat.name)
        cat.year_born = cat_info.get('year_born', cat.year_born)
        cat.year_adopted = cat_info.get('year_adopted', cat.year_adopted)
        cat.breed = cat_info.get('breed', cat.breed)
        db.session.commit()
        return CatSchema(exclude=['notes']).dump(cat)
    else:
        return {'error': 'Cat not found'}, 404


@cats_bp.route('/<int:cat_id>', methods=['DELETE'])
@jwt_required()
def delete_cat(cat_id):
    stmt = db.select(Cat).filter_by(id=cat_id)
    cat = db.session.scalar(stmt)
    owner_id = cat.owner.id
    if cat:
        admin_or_owner_required(owner_id)
        db.session.delete(cat)
        db.session.commit()
        return {}, 200
    else:
        return {'error': 'Cat not found'}, 404