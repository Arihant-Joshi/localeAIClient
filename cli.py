from client import Client
import argparse
import os
import json
import csv
import pandas as pd

def cleanDict(data):
	return {k: v for k, v in data.items() if v not in [None,""]}

def postRow(data):
	data = cleanDict(data)
	if("booking_id" not in data):
		return ""
	response = client.createNew(data)
	if(type(response) == str and response[:6] == "ERROR:"):
		return response
	return ""

def putRow(data):
	data = cleanDict(data)
	if("booking_id" not in data):
		return ""
	bId = data["booking_id"]
	del data["booking_id"]
	response = client.update(data,bId)
	if(type(response) == str and response[:6] == "ERROR:"):
		return response
	return ""

def listToCSV(data,outFile):
	with open(outFile,"w") as file:
		csv_writer = csv.writer(file)
		header = data[0].keys()
		csv_writer.writerow(header)
		for emp in data:
			csv_writer.writerow(emp.values())

def dictToCSV(data,outFile):
	with open(outFile,"w") as file:
		csv_writer = csv.writer(file)
		csv_writer.writerow(data.keys())
		csv_writer.writerow(data.values())

parser = argparse.ArgumentParser(prog='', description='')
parser.add_argument('cmd', choices=['get','put','post','delete','help','quit'])
parser.add_argument('-p','--path',type = str,help="Path to Input/Output File(Get/Post/Put)")
parser.add_argument('-c','--csv',action = "store_true",help="Flag: The File is in CSV format(Get/Post/Put)")
parser.add_argument('-b','--bookingId',type = int,help="Booking ID([Get]/Delete)")

client = Client()

username = "djAdmin"
password = "locale.ai"
print("####USE THESE CREDENTIALS####")
print(f"USERNAME:{username}")
print(f"PASSWORD:{password}")

while(True):
	username = input("USERNAME:")
	password = input("PASSWORD:")
	response = client.getToken(username,password)
	if(type(response) == str and response[:6] == "ERROR:"):
		print(response)
		print("Wrong Credentials")
		continue
	break
#client.getToken(username,password)
#print(client.getData(12))

while(True):
	astr = input('$: ')
	astr = astr.split()
	astr[0] = astr[0].lower()
	# print astr
	try:
		args = parser.parse_args(astr)
	except SystemExit:
		# trap argparse error message
		#print('error')
		continue
	#if(args.cmd in ['get','put','post','delete']):
		#print(f'doing {args.cmd}')
	if(args.cmd == "get"):
		if(not args.path):
			print("Requires --path argument,\nThe location of output file")
			continue
		if(args.bookingId):
			response = client.getData(args.bookingId)
		else:
			response = client.getAllData()

		if(type(response) == str):
			print(response)
			continue
		
		if(os.path.exists(args.path)):
			os.remove(args.path)

		if(args.csv):
			if(type(response) == list):
				listToCSV(response,args.path)
			else:
				dictToCSV(response,args.path)
		else:
			with open(args.path,"w") as outputFile:
				json.dump(response,outputFile,indent=4)

	elif(args.cmd == "post"):
		if(not args.path):
			print("Requires --path argument,\nThe location of input file")
			continue
		if(not os.path.exists(args.path)):
			print("File Does Not Exist")
			continue

		errorList = {}
		with open(args.path) as file:
			if(args.csv):
				data = {}
				reader = csv.reader(file)
				first = True
				keys = []
				for row in reader:
					if(first):
						first = False
						keys = row
						continue
					data = dict(zip(keys,row))
					response = postRow(data)
					if(response != ""):
						errorList[data["booking_id"]] = response

			else:
				data = json.load(file)
				if(type(data) == list):
					for entry in data:
						response = postRow(entry)
						if(response != ""):
							errorList[entry["booking_id"]] = response
				else:
					response = postRow(data)
					if(response != ""):
						errorList[data["booking_id"]] = response
		print(errorList)

	elif(args.cmd == "put"):
		if(not args.path):
			print("Requires --path argument,\nThe location of input file")
			continue
		if(not os.path.exists(args.path)):
			print("File Does Not Exist")
			continue

		errorList = {}
		with open(args.path) as file:
			if(args.csv):
				data = {}
				reader = csv.reader(file)
				first = True
				keys = []
				for row in reader:
					if(first):
						first = False
						keys = row
						continue
					data = dict(zip(keys,row))
					response = putRow(data)
					if(response != ""):
						errorList[data["booking_id"]] = response
			else:
				data = json.load(file)
				if(type(data) == list):
					for entry in data:
						response = putRow(entry)
						if(response != ""):
							errorList[entry["booking_id"]] = response
				else:
					response = putRow(data)
					if(response != ""):
						errorList[data["booking_id"]] = response
		print(errorList)

	elif(args.cmd == "delete"):
		if(not args.bookingId):
			print("Requires --bookingId argument,\nThe Booking_Id of the entry to be deleted")
			continue
		response = client.deleteEntry(args.bookingId)
		if(type(response) == str and response[:6] == "ERROR:"):
			print(response)
			continue

	elif args.cmd == 'help':
		parser.print_help()

	else:
		print('done')
		break