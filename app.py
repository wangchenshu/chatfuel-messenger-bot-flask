#-*- coding: utf-8 -*-
import sys
import mysql.connector

from flask import Flask
from flask import request
from flask import jsonify
from flask import Response

import logging
import json
import message

app = Flask(__name__)

@app.route("/shares", methods=['GET', 'POST'])
def shares():
    if request.method == 'POST':
        logging.warning (request.form)
        reload(sys)
        sys.setdefaultencoding('utf-8')

        try:
            options = request.form.get('options')
            name = request.form.get('name')
            shares = request.form.get('shares')
            sheets = request.form.get('sheets')
            get_number = request.form.get('get_number')
            get_item = request.form.get('get_item')
            remarks = request.form.get('remarks')

            logging.warning('options: ' + options)
            logging.warning ('name: ' + name)
            logging.warning ('shares: ' + shares)
            logging.warning ('sheets ' + sheets)
            logging.warning ('get_number ' + get_number)
            logging.warning ('get_item ' + get_item)
            logging.warning ('remarks ' + remarks)

            cnx = mysql.connector.connect(user='root',
                                password='iamwalter',
                                host='db',
                                database='home')

            cursor = cnx.cursor()

            query = ("SELECT serial, company, date FROM request WHERE " + options + " = '" + name + "'")
            logging.warning(query)
            cursor.execute(query)
            for (serial, company, date) in cursor:
                logging.warning("data: {}, {}, {}".format(serial, company, date))
                insert_serial = serial
                insert_company = company
                insert_date = date

            add_share = ("INSERT INTO shares "
                        "(serial, company, date, shares, sheets, get_number, get_item, remarks) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ")
            data_share = (serial, company, date, shares, sheets, get_number, get_item, remarks)
            
            logging.warning(add_share)
            cursor.execute(add_share, data_share)
            cnx.commit()

            cursor.close()
            cnx.close()
        
            resp = Response(json.dumps(message.success))
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        except Exception, ex:
            logging.error(str(ex))

    else:
        reload(sys)
        sys.setdefaultencoding('utf-8')

        try:
            company = request.args.get('company')
            logging.warning ('company: ' + company)

            cnx = mysql.connector.connect(user='root',
                                password='iamwalter',
                                host='db',
                                database='home')

            cursor = cnx.cursor()
            # SELECT r.serial, r.date, s.shares, s.sheets FROM shares s, request r WHERE s.company = '大同' AND r.company = '大同'
            query = ("SELECT r.company, r.serial, r.date, s.shares, s.sheets FROM shares s, request r WHERE s.company = '" + company + "' AND r.company = '" + company +  "'")
            cursor.execute(query)

            ret_shares = 0
            ret_sheets = 0
            
            for (company, serial, date, shares, sheets) in cursor:
                logging.warning("data: {}, {}, {}, {}, {}".format(company, shares, sheets, date, serial))
                ret_shares += shares
                ret_sheets += sheets
                message.shares['company'] = company
                message.shares['serial'] = serial
                message.shares['date'] = date
                message.shares['retshares'] = ret_shares
                message.shares['sheets'] = ret_sheets

            cursor.close()
            cnx.close()

            resp = Response(json.dumps(message.shares))
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        except Exception, ex:
            logging.error(str(ex))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
