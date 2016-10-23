from rapidconnect import RapidConnect
import requests
import json

rapid = RapidConnect('DJT', '173286f8-8072-4dbf-bef8-91c992403d8e');

result = rapid.call('FacebookGraphAPI', 'getProfile', { 
	'access_token': 'EAACEdEose0cBAFTI9ZAw2k1eUcdMZCTQqBNpyU8D0ooDE8CoqabLVwr6snXvDSFkPwLqC6QJwtE42AwdkO1903QSb7EgwfaA71FNVD9UY1cIMZCU5NWhNOXSPfljusIMcXECnqL4uZBPywA12ICdKJQKNJbXeULWXAPND0kNDAZDZD',
		'profile_id': 'me'
		 
		 });
#print result
jsontext = json.loads(result)
idnum = jsontext["id"]

access = 'EAACEdEose0cBADeXcfNC9FujDha0qV9cmNZCP02ywTZCzM2zq3DR3grSYqGhgePNpBjt5A805KzZC8vRaKNaIm53ZBKTFu09oZBXF9aZCs4ZB62hYWFAd3LI5FCOb6lX53wBeUHOkAzvCwh4CH8oZCw4a5KWN5zQ8J69tudWeEA4ZBQZDZD'

fields = "id,name,hometown,about,age_range,birthday,education,gender,inspirational_people,interested_in,locale,political,religion,relationship_status"

r = requests.get("https://graph.facebook.com/v2.8/"+idnum+"?fields="+fields+"&access_token="+access) 
jsontext = json.loads(r.content)
guess = 0

if "age_range" in jsontext:
	age = jsontext["age_range"]
	avgage = (age["max"] + age["min"]) /2
	if avgage < 27:
		guess += 16 
	elif average < 40:
		guess += 7
	elif average > 60:
		guess -= 4

	if avgage > 25 and "College" not in jsontext:
		guess -= 8

if "gender" in jsontext:
	gender = jsontext["gender"]
	if gender == "male":
		guess -= 2
	else:
		guess += 7

location = "Austin"
if location == "Austin":
	guess += 1

#print r.content
if guess > 0:
	print 'D'
else:
	print 'R'
