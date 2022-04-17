import requests
from config.credentials import *

url = "https://yh-finance.p.rapidapi.com/market/get-trending-tickers"

querystring = {"region":"US"}

headers = {
	"X-RapidAPI-Host": "yh-finance.p.rapidapi.com",
	"X-RapidAPI-Key": RAPID_API_KEY
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)
