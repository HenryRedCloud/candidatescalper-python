import requests
import json
import csv
from lxml import html
import sys

address = sys.argv[1]
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
	job = tree.xpath('//*[@id="MasterMainContent_InnerContent"]/div[3]/div/div['+str(i)+']/div/div[1]/div[1]/span/text()')
	for j in range(1,10):
		candidates = tree.xpath('//*[@id="MasterMainContent_InnerContent"]/div[3]/div/div['+str(i)+']/div/div['+str(j)+']/div/div[1]/span/text()')
		website = tree.xpath('//*[@id="MasterMainContent_InnerContent"]/div[3]/div/div['+str(i)+']/div/div['+str(j)+']/div/div[3]/div[1]/span[1]/span/a/@href')
		moreinfo = tree.xpath('//*[@id="MasterMainContent_InnerContent"]/div[3]/div/div['+str(i)+']/div/div['+str(j)+']/div/div[3]/div[4]/a/@href')
		party = tree.xpath('//*[@id="MasterMainContent_InnerContent"]/div[3]/div/div['+str(i)+']/div/div['+str(j)+']/div/div[1]/span[1]/a/text()')
		if len(moreinfo) > 0:
			morehtml = requests.get(moreinfo[0])
#			print(morehtml.content)
		if len(candidates) > 0:
			print(job,candidates[0][:-3],party,website,moreinfo)
			name = candidates[0][:-3].split(" ")[0]
			r = requests.get("https://congress.api.sunlightfoundation.com/legislators?query="+name+"&apikey=9b5f43862a344c20865c9491753c9f01") 
			jsontext = json.loads(r.content)
			print jsontext
			if len(jsontext["results"]) > 0:
				idnum = jsontext["results"][0]["govtrack_id"]
				print idnum
