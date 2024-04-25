import requests
from dotenv import load_dotenv
import os
from datetime import datetime as dt, timedelta

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

load_dotenv()

STOCK_API_KEY = os.getenv("STOCK_API_KEY")
STOCK_API_URL = os.getenv("STOCK_API_URL")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_API_URL = os.getenv("NEWS_API_URL")


def get_news():
    news_params = {
        "apiKey": NEWS_API_KEY,
        "q": COMPANY_NAME,
        "from": yesterday
    }
    news_response = requests.get(NEWS_API_URL, news_params)
    news_data = news_response.json()

    articles_data = news_data["articles"]

    message = f'Headline: {articles_data[2]["title"]}\n'
    message += f'Brief: {articles_data[2]["description"]}'

    return message

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY
}
stock_response = requests.get(STOCK_API_URL, params=stock_params)
stock_data = stock_response.json()

# get yesterday
today = dt.now()
yesterday = (today - timedelta(days=1)).strftime("%Y-%m-%d")
day_before_yesterday = (today - timedelta(days=13)).strftime("%Y-%m-%d")

daily_data = stock_data["Time Series (Daily)"]
yesterday_close = float(daily_data[yesterday]["4. close"])
day_before_yesterday_close = float(daily_data[day_before_yesterday]["4. close"])

# check the difference (positive or negative)
if abs(yesterday_close / day_before_yesterday_close - 1) > 0.05:
    is_positive = yesterday_close / day_before_yesterday_close > 1
    percentage = int(abs(yesterday_close / day_before_yesterday_close - 1)*100)

    message = f'{"🔺" if is_positive else "🔻"}{percentage}%\n'
    message += get_news()
    print(message)

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

