import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHAVANTAGE_API_KEY = "abc123"  # Enter alphavantage API key
NEWSAPI_API_KEY = "abc123"  # Enter NewsAPI API key

TWILIO_ACCOUNT_SID = 'abc123'  # Enter Twilio account SID
TWILIO_AUTH_TOKEN = 'abc123'  # Enter Twilio auth token
TWILIO_API_KEY = "abc123"  # Enter Twilio API key

## TODO 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

ALPHAVANTAGE_PARAMETERS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "outputsize": "compact",
    "apikey": ALPHAVANTAGE_API_KEY,
}

response = requests.get(url="https://www.alphavantage.co/query", params=ALPHAVANTAGE_PARAMETERS)
response.raise_for_status()
data = response.json()
# print(data)
idx = 0
close_prices = []

# Step through the json data hierarchy and obtain the first 2 opening prices [today, yesterday]
for day in data["Time Series (Daily)"]:
    close_prices += [float(data["Time Series (Daily)"][day]["4. close"])]
    idx += 1
    # print(open_prices)
    if idx > 1:
        break

close_prices[0] = .95
close_prices[1] = 1
percent_change = round((close_prices[0] - close_prices[1])/close_prices[0] * 100)
up_down = None
if percent_change >= 0:
    up_down = "🔼"
else:
    up_down = "🔽"


## TODO 2: Use https://newsapi.org
# Get the first 3 news pieces for the COMPANY_NAME.
# If there is a greater than 5% change, get the news for Tesla
if abs(percent_change) >= 5:
    # print("get news")
    NEWSAPI_PARAMETERS = {
        "qInTitle": COMPANY_NAME,
        "apiKey": NEWSAPI_API_KEY,
    }

    response = requests.get(url="https://newsapi.org/v2/everything", params=NEWSAPI_PARAMETERS)
    response.raise_for_status()
    articles = response.json()["articles"][:3]
    # print(articles)

    ## TODO 3: Use https://www.twilio.com
    # Send a seperate message with the percentage change and each article's title and description to your phone number.

    formatted_articles = [f"{STOCK}: {up_down}{percent_change}%\nHeadline: {article['title']}.\nBrief: {article['description']}" for article in articles]

    # Twilio
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_='+##########',
            to='+##########'
        )
