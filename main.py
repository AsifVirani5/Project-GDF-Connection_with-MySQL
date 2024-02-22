from flask import Flask, request, jsonify
import json
import mysql.connector
'''from flask_ngrok import run_with_ngrok'''

with open('config.json') as file:
    params = json.load(file)['params']

app = Flask(__name__)
'''run_with_ngrok(app)'''

@app.route("/webhook", methods = ["POST", "GET"])
def dialogflow_MySql_Connection():
    try:
        req = request.get_json(force = True)
        user_query = req["queryResult"]["queryText"]
        parameters = req["queryResult"]["parameters"]
        card_type = parameters.get("cardtype")
        card_brand = parameters.get("cardbrand")
        card_number = parameters.get("cardnumber")
        card_expiry_date = parameters.get("cardexpirydate")
        cvv = parameters.get("CVV")
        given_name = parameters.get("givenname")
        Last_name = parameters.get("lastname")
        data = { 
            "user_query": user_query,
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
            "CREATE DATABASE IF NOT EXISTS ViranisTransientBusiness")
        
        
        # Select the database
        cnx.database = params['Database']

        # Create table
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS `viranistransientbusinessdata`("
            "`user_query` VARCHAR(350), "
            "`cardtype` VARCHAR(255), "
            "`cardbrand` VARCHAR(255), "
            "`cardnumber` INT(16), "
            "`cardexpirydate` VARCHAR(255), "
            "`cvv` INT(7), "
            "`givenname` VARCHAR(255), "
            "`lastname` VARCHAR(255)"
            ")"
        )

        # Insert data into table
        cursor.execute(
            "INSERT INTO `viranistransientbusinessdata` ("
            "`user_query`, `cardtype`, `cardbrand`, `cardnumber`, `cardexpirydate`, `cvv`, `givenname`, `lastname`"
            ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (user_query, card_type, card_brand, card_number, card_expiry_date, cvv, given_name, Last_name)
        )

        cnx.commit()

        # Prepare the response for Dialogflow
        dialogflow_response = {
            "fulfillmentText": "Data has been stored successfully."
        }

        return jsonify(dialogflow_response), 200

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()






'''from flask import Flask, request, jsonify
import json
import mysql.connector

with open('config.json') as file:
    params = json.load(file)['params']

app = Flask(__name__)

@app.route("/webhook", methods = ["POST"])
def dialogflow_MySql_Connection():
    try:
        req = request.get_json(force = True)
        user_query = req["queryResult"]["queryText"]
        parameters = req["queryResult"]["parameters"]
        card_type = parameters.get("cardtype")
        card_brand = parameters.get("cardbrand")
        card_number = parameters.get("cardnumber")
        card_expiry_date = parameters.get("cardexpirydate")
        cvv = parameters.get("CVV")
        given_name = parameters.get("givenname")
        Last_name = parameters.get("lastname")
        data = { 
            "user_query": user_query,
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
            "CREATE DATABASE IF NOT EXISTS Viranis-Transient-Business")
        
        
        # Select the database
        #cnx.database = params['database']

        # Create table
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS `viranis-transient-business-data`("
            "`user_query` VARCHAR(350), "
            "`cardtype` VARCHAR(255), "
            "`cardbrand` VARCHAR(255), "
            "`cardnumber` INT(16), "
            "`cardexpirydate` VARCHAR(255), "
            "`cvv` INT(7), "
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

        # Prepare the response for Dialogflow
        dialogflow_response = {
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            "Data has been stored successfully."
                        ]
                    }
                }
            ]
        }

        return jsonify(dialogflow_response), 200

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()'''
