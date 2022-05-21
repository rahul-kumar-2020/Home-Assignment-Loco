from flask import Flask 
from flask import request,jsonify
import jaydebeapi
import mysql.connector
import json 

app = Flask(__name__)

### Transaction Objects 
class Transaction_object:
   def __init__(self, transaction_id, amount, type, parent_id):
     self.transaction_id = transaction_id
     self.amount = amount
     self.type = type
     self.parent_id = parent_id
     self.total_amount = amount


class Transaction_database:
      transaction_id_dict = {}
      transaction_type_dict = {}

      def update_sum_transitively(self, transaction_id, amount_to_add):
         transObj = self.transaction_id_dict[transaction_id]
          
         while(transObj.parent_id != -1):
            transObj = self.transaction_id_dict[transObj.parent_id]
            transObj.total_amount = transObj.total_amount + amount_to_add
            self.transaction_id_dict[transObj.transaction_id] = transObj   


      def insert_transaction(self, transObj):
         transaction_id = transObj.transaction_id
         type = transObj.type

         if( transObj.parent_id != -1 and transObj.parent_id not in self.transaction_id_dict):
             return f"Error : Invalid transaction, parent_id : {transObj.parent_id} doesn't exist in database"  

         if transaction_id not in self.transaction_id_dict:
            self.transaction_id_dict[transaction_id] = transObj
          
            types_list = self.transaction_type_dict.get(type, [])
            types_list.append(transaction_id)
            self.transaction_type_dict[transObj.type] = types_list
            
            ## Update sum in parents
            self.update_sum_transitively(transaction_id, transObj.amount)   

            return "success"   
         else: 
            return f"Error : Transaction Id : {transaction_id} already exists in Db"        


      def fetch_transaction_by_id(self, transaction_id):
          response = {}

          if transaction_id in self.transaction_id_dict:
            trans_obj = self.transaction_id_dict[transaction_id]
            response = {
               "amount" : trans_obj.amount,
               "type" : trans_obj.type,
               "parent_id" : trans_obj.parent_id
            }
          return response

      def fetch_transactions_by_type(self, type):
          return self.transaction_type_dict.get(type,[])    

      def fetch_transaction_sum_by_id(self, transaction_id):
          if transaction_id in self.transaction_id_dict:
             return  self.transaction_id_dict[transaction_id].total_amount
          else:
             return {}     


transaction_db = Transaction_database()

## Server Flow 
@app.route('/transactionservice/transaction/<transaction_id>', methods=['PUT'])
def insert_transaction(transaction_id):
      try: 
         parent_id = -1
         amount = request.json['amount']
         type = request.json['type']

         if 'parent_id' in request.json:
            parent_id = request.json['parent_id']

         trans_obj = Transaction_object(int(transaction_id), amount, type, parent_id)      
         response = transaction_db.insert_transaction(trans_obj)
         
         if(response == "success"):
               response = { "status": "ok" }

         json_response = str(json.dumps(response))
         return json_response, 200

      except Exception as ex:
         return f"There was an error on the server and the request could not be completed : {ex}", 500


@app.route('/transactionservice/transaction/<transaction_id>', methods=['GET'])
def fetch_transaction_by_id_call(transaction_id):  
   try: 
      response = transaction_db.fetch_transaction_by_id(int(transaction_id))
      json_response = str(json.dumps(response))
      return json_response, 200   

   except Exception as ex:
      return f"There was an error on the server and the request could not be completed : {ex}", 500


@app.route('/transactionservice/types/<type>', methods=['GET'])
def fetch_transactions_by_type_call(type):  
   try: 
      response = transaction_db.fetch_transactions_by_type(type)
      json_response = str(json.dumps(response))
      return json_response, 200   

   except Exception as ex:
      return f"There was an error on the server and the request could not be completed : {ex}", 500



@app.route('/transactionservice/sum/<transaction_id>', methods=['GET'])
def fetch_transaction_sum_by_id_call(transaction_id):  
   try: 
      response = transaction_db.fetch_transaction_sum_by_id(int(transaction_id))
      json_response = str(json.dumps(response))
      return json_response, 200

   except Exception as ex:
      return f"There was an error on the server and the request could not be completed : {ex}", 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

