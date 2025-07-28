import requests
from apikeys import alpha_vantage_api_key
from datetime import datetime, timedelta

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

"""the api is providing 3 days before data
that is why we subtract 3 days from today
to dynamically change the date"""
today_date = datetime.now().date()
three_days_ago = today_date - timedelta(days=3)
string_three_days_ago = three_days_ago.strftime("%Y-%m-%d")
four_days_ago = today_date - timedelta(days=4)
string_four_days_ago = four_days_ago.strftime("%Y-%m-%d")
# print(today_date)
# print(three_days_ago)


STOCK_API_KEY = alpha_vantage_api_key
# print(STOCK_API_KEY)

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

response = requests.get(url=STOCK_ENDPOINT, params=stock_params)
response.raise_for_status()
stock_data = response.json()
# print(stock_data)
# print(stock_data["Time Series (Daily)"])

# the api is providing the data as of three days ago
# three_days_ago_opening_price = stock_data["Time Series (Daily)"][string_three_days_ago]["1. open"]
three_days_ago_closing_price = stock_data["Time Series (Daily)"][string_three_days_ago]["4. close"]
# print(three_days_ago_opening_price)
print(three_days_ago_closing_price)

# four_days_ago_opening_price = stock_data["Time Series (Daily)"][string_four_days_ago]["1. open"]
four_days_ago_closing_price = stock_data["Time Series (Daily)"][string_four_days_ago]["4. close"]
# print(four_days_ago_opening_price)
print(four_days_ago_closing_price)

# calculate the difference between the prices
difference = abs(float(three_days_ago_closing_price) - float(four_days_ago_closing_price))
print(difference)

# calculate the percentage of the difference
diff_percent = (difference / float(three_days_ago_closing_price)) * 100
print(diff_percent)

if diff_percent > 4:
    print("get News")
