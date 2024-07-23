import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "your alphavantage key"
NEWS_API_KEY = "your news api key"
account_sid = "your twilio account id"
auth_token = "your twilio auth token"

parameter = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=parameter)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_closing_price = data_list[0]["4. close"]
day_before_yesterday_closing_price = data_list[1]["4. close"]
difference = (float(yesterday_closing_price)-float(day_before_yesterday_closing_price))
sign = ""
if difference < 0:
    sign = "🔻"
else:
    sign = "🔺"
# print(difference)
diff_percent = round((difference/float(yesterday_closing_price))*100)
# print(diff_percent)
if abs(diff_percent) > 4:
    news_parameter = {
        "apiKey": NEWS_API_KEY,
        "q": COMPANY_NAME
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_parameter)
    articles = news_response.json()["articles"]
    three_articles = articles[:3]
    formatted_article = [f"{STOCK_NAME}: {sign}{diff_percent}%  Headline:{article['title']}.  Brief:{article['description']}" for article in three_articles]
    # print(formatted_article)
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=formatted_article,
        from_="your_twilio number",
        to="your registered number on twilio"
    )
    print(message.status)

"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

