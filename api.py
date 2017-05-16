from flask import Flask
from flask import request
from flask import jsonify
from dokuwiki import DokuWiki, DokuWikiError
from datetime import datetime

import message

app = Flask(__name__)

@app.route("/register", methods=['POST'])
def register():
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    url_str = 'http://new.hackingthursday.org/dokuwiki/%d%02d%02d' % (year, month, day)
    
    '''
    try:
        wiki = DokuWiki(url_str, 'USER', 'PASSWORD')
    except (DokuWikiError, Exception) as err:
        print('unable to connect: %s' % err
    '''

    chatfuel_user_id = request.form['chatfuel user id']
    first_name = request.form['first name']
    last_name = request.form['last name']

    print ("chatfuel_user_id: " + chatfuel_user_id)
    print ("first_name: " + first_name)
    print ("last_name: " + last_name)
    
    return ""
    #return jsonify(message.welcome)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)