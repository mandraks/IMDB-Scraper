#!/usr/bin/python
#----------------------------------------------------------------------------
# Created By  : Daniel Ortiz
# Created Date: Jan 2022
# Project URL: https://github.com/mandrak
# version ='1.0'
# ---------------------------------------------------------------------------
import bs4 as bs
import requests
import matplotlib.pyplot as plt
from pandas import DataFrame

# add multiple ulrs + save to multiple excels

url = 'https://www.imdb.com/chart/toptv'
source = requests.get(url)

soup = bs.BeautifulSoup(source.text,features='lxml')

# .lister-list tr

years = []
ratings = []
ranks = []
titles = []

for movie in soup.select('.lister-list tr'):
    rank = movie.select_one('.titleColumn').contents[0].text.strip()[:-1]
    title = movie.select_one('.titleColumn a').text.strip()
    year = movie.select_one('span.secondaryInfo').text.strip()[1:-1]
    rating = movie.select_one('.imdbRating strong').text.strip()
    years.append(year)
    ratings.append(rating)
    ranks.append(rank)
    titles.append(title)

plt.plot(years, ratings)
plt.xlabel('Year')
plt.ylabel('Ratings')

plt.show()

df = DataFrame({'ranking':ranks, 'titles': titles, 'years': years, 'ratings':ratings})

df.to_excel('test.xlsx', index=False)
