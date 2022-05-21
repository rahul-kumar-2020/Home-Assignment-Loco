import requests


trans_id_map = {}
trans_id_map[1] = {"amount": 100, "type" : "cars"}
trans_id_map[2] = {"amount": 100, "type" : "cars", "parent_id" : 1}
trans_id_map[3] = {"amount": 100, "type" : "cars", "parent_id" : 1}
trans_id_map[4] = {"amount": 100, "type" : "cars", "parent_id" : 2}
trans_id_map[5] = {"amount": 100, "type" : "bikes", "parent_id" : 2}
trans_id_map[6] = {"amount": 100, "type" : "shopping", "parent_id" : 3}
trans_id_map[7] = {"amount": 100, "type" : "bikes", "parent_id" : 6}
trans_id_map[8] = {"amount": 100, "type" : "shopping", "parent_id" : 4}
trans_id_map[9] = {"amount": 100, "type" : "shopping", "parent_id" : 1}
trans_id_map[10] = {"amount": 100, "type" : "shopping", "parent_id" : -1}


trans_id_list = [1,2,3,4,5,6,7,8,9,10]

print("--------------Inserting transaction Ids--------------")
for transaction_id in trans_id_list:
		response = requests.put(f"http://0.0.0.0:8080/transactionservice/transaction/{transaction_id}", json = trans_id_map[transaction_id])
		print(f"transaction_id : {transaction_id},  data : {trans_id_map[transaction_id]},  response : {response.text}")


print("\n\n--------------fetch transaction ids data--------------")
for transaction_id in trans_id_list:
		response = requests.get(f"http://0.0.0.0:8080/transactionservice/transaction/{transaction_id}")
		print(f"transaction_id : {transaction_id},  response : {response.text}")


print("\n\n--------------fetch transaction types data--------------")
types_list = ["cars", "shopping", "bikes"]
for type in types_list:
		response = requests.get(f"http://0.0.0.0:8080/transactionservice/types/{type}")
		print(f"type : {type},  response : {response.text}")


print("\n\n--------------fetch transaction sum data--------------")
for transaction_id in trans_id_list:
		response = requests.get(f"http://0.0.0.0:8080/transactionservice/sum/{transaction_id}")
		print(f"transaction_id : {transaction_id},  sum : {response.text}")