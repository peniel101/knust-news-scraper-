from bs4 import BeautifulSoup
import requests
from datetime import datetime
from pushbullet import Pushbullet
import os

# api key of pushbullet
API_KEY = os.environ.get("PUSH_API_KEY")


def get_knust_news():
    # Url of my university announcements page
    url = "https://www.knust.edu.gh/announcements"
    request = requests.get(url)
    content = request.text
    # making a beautiful soup object
    soup = BeautifulSoup(content, "lxml")
    # scraping the annoucements and date published from the university site
    articles = soup.find_all("div", {"class": "views-row"})
    news_list = []
    published_date = []
    for element in articles:
        news = element.find_all("h3")
        date_published = element.find_all('span')
        for dates in date_published:
            date = dates.find_all('span')
            for time_published in date:
                published_date.append(time_published.text)
        for news_text in news:
            news_list.append(news_text.text)

    # slicing the news to get the first 5 elements in the list
    date_keys = published_date[:7]
    news_values = news_list[:7]

    #using the Pushbullet API to send the notification
    todays_date = datetime.today().now()
    Title = f"Knust Announcements, last updated: {todays_date}"
    # Authentication
    pb = Pushbullet(api_key=API_KEY)
    # looping through the list of news and appending it to message string
    message = ""
    for i in range(0, len(news_values)):
        message += f"{date_keys[i]}:{news_values[i]}\n\n"
    # sending the notifications to my phone
    pb.push_note(Title, message)


get_knust_news()


