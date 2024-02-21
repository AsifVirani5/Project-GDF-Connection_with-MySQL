from flask import Flask, request, jsonify
import json
import mysql.connector

with open('config.json') as file:
    params = json.load(file)['params']

app = Flask(__name__)

@app.route("/webhook", methods = ["POST", "GET"])
def dialogflow_MySql_Connection():
    req = request.get_json(force = True)
    user_query = req["queryResult"]["queryText"]
    parameters = req["queryResult"]["parameters"]
    card_type = parameters.get["cardtype"]
    card_brand = parameters.get["cardbrand"]
    card_number = parameters.get["cardnumber"]
    card_expiry_date = parameters.get["cardexpirydate"] 
    cvv = parameters.get["CVV"]
    given_name = parameters.get["givenname"]
    Last_name = parameters.get["lastname"]
    data = { "user_query": user_query,
              "cardtype" : card_type,
              "cardbrand" : card_brand,
              "cardnumber" : card_number,
              "cardexpirydate" : card_expiry_date,
              "cvv" : cvv,
              "givenname" : given_name,
              "lastname" : Last_name         
    }
 
     # Establish the connection
    cnx = mysql.connector.connect(user=params['Username'], 
                                  password=params['Password'],
                                  host=params['Hostname'],
                                  port=params['Port'])

    cursor = cnx.cursor()

    # Create database
    cursor.execute(
        "CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8'".format(params['database'])
    )
    
    # Select the database
    cnx.database = params['database']

    # Create table
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `viranis-transient-business-data`("
        "`user_query` VARCHAR(255), "
        "`cardtype` VARCHAR(255), "
        "`cardbrand` VARCHAR(255), "
        "`cardnumber` VARCHAR(255), "
        "`cardexpirydate` VARCHAR(255), "
        "`cvv` VARCHAR(255), "
        "`givenname` VARCHAR(255), "
        "`lastname` VARCHAR(255)"
        ")"
    )

    # Insert data into table
    cursor.execute(
        "INSERT INTO `viranis-transient-business-data` ("
        "`user_query`, `cardtype`, `cardbrand`, `cardnumber`, `cardexpirydate`, `cvv`, `givenname`, `lastname`"
        ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (user_query, card_type, card_brand, card_number, card_expiry_date, cvv, given_name, Last_name)
    )

    cnx.commit()

    return jsonify(data), 200

if __name__ == "__main__":
        app.run()    
