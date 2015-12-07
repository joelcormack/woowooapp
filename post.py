import requests, json
 
data = { "site" : {
            "name" : "SPOC",
            "closing date" : "02/03/2016",
            "address one" : "St Pancras Old Church",
            "address two" : "",
            "postcode" : "NW1 1UL",
            },
        "contact" : {
                "name" : "Brendan Collins",
                "email" : "b@s.com",
                "phone" : "0123456789",
                "mobile" : "012873873",
        }
}
headers = {'content-type': 'application/x-www-form-urlencode'}

r = requests.post("http://192.168.1.126:8080", data=data, headers=headers)
print r
