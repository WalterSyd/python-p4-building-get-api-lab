#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'


#View to get all bakeries
@app.route('/bakeries')
def bakeries():
    bakeries=[]
    #unpacks individual bakeries in the bakeries db &
    #appends each bakery to the bakeries list
    for b in Bakery.query.all():
        b_dict = b.to_dict()
        bakeries.append(b_dict)
    response = make_response(bakeries,
                            200,
                            {'Content-Type': 'application/json'}
                        )
    return response

#View to get a single bakery with its baked goods
@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    #Returns a single bakery as JSON with its baked goods nested in a list
    bakery = Bakery.query.filter(Bakery.id == id).first()
    bakery_dict = bakery.to_dict()
    #unpacks baked goods in each bakery into a list
    baked_goods = []
    for b in bakery.baked_goods:
        b_dict = b.to_dict()
        baked_goods.append(b_dict)
    bakery_dict['baked_goods'] = baked_goods


    response = make_response(bakery_dict,
                            200,
                            {'Content-Type': 'application/json'}
                        )
    return response

#View to get all baked goods by price
@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = []
    #Loop through all baked goods and append them to the list individually after ordering them by price
    for b in BakedGood.query.order_by(BakedGood.price.desc()).all():
        b_dict = b.to_dict()
        baked_goods_by_price.append(b_dict)

    response = make_response(baked_goods_by_price,
                            200,
                            {'Content-Type': 'application/json'}
                        )
    return response
    

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    #sorting through the baked goods to find the most expensive baked good by price and limiting it by first
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    baked_good_dict = baked_good.to_dict()
    response = make_response(baked_good_dict,
                            200,
                            {'Content-Type': 'application/json'}
                        )
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
