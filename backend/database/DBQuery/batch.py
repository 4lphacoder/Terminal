from pymongo import MongoClient
import config
import sys
from logger import log

## START OF BATCH COLLECTION API
## ------------------------------------------------------------------------------------------
## THIS BATCH CLASS IS USED FOR THE FOLLOWING FUNCTIONS:-
## 1. ADDING A NEW BATCH WITH METHOD NAME - INSERT
## 2. LISTING ALL THE STUDENTS ENROLLED IN A BATCH WITH METHOD NAME - SHOW_ALL
## 3. REMOVING ALL THE ENROLLED STUDENTS FROM BATCH WITH METHOD NAME - REMOVE_ALL
## 4. REMOVE ANY SINGLE STUDENT ENROLLED WITH METHOD NAME - REMOVE
##
class Batch:
	def __init__(self,programme,branch,section,year_of_pass):
		# THIS CONSTRUCTOR IS USED TO CREATE A REQUIRED COLLECTION
		# IN DATABASE. FOR EXAMPLE :- BATCH_BTECH_CSE_A_2021
		#
		try:
			self.client = MongoClient(config.MongoDB_URI)
			db = self.client[config.Batch_DB]
			log('[ INFO  ] Batch_DB Connected Successfully')
		except:
			log('[ Error ] Unable To Create Connection With Batch_DB')
			sys.exit(0)
		self.collection = db[ f'{programme}_{branch}_{section}_{year_of_pass}' ]

	def insert(self,enrollment):
		# USED TO INSERT ENROLLMENT OF A STUDENT IN THE REQUIRED COLLECTION
		# ---------------------------------------------------------------------------
		# DATA STRUCTURES OF ENROLLED_STUDENTS :-
		# ENROLLMENT --> STRING
		#
		# CHECKING FOR ANY DUPLICATE ENTRY IN THE COLLECTION
		duplicate_entry = self.collection.find_one({ 'enrollment':enrollment })
		if duplicate_entry != None:
			log('[ ERROR ] This Student Already Present in Database')
			return 417
		else:
			status = self.collection.insert_one({ 'enrollment':enrollment })
			log(f'[ INFO  ] {status}')
			log('[ INFo  ] A new batch has been successfully inserted.')
			return 201

	def remove(self,enrollment):
		# USED TO REMOVE ENROLLMENT OF A PARTICULAR STUDENT FROM BATCH COLLECTION
		# ----------------------------------------------------------------------------
		# DATA STRUCTURES OF INPUT PARAMETER :-
		# ENROLLMENT --> STRING
		#
		try:
			status = self.collection.delete_one({ 'enrollment':enrollment })
			log(f'[ INFO  ] {status}')
			log('[ INFo  ] Enrollment of a particular student has been removed from batch collection.')
			return 220
		except:
			return 203
    
	def remove_all(self):
		# USED TO REMOVE WHOLE COLLECTION FOR WHICH BATCH CLASS
		# OBJECT IS INITIALISED.
		# ----------------------------------------------------------------------------
		#
		try:
			self.collection.drop()
			log('[ INFO  ] Batch_DB has been removed.')
			return 512
		except:
			return 400


	def show_all(self):
		# USED TO DISPLAY A LIST OF ALL THE ENROLLED STUDENTS IN A CLASS
		try:
			res = list(self.collection.find({}))
			response = {
				'status':'302',
				'res':res
			}
		except:
			response = {
				'status':'598',
				'res':'NA'
			}
			log('[ INFO  ] All the enrolled students displayed.')
			return response

	def __del__(self):
		# log('[ INFO  ] Connection closed successfully of Batch_DB.')
		self.client.close()	# RELEASING OPEN CONNECTION WITH DATABASE


if __name__ == "__main__":
	# TESTING SCRIPT
	pass
