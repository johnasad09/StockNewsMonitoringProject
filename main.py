import requests
from apikeys import ALPHA_VANTAGE_API_KEY, NEWS_API_KEY, TWILIO_AUTH_TOKEN, TWILIO_SID
from datetime import datetime, timedelta
from twilio.rest import Client

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




STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# for security purpose, we saved the api key in another module and then imported it here
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": ALPHA_VANTAGE_API_KEY,
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
difference = float(three_days_ago_closing_price) - float(four_days_ago_closing_price)
print(difference)

# calculate the percentage of the difference
diff_percent = round((difference / three_days_ago_closing_price) * 100)
# diff_percent = (difference / float(three_days_ago_closing_price)) * 100
# print(diff_percent)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

if abs(diff_percent) > 1:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    # print(articles)

    three_articles = articles[:3]
    # print(three_articles)

    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}% \nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    for article in formatted_articles:

        message = client.messages.create(
            body=article,
            from_="+123456789",
            to="+123456789"
        )
