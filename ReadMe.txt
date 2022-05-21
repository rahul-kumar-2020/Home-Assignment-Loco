#########################################################
Name : Rahul Lahane
Mob : 8830609624
Project - Loco Home Assignment Test
#########################################################


Overview:
Have prepared two solution for it, 
1. One which uses the mysql database for storing data -> loco_sol_with_db.py
2. One which uses in-memory approach -> loco_sol_with_class.py

Have created one file for testing the setup, which fires no of requests for each of the feature and shows the result in console

REQUIREMENT : 
  1. loco_sol_with_db.py -> Python3, Flask, python-mysql-connector, python-requests module
  2. loco_sol_with_class.py -> Python3, Flask
  3. request_calls.py -> Python3, python-requests module


HOW TO RUN : 
  python3 <file-name>
  ex python3 loco_sol_with_db.py
  	 python3 request_calls.py



Assumption:
1. The API is read intensive
2. transaction can't be inserted before its parent transaction is inserted.

Approach : 
A. loco_sol_with_db(using mysql database)
	1. Have made the solution keeping in view the app is going to be READ intensive, hence the latency of read should be low as much as possible.
	2. Have added a new column, other than the transaction parameters -> "total_amount", which will have the total sum, i.e the sum of the transaction and all of its child transaction.
	3. During the insert operation, a stored procedure has been used, code of which has been attached in file mysql_query_sp.txt. The SP first inserts the transaction and then iteratively find out the transaction_ids which are its parent, at last it adds the sum of current transaction in all of its parent.
	4. Other operations are straight-forward query from the Dbs.


B. loco_sol_with_class(in-memory)
	1. Have made the solution keeping in view the app is going to be READ intensive, hence the latency of read should be low as much as possible.
	2. Have created two class, "Transaction_object" -> to store the transaction meta data, and another "Transaction_database" -> which stores the transaction objects and acts as a database and exposes various functions for the required case.
	3. Like in previous case, maintaining one additional variable in transaction object "total_amount", which stores the final sum i.e the sum of the transaction and all of its child transaction.
	4. During insert operation only, the method "update_sum_transitively" will be called to update the respective parents sum.
	5. Other operations are straight-forward filter from dictionary.


