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
headers = {'content-type': 'application/json'}

r = requests.post("http://0.0.0.0:8080/update", data=json.dumps(data), headers=headers)
