import requests, json
 
data =  {"site-name" : "SPOC","site-add-one" : "St Pancras Old Church","site-add-two" : "","site-postcode" : "NW1 1UL","contact-firstname" : "Brendan", "contact-lastname": "Collins","contact-email" : "b@s.com","contact-landline" : "0123456789","contact-mobile" : "012873873"}
#headers = {'content-type': 'application/x-www-form-urlencode'}

#r = requests.post("http://192.168.1.126:8080", data=data, headers=headers)
r = requests.post("http://0.0.0.0:8080/update", data=data)
print r
