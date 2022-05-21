from flask import Flask 
from flask import request,jsonify
import jaydebeapi
import mysql.connector
import json 

##mysql connection
#conn = mysql.connector.connect(host="127.0.01",port="3306",user="root",password="",database="locoTest")(
conn = mysql.connector.connect(host="sql6.freemysqlhosting.net",port="3306",user="sql6493629",password="udCwjeHfpb",database="sql6493629")
app = Flask(__name__)


'''
Inserts the Data into table, calls a stored procedure to execute the insert and update in total_amount
'''
@app.route('/transactionservice/transaction/<transaction_id>', methods=['PUT'])
def insert_transaction(transaction_id):
   try: 
         parent_id = -1
         amount = request.json['amount']
         type = request.json['type']
         cursor = conn.cursor()

         if 'parent_id' in request.json:
            parent_id = request.json['parent_id']

            # check if parent_id exists in db or not
            if parent_id != -1:
               sql_query = f"SELECT transaction_id FROM transactionsTable where transaction_id = {parent_id}"
               cursor.execute(sql_query)
               result = cursor.fetchall()
               if(len(result)==0):
                 return f"Error : Invalid transaction, parent_id : {parent_id} doesn't exist in database", 500 
            
         args = [transaction_id, amount, type, parent_id]
         result = cursor.callproc('InsertTransaction', args)
         response = { "status": "ok" }  
         json_response = str(json.dumps(response))

         cursor.close()
         conn.commit()
          
         return json_response, 200

   except Exception as ex:
        return f"There was an error on the server and the request could not be completed : {ex}", 500



'''
Fetches data w.r.t transaction_id 
'''
@app.route('/transactionservice/transaction/<transaction_id>', methods=['GET'])
def fetch_transaction_by_id(transaction_id):  
   try: 
      sql_query = f"SELECT * FROM transactionsTable where transaction_id = {transaction_id}"

      cursor = conn.cursor()
      cursor.execute(sql_query)
      result_tuple = cursor.fetchall()

      log = {}
      for result in result_tuple:
         log = {
         "amount" : result[1],
         "type" : result[2],
         "parent_id" : result[3]
         }
      
      json_response = str(json.dumps(log))
      cursor.close()

      return json_response, 200   

   except Exception as ex:
      return f"There was an error on the server and the request could not be completed : {ex}", 500


'''
Fetches data w.r.t type 
'''
@app.route('/transactionservice/types/<type>', methods=['GET'])
def fetch_transactions_by_type(type):  
   try: 
      sql_query = f"SELECT transaction_id FROM transactionsTable where type = '{type}'"
      
      cursor = conn.cursor()
      cursor.execute(sql_query)
      result_tuple = cursor.fetchall()
        
      types_list = []
      for result in result_tuple:
         types_list.append(result[0])

      json_response = str(json.dumps(types_list))
      cursor.close()

      return json_response, 200   

   except Exception as ex:
      return f"There was an error on the server and the request could not be completed : {ex}", 500


'''
Fetches sum w.r.t transaction_id
'''
@app.route('/transactionservice/sum/<transaction_id>', methods=['GET'])
def fetch_transaction_sum_by_id(transaction_id):  
   try: 
      sql = f"SELECT total_amount FROM transactionsTable where transaction_id = '{transaction_id}'"
      
      cursor = conn.cursor()
      cursor.execute(sql)
      result_tuple = cursor.fetchall()

      response = {}
      for result in result_tuple:
          response= {"sum":result[0]}

      json_response = str(json.dumps(response))
      cursor.close()

      return json_response, 200

   except Exception as ex:
      return f"There was an error on the server and the request could not be completed : {ex}", 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)