import requests

url = "https://yh-finance.p.rapidapi.com/market/get-trending-tickers"

querystring = {"region":"US"}

headers = {
	"X-RapidAPI-Host": "yh-finance.p.rapidapi.com",
	"X-RapidAPI-Key": "8876aab035mshfea535f6d8296bep106416jsn61e14a5e69ae"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)