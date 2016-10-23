import requests
import json
import csv
from lxml import html
import sys
from rapidconnect import RapidConnect
from flask import Flask, url_for

app = Flask(__name__)

@app.route('/rapid/<key>')
def api_rapid(key):
	val = rapid(key)
	return val

@app.route('/candidates/<articleid>')
def api_candidates(articleid):
	return json.dumps(candidates(articleid))

def rapid(access_key):
	rapid = RapidConnect('DJT', '173286f8-8072-4dbf-bef8-91c992403d8e');

	result = rapid.call('FacebookGraphAPI', 'getProfile', { 
		'access_token': 'EAACEdEose0cBAFD1EhI4HoMzJkyMvZCK4NXLbd4YJQUxy6bZAvdpJSZAbhKBGm46GU8BO0Ybk5Nzdp1iHM1M88t6gEp0MrEOCpD2RgZBj99S7c3SQGSMjZBcpZCCufj9AcyQDKX9epZCKppmsoKEmJhByx8mW6DdypabCTrF2V5mAZDZD',
		'profile_id': 'me'
		 
		 });
	jsontext = json.loads(result)
	idnum = jsontext["id"]

	access = 'EAACEdEose0cBAFD1EhI4HoMzJkyMvZCK4NXLbd4YJQUxy6bZAvdpJSZAbhKBGm46GU8BO0Ybk5Nzdp1iHM1M88t6gEp0MrEOCpD2RgZBj99S7c3SQGSMjZBcpZCCufj9AcyQDKX9epZCKppmsoKEmJhByx8mW6DdypabCTrF2V5mAZDZD'

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

	if guess > 0:
		return 'D'
	else:
		return 'R'

def candidates(address):
	r = requests.get('https://api.geocod.io/v1/geocode?q='+address+'&fields=stateleg,cd&api_key=d016fddc414e84c3f1580b8bc58f110d0c10be5');
	jsontext = json.loads(r.content)

	countyreq = requests.get('http://www2.census.gov/geo/docs/reference/codes/files/national_county.txt')
	ctext = countyreq.content

	statesen = str(jsontext["results"][0]["fields"]["state_legislative_districts"]["senate"]["district_number"])
	statehouse = str(jsontext["results"][0]["fields"]["state_legislative_districts"]["house"]["district_number"])
	cong = str(jsontext["results"][0]["fields"]["congressional_district"]["district_number"])
	county = str(jsontext["results"][0]["address_components"]["county"])
	stateabbr = str(jsontext["results"][0]["address_components"]["state"])

	index = ctext.find(stateabbr)
	county = county[index:]
	countyreq.content.find(county)

	countynum = ""
	index -= 2
	countynum = ctext[index - 2] + ctext[index - 1] + ctext[index]

	url = 'http://vote-'+stateabbr.lower()+'.org/Ballot.aspx?State='+stateabbr+'&Election='+stateabbr+'20161108GA&Congress='+cong+'&StateSenate='+statesen+'&StateHouse='+statehouse+'&County='+countynum
	r = requests.get(url)
	print r.content
	tree = html.fromstring(r.content)

	print r.url

	allar = []
	for i in range(1,20):
		job = tree.xpath('//*[@id="MasterMainContent_InnerContent"]/div[3]/div/div['+str(i)+']/div/div[1]/div[1]/span/text()')
		ar = []
		for j in range(1,10):
			candidates = tree.xpath('//*[@id="MasterMainContent_InnerContent"]/div[3]/div/div['+str(i)+']/div/div['+str(j)+']/div/div[1]/span/text()')
			website = tree.xpath('//*[@id="MasterMainContent_InnerContent"]/div[3]/div/div['+str(i)+']/div/div['+str(j)+']/div/div[3]/div[1]/span[1]/span/a/@href')
			moreinfo = tree.xpath('//*[@id="MasterMainContent_InnerContent"]/div[3]/div/div['+str(i)+']/div/div['+str(j)+']/div/div[3]/div[4]/a/@href')
			party = tree.xpath('//*[@id="MasterMainContent_InnerContent"]/div[3]/div/div['+str(i)+']/div/div['+str(j)+']/div/div[1]/span[1]/a/text()')
			#if len(moreinfo) > 0:
			#	morehtml = requests.get(moreinfo[0])
			if len(candidates) > 0:
				#print(job,candidates[0][:-3],party,website,moreinfo)
				ar.append((job,candidates[0][:-3],party,website,moreinfo))
		allar.append(ar)
	return allar
	

app.run()
