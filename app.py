#----------------------------------------------------------------------------#
# Pacakges import
#----------------------------------------------------------------------------#
import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import func
from models import setup_db, Drink, Transaction, db
from flask_cors import CORS
import datetime
import json
from auth import AuthError, requires_auth


def create_app(test_config=None):
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

#----------------------------------------------------------------------------#
# Drinks routes
#----------------------------------------------------------------------------#
    @app.route('/drinks')
    def get_drinks():
        drinks=Drink.query.all()
        drinks_formatted=[d.format() for d in drinks]
        return jsonify({
            "success":True,
            "drinks":drinks_formatted
        })
    
    @app.route('/drinks',methods=["POST"])
    @requires_auth('post:drinks')
    def add_drinks(payload):
        body = request.get_json()
        new_name = body.get('name')
        new_price = body.get('price')
        new_quantity=body.get('quantity')
        if new_name is None or new_price is None or new_quantity is None:
            abort(400)
        try: 
            drink = Drink(new_name,new_price,new_quantity)
            drink.insert()
            return jsonify({
                "success":True
            })
        except:
            abort(422)

    @app.route('/drinks/<int:id>', methods=["PATCH"])
    @requires_auth('patch:drinks')
    def drinks_patch(payload,id):
        drink = Drink.query.get(id)        
        if drink is None:
            abort(404)

        try:
            body = request.get_json()
            new_name = body.get('name')
            new_price = body.get('price')
            new_quantity=body.get('quantity')
            if new_name is not None:
                drink.name=new_name
            if new_price is not None:
                drink.price=new_price
            if new_quantity is not None:
                drink.quantity=new_quantity
            drink.update()

            return jsonify({
                'success': True,
                'drink': drink.format()
            })
        except:
            abort(422)
        

    @app.route('/drinks/<int:id>', methods=["DELETE"])
    @requires_auth('delete:drinks')
    def drinks_delete(payload,id):
        drink = Drink.query.get(id)
        if drink is None:
            abort(404)

        try:
            drink.delete()
            return jsonify({
                'success': True,
                'delete': id
            })
        except:
            abort(422)

#----------------------------------------------------------------------------#
# Transaction routes
#----------------------------------------------------------------------------#
    @app.route('/transactions')
    @requires_auth('get:transactions')
    def tansaction_history(payload):
        trans=Transaction.query.order_by(Transaction.created_at).all()
        trans_formatted=[t.format() for t in trans]
        return jsonify({
            'success':True,
            'history':trans_formatted
        })

    @app.route('/transactions',methods=["POST"])
    @requires_auth('post:transactions')
    def transaction_create(payload):
        body = request.get_json()
        new_drink_id = body.get('drink_id')
        new_quantity=body.get('quantity')  
        new_created_at=body.get('created_at')     
        
        # check input
        if new_drink_id is None or new_quantity is None or new_created_at is None:
            abort(400)
        drink=Drink.query.get(new_drink_id)
        if drink is None or drink.quantity<new_quantity:
            abort(400)
        
    
        t=datetime.datetime.strptime(new_created_at,"%Y-%m-%d")
        trans=Transaction(new_drink_id,new_quantity,t)
        trans.insert()

        drink.quantity-=new_quantity
        drink.update()

        return jsonify({
            'success':True,
            'transaction':trans.format(),
            'drink':drink.name
        })


    @app.route('/transactions',methods=["PATCH"])
    @requires_auth('patch:transactions') 
    def transaction_update(payload):
        body = request.get_json()
        trans_id=body.get('trans_id')
        new_drink_id = body.get('drink_id')
        new_quantity=body.get('quantity')  
        new_created_at=body.get('created_at')     
        
        # check input
        if trans_id is None:
            abort(400)
        trans=Transaction.query.get(trans_id)
        if trans is None: 
            abort(400)

        # revoke old changes to drink quantity
        trans.drink.quantity+=trans.quantity
        trans.drink.update()
        # update transacation
        if new_drink_id is not None:
            trans.drink_id=new_drink_id
        if new_quantity is not None:
            trans.quantity=new_quantity
        if new_created_at is not None:
            trans.created_at=datetime.datetime.strptime(new_created_at,"%Y-%m-%d")
        trans.update()
        trans.drink.quantity-=trans.quantity
        trans.drink.update()

        return jsonify({
            'success':True,
            'transaction':trans.format(),
            'drink':trans.drink.name            
        })

    @app.route('/transactions',methods=["DELETE"])
    @requires_auth('delete:transactions') 
    def transaction_delete():
        body = request.get_json()
        trans_id=body.get('trans_id') 
        
        # check input
        if trans_id is None:
            abort(400)
        trans=Transaction.query.get(trans_id)
        if trans is None: 
            abort(400)

        # revoke old changes to drink quantity
        trans.drink.quantity+=trans.quantity
        trans.drink.update()

        # delete trans
        trans.delete()
        return jsonify({
            'success':True,
            'transaction_id':trans_id        
        })



    @app.route('/transactions/popular')
    def get_popular_drinks():
        trans=db.session.query(Transaction.drink_id,func.count(Transaction.id).label('total')).group_by(Transaction.drink_id).order_by(db.desc('total')).limit(5).all()
        output_formatted=[]
        for t in trans:
            data={}
            data['sales']=t[1]
            data['drink_id']=t[0]
            output_formatted.append(data)

        return jsonify({
            'success':True,
            'toplist':output_formatted
        }) 
#----------------------------------------------------------------------------#
# Error handling
#----------------------------------------------------------------------------#
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404


    @app.errorhandler(400)
    def badrequest(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400


    @app.errorhandler(405)
    def methodnotallow(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405


    @app.errorhandler(401)
    def authentication(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "authentication error"
        }), 401


    @app.errorhandler(403)
    def permission(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "no permission"
        }), 403


    

    return app

app = create_app()

if __name__ == '__main__':
    app.run()