from flask import Flask, jsonify, render_template,request, abort
import os
from flask_cors import CORS
from .models import app, setup_db, db_drop_and_create_all
from .models import User, Posts


@app.route('/blogs', methods=['GET'])
def current_loans():
    loans = Posts.query.all()
    formatted_current_loans = [loan.format() for loan in loans]
    return jsonify({
            'success': True,
            'loans': formatted_current_loans,
            'total_loans':len(formatted_current_loans)
        }),200
    


@main.route('/loan-status/<int:account_number>')
def get_loan_status(account_number):
    # account_number = AccountNumber.query.filter(AccountNumber.account_number == account_number).one_or_none()
    # if account_number is None:
    #     # abort(404)
    #     return {'message': 'Account number not found', 'error_code': '404'}, 404
    # if account_number:
    #     validate_account(account_number)
    loan_status = CurrentLoan.query.filter(CurrentLoan.customer_identifier == account_number and CurrentLoan.loan_identifier == "active").all()
    if len(loan_status) == 0:
        return {'message': 'No loan found', 'error_code': '200'}, 200
    else:
        formatted_outstanding_loans = [loan.format() for loan in loan_status]
        return jsonify({
            'success': True,
            'loans': formatted_outstanding_loans,
            'total_loans':len(formatted_outstanding_loans)
            }),200

@app.route('/new-account-number', methods=['POST'])
def create_account_number():
    body = request.get_json()
    new_account_number = body.get('account_number', None)
    try:
        account_number = AccountNumber(account_number=new_account_number)
        print(account_number)
        account_number.insert()
        
        # selection = AccountNumber.query.order_by(AccountNumber.id).all()
        # account_numbers = paginate_accounts(request, selection)
        
        return jsonify({
                'success': True,
                'created': account_number.id,
                # 'account_numbers': account_numbers,
                'NO of account_numbers': len(AccountNumber.query.all())
            })
    except:
        abort(422)                      



def create_app(app,test_test_config=None):
    app.config['SECRET_KEY']='57324676734hjvbedhjewr9pp942312y89r321g8t7'
    with app.app_context():
        setup_db(app)
        CORS(app)
        db_drop_and_create_all() 
    return app
    
APP=create_app(app)

if __name__=="__main__":
    port= int(os.environ.get("PORT",5000))
    APP.run(host='127.0.0.1',port=port,debug=True)

    