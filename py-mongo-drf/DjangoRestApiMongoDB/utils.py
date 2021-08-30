from pymongo import MongoClient


def get_db_handle(db_name, host, port, username, password):

#  client = MongoClient(host=host,
#                       port=int(port),
#                       username=username,
#                       password=password
#                      )

   client = MongoClient("mongodb://mongouser:password@localhost/boot_mongodb")
   db_handle = client['boot_mongodb']
 
   return db_handle, client