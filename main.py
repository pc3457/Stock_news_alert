import datetime
import smtplib
import requests
from email.message import EmailMessage
import os

# Add Company Stocks below based on choice
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
COMPANY = "tesla"

# Email credentials
my_email = "ptest6969python@gmail.com"
password = "your_mail_pass"

# Accessing dates to get previous and the day before stock prices data
today = str(datetime.datetime.now().date())
yesterday = str(datetime.datetime.now().date() - datetime.timedelta(days=1))
day_before = str(datetime.datetime.now().date() - datetime.timedelta(days=2))

STOCK_ENDPOINT = "https://www.alphavantage.co/query"

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# Get the stock end points by accessing both above sites and storing the data in your environment
stock_api_key = os.environ.get("STOCK_KEY")
new_api_key = os.environ.get("NEWS_KEY")

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": stock_api_key
}
# Request to get stock data
r = requests.get(STOCK_ENDPOINT, params=stock_params)
stock_data = r.json()
print(stock_data)
stock_dates = stock_data['Time Series (Daily)']
close_price = []
for values in stock_dates.keys():
    close_price.append(stock_dates[values]['4. close'])

print(close_price)

news_params = {
    "q": COMPANY,
    "from": yesterday,
    "sortBy": "popularity",
    "apiKey": new_api_key
}
# Request to get news data
news_r = requests.get(NEWS_ENDPOINT, params=news_params)
news_data = news_r.json()

# Setting up the calculations
difference = float(close_price[0]) - float(close_price[1])
UpDown = None
if difference < 0:
    UpDown = "🔻"
elif difference > 0:
    UpDown = "🔺"
percentage_data = round(difference / float(close_price[0]) * 100)
print(percentage_data)
articles = news_data['articles']
three_articles = articles[:3]

print(percentage_data)
# You can change the percentage of the stocks change in the below line
if abs(percentage_data) > 4:
    print(three_articles)
    for article in three_articles:
        subject = f"{STOCK} stock:{UpDown}{percentage_data}% ,{article['title']}"
        body = f"{article['description']}"

        # build-up email details using email.message module
        message = EmailMessage()
        message["Subject"] = subject
        message["From"] = my_email
        message["To"] = my_email
        message.set_content(body)

        # send the message via smtp using details above
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(my_email, password=password)
            connection.send_message(message)

else:
    print("Stock dates not adding up")
