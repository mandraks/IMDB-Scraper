#!/usr/bin/python
#----------------------------------------------------------------------------
# Created By  : Daniel Ortiz
# Created Date: Jan 2022
# Project URL: https://github.com/mandrak
# version ='1.0'
# ---------------------------------------------------------------------------
import bs4 as bs
import pandas as pd
import requests
import re
import matplotlib.pyplot as plt

# add multiple ulrs + save to multiple excels

urls = [('Top TV Shows', 'https://www.imdb.com/chart/toptv'), ('Movie Meter', 'https://www.imdb.com/chart/moviemeter'), ('Top 250 Movies', 'https://www.imdb.com/chart/top'), ('Top English Movies', 'https://www.imdb.com/chart/top-english-movies'), ('TV Meter', 'https://www.imdb.com/chart/tvmeter'), ('Top Indian Movies', 'https://www.imdb.com/india/top-rated-indian-movies'), ('Worst Rated Movies', 'https://www.imdb.com/chart/bottom')]


# https://www.imdb.com/chart/boxoffice

# create excel writer
writer = pd.ExcelWriter('output.xlsx')

for key, url in enumerate(urls):
    print("Scraping: {}".format(url))
    source = requests.get(url[1])

    soup = bs.BeautifulSoup(source.text,features='lxml')


    # .lister-list tr

    years = []
    ratings = []
    ranks = []
    titles = []

    for movie in soup.select('.lister-list tr'):
        if url[0] ==  'Movie Meter' or url[0] == 'TV Meter':
            rank = movie.select_one('.titleColumn .velocity').contents[0].text.strip()
            rank = re.search('^[0-9]*', rank)
            rank = rank[0]
        else:
            rank = movie.select_one('.titleColumn').contents[0].text.strip()[:-1]
        title = movie.select_one('.titleColumn a').text.strip()
        year = movie.select_one('span.secondaryInfo').text.strip()[1:-1]
        rating = movie.select_one('.imdbRating').text.strip()
        years.append(year)
        ratings.append(rating)
        ranks.append(rank)
        titles.append(title)

    df = pd.DataFrame({'ranking':ranks, 'titles': titles, 'years': years, 'ratings':ratings})

    # write dataframe to excel sheet named 'marks'
    df.to_excel(writer, url[0])
    # save the excel file
    writer.save()
    print('DataFrame is written successfully to Excel Sheet.')

#    plt.plot(years, ratings)
#    plt.xlabel('Year')
#    plt.ylabel('Ratings')

#    plt.show()
