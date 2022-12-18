from __main__ import app

from flask import request, render_template

from data import *
from db_resource import get_trans_data
from utils import generate_trans_data, writer, generate_exception_data, cleaner


@app.route('/HttpServices/api/inner/<tran_id>', methods=['GET', 'POST'])
def create_inner_data(tran_id):
    resp = {'message': 'inner data created'}
    cleaner()

    data = get_trans_data(tran_id)
    print(f'TransactionData: {data}')

    code = request.get_json().get('code')
    print(f'TransactionCode: {code}')

    data_trans = generate_trans_data(data)
    writer(data_trans, filename='trans.json')

    exception_data = generate_exception_data(data, code)
    writer(exception_data, filename='exceptions.json')

    return resp, 200


@app.route('/HttpServices/api/<exceptions>', methods=['GET', 'POST'])
def get_exeption(exceptions):
    return render_template('exceptions.json')
    # return exept


@app.route('/HttpServices/api/exceptions/id/<exceptions>', methods=['GET', 'POST'])
def get_exeption_id(exceptions):
    return render_template('exception.json')
    # return exept


@app.route('/HttpServices/api/transactions/id/<tran_id>', methods=['GET', 'POST'])
def get_trans(tran_id):
    return render_template('trans.json')
    # return trans
