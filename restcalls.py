import requests
import json
import csv
from lxml import html
import sys
from rapidconnect import RapidConnect

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

@api_view(['GET', 'POST'])
def snippet_list(request):
	if request.method == 'GET':
		snippets = Snippet.objects.all()
		serializer = SnippetSerializer(snippets, many=True)
		return Response(serializer.data)

	elif request.method == 'POST':
		serializer = SnippetSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		
def rapid(access_key):
	rapid = RapidConnect('DJT', '173286f8-8072-4dbf-bef8-91c992403d8e');

	result = rapid.call('FacebookGraphAPI', 'getProfile', { 
		'access_token': 'EAACEdEose0cBAFTI9ZAw2k1eUcdMZCTQqBNpyU8D0ooDE8CoqabLVwr6snXvDSFkPwLqC6QJwtE42AwdkO1903QSb7EgwfaA71FNVD9UY1cIMZCU5NWhNOXSPfljusIMcXECnqL4uZBPywA12ICdKJQKNJbXeULWXAPND0kNDAZDZD',
		'profile_id': 'me'
		 
		 });
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

	tree = html.fromstring(r.content)

	print r.url

	for i in range(1,20):
		for j in range(1,10):
			job = tree.xpath('//*[@id="MasterMainContent_InnerContent"]/div[3]/div/div['+str(i)+']/div/div[1]/div[1]/span/text()')
			candidates = tree.xpath('//*[@id="MasterMainContent_InnerContent"]/div[3]/div/div['+str(i)+']/div/div['+str(j)+']/div/div[1]/span/text()')
			website = tree.xpath('//*[@id="MasterMainContent_InnerContent"]/div[3]/div/div['+str(i)+']/div/div['+str(j)+']/div/div[3]/div[1]/span[1]/span/a/@href')
			moreinfo = tree.xpath('//*[@id="MasterMainContent_InnerContent"]/div[3]/div/div['+str(i)+']/div/div['+str(j)+']/div/div[3]/div[4]/a/@href')
			party = tree.xpath('//*[@id="MasterMainContent_InnerContent"]/div[3]/div/div['+str(i)+']/div/div['+str(j)+']/div/div[1]/span[1]/a/text()')
			if len(moreinfo) > 0:
				morehtml = requests.get(moreinfo[0])
#				print(morehtml.content)
			if len(candidates) > 0:
				print(job,candidates[0][:-3],party,website,moreinfo)
