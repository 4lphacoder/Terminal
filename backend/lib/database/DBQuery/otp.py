from pymongo import MongoClient
from logger import log
import config

class OTP:
    def __init__(self):
        try:
            self.client = MongoClient(config.MongoDB_URI)
            db = self.client[config.OTP_DB]
            log(f'[  INFO  ] {config.OTP_DB} Connected Successfully')
        except:
            log(f'[  ERROR ] Unable To Create Connection With {config.OTP_DB}')
        self.collection = db[config.OTP_COLLECTION]

    def insert(self,hash_id,otp,function):
		# USED TO INSERT OTP FOR A PARTICULAR USERID 
		# ---------------------------------------------------------------------------
		# DATA STRUCTURES OF ENROLLED_STUDENTS :-
		# HASH_ID --> STRING
		# OTP --> INTEGER
        # FUNCTION --> STRING
        #
        # CHECKING THE PRESENCE OF DUPLICATE ENTRY IN DATABASE
        try:
            res = self.collection.find({ 'hash_id': hash_id })
            if res.count() > 0:
                ## CHECKING WHETHER SAME FUNCTIONALITY EXISTS IN THE DUPLICATE RESULTS
                for document in res:
                    if document['function'] == function :
                        log(f'[  INFO  ] For Hash ID - {hash_id} Duplicate Entry Found at {config.OTP_COLLECTION} Collection in {config.OTP_DB}')
                        status = self.collection.delete_one({ 'hash_id':hash_id })
                        log(f'[  INFO  ] {status}')
                        log(f'[  INFO  ] Hash_ID - {hash_id} Removed Successfully from {config.OTP_COLLECTION} Collection in {config.OTP_DB}')
            status = self.collection.insert_one({
                'hash_id':hash_id,
                'otp':otp,
                'function':function
            })
            log(f'[  INFO  ] {status}')
            log(f'[  INFO  ] For Hash_ID - {hash_id} OTP Inserted Successfully at {config.OTP_COLLECTION} Collection in {config.OTP_DB}')
            return 201
        except Exception as e:
            log(f'[  ERROR ] Unable To Insert Document For User_ID - {user_id} at {config.OTP_COLLECTION} Collection in {config.OTP_DB}')
            return 417

    def query(self,query_param,query_value):
        # THIS QUERY FUNCTION INPUTS QUERY PARAMETER LIKE USERID AND QUERY VALUE TO SEARCH 
        # IN COLLECTION.  AFTER SUCCESSFUL SEARCH, IT RETURNS RESULT COMBINED WITH STATUS VALUE
        # -----------------------------------------------------
        # DATA STRUCTURE OF INPUT PARAMETER :-
        # QUERY_PARAMETER --> STRING
        # QUERY_VALUE --> STRING
        #
        res = self.collection.find({ query_param: query_value})
        if res.count() > 0:     ## RUNS WHEN ANY RESULT COMES
            response = {
                'status': 212,
                'res': res
            }
        else: 
            response = {
                'status':206,
                'res': None
            }
        log(f'[  INFO  ] The Search Query Completed Successfully in {config.OTP_DB}')
        return response

    def remove(self,hash_id,function):
		# USED TO REMOVE DOCUMENT CARRYING USERID AND OTP GENERATED FOR THAT USERID
		# ----------------------------------------------------------------------------
		# DATA STRUCTURES OF INPUT PARAMETER :-
		# HASH_ID --> STRING
        # FUNCTION --> STRING
        try:
            status = self.collection.delete_one({ 'hash_id':hash_id,'function':function })
            log(f'[  INFO  ] {status}')
            log(f'[  INFO  ] Hash_ID - {hash_id} Removed Successfully from {config.OTP_COLLECTION} Collection in {config.OTP_DB}')
            return 220
        except:
            return 203
            log(f'[  ERROR ] Unable To Remove Hash_ID - {hash_id} from {config.OTP_COLLECTION} Collection in {config.OTP_DB}')

    def __del__(self):
        self.client.close()	# RELEASING OPEN CONNECTION WITH DATABASE

if __name__ == "__main__":
	# TESTING SCRIPT
    pass