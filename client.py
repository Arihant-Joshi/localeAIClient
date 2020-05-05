import requests

class Client:
	def __init__(self):
		self.URLMain = "https://locale-ai.herokuapp.com"
		self.token = None

	def getToken(self,username,password):
		url = f"{self.URLMain}/api/user/"
		response = requests.post(url,data = {
			"username":f"{username}",
			"password":f"{password}"
			})
		self.token = self.procResponse(response)#.json()
		return self.token

	def getAllData(self):
		url = f"{self.URLMain}/api/basic/"
		#token = getToken()
		header = {"Authorization" : f"Token {self.token}"}
		response = requests.get(url, headers = header)
		return self.procResponse(response)

	def getData(self,booking_id):
		url = f"{self.URLMain}/api/basic/{booking_id}"
		#print(url)
		#token = getToken()
		header = {"Authorization" : f"Token {self.token}"}
		response = requests.get(url, headers = header)
		return self.procResponse(response)

	def createNew(self,data):
		url = f"{self.URLMain}/api/basic/"
		#token = getToken()
		#print(data)
		header = {"Authorization" : f"Token {self.token}"}
		response = requests.post(url,data = data, headers = header)
		return self.procResponse(response)

	def update(self,data,booking_id):
		url = f"{self.URLMain}/api/basic/{booking_id}"
		#token = getToken()
		print(booking_id)
		print(data)
		header = {"Authorization" : f"Token {self.token}"}
		response = requests.put(url,data = data, headers = header)
		return self.procResponse(response)

	def deleteEntry(self,booking_id):
		url = f"{self.URLMain}/api/basic/{booking_id}"
		#token = getToken()
		header = {"Authorization" : f"Token {self.token}"}
		response = requests.delete(url, headers = header)
		return self.procResponse(response)

	def procResponse(self,response):
		if(response.status_code >= 200 and response.status_code < 300):
			return response.json()
		#print(response)
		return f"ERROR: HTTP STATUS {response.status_code}"
		

#YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z]
"""jsonData = {'booking_id': 2,
			'user_id': 1234,
			'vehicle_model_id': 1234, 
			'travel_type_id': 1, 
			'from_date': datetime.datetime.now(), 
			'online_booking': 1, 
			'mobile_site_booking': 1, 
			'booking_created': datetime.datetime.now(), 
			'Car_Cancellation': 0
			}
jsonData1 = {
			"mobile_site_booking": 10
			}

print(getToken())"""
#print(getData(11))
#print(update(jsonData1,11).text)
#print(deleteEntry(11))
#print(createNew(jsonData).status_code)