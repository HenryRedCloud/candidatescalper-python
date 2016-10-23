import requests
import json

r = requests.get("https://congress.api.sunlightfoundation.com/legislators?last_name=Williams&apikey=9b5f43862a344c20865c9491753c9f01") 
jsontext = json.loads(r.content)
print jsontext
idnum = jsontext["results"][0]["bioguide_id"]
idnum = jsontext["results"][0]["govtrack_id"]
print idnum
#r = requests.get("https://www.govtrack.us/api/v2/vote_voter/?person="+idnum+"&limit=1000&order_by=created&format=csv&fields=vote__id,created,option__value,vote__category,vote__chamber,vote__question,vote__number")

r = requests.get("https://www.govtrack.us/api/v2/vote_voter/?person=400222&limit=6000&order_by=-created&format=csv&fields=person__id,vote__id,option__value")

print r.content
