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

'''
CREATE TABLE `my_shares` (
`company` varchar(20) NOT NULL default '',
`shares` int(11) NOT NULL,
`sheets` int(11) NOT NULL,
`other` varchar(20),
`remarks` varchar(50)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

'''
@app.route("/shares", methods=['GET', 'POST'])
def shares():
    if request.method == 'POST':
        company = request.form.get('company')
        shares = request.form.get('shares')
        sheets = request.form.get('sheets')
        other = request.form.get('other')
        remarks = request.form.get('remarks')

        logging.warning ('company: ' + company)
        logging.warning ('shares: ' + shares)
        logging.warning ('sheets ' + sheets)
        logging.warning ('other ' + other)
        logging.warning ('remarks ' + remarks)

        cnx = mysql.connector.connect(user='root',
                                  password='iamwalter',
                                  host='db',
                                  database='shares2')
        cursor = cnx.cursor()

        data_share = (company, shares, sheets, other, remarks)
        add_share = ("INSERT INTO my_shares "
                      "(company, shares, sheets, other, remarks) "
                      "VALUES (%s, %s, %s, %s, %s)")
        cursor.execute(add_share, data_share)
        cnx.commit()

        cursor.close()
        cnx.close()
    
        resp = Response(json.dumps(message.success))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

    else:
        reload(sys)
        sys.setdefaultencoding('utf-8')

        company = request.args.get('company')
        logging.warning ('company: ' + company)

        cnx = mysql.connector.connect(user='root',
                                  password='iamwalter',
                                  host='db',
                                  database='shares2')
        cursor = cnx.cursor()
        query = ("SELECT company, shares, sheets from my_shares where company = '" + company + "'")
        cursor.execute(query)

        for (company, shares, sheets) in cursor:
            logging.warning("data: {}, {}, {}".format(company, shares, sheets))
            message.shares['company'] = company
            message.shares['retshares'] = shares
            message.shares['sheets'] = sheets
            break

        cursor.close()
        cnx.close()

        resp = Response(json.dumps(message.shares))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
