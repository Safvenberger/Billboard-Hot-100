from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import sys

url = 'https://www.billboard.com/archive/charts/1958/hot-100'  # start year
base_url = 'https://www.billboard.com'
r = requests.get(url.strip())  # download url
soup = BeautifulSoup(r.content, 'html.parser')  # extract HTML elements from the url

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']

years = soup.find_all('li', attrs={'class': 'year-list__decade__dropdown__item'})
years = [str(tag) for tag in years]  # convert all tags to string
years = [re.sub('<li.+href="', '', i) for i in years]  # remove html elements
year_urls = [re.split('"', i)[0] for i in years]
years = [re.split('/', i)[-1] for i in year_urls]
years.append(str(int(years[-1])+1))

user_year = input('What year do you wish to gather data from?')

try:
    int(user_year)
except ValueError:
    sys.exit('Invalid input. Please enter a year in YYYY format')

if user_year not in years:
    sys.exit('This year is not available. Please select another year between 1958 and the current year.')

r = requests.get(base_url + '/archive/charts/' + user_year + '/hot-100')
soup = BeautifulSoup(r.content, 'html.parser')

songs_and_dates = soup.find_all('td')  # find items indicating the songs
songs_and_dates = [str(tag) for tag in songs_and_dates]  # convert all tags to string

chart_dates = [item.split('"')[1] for item in songs_and_dates if
               re.split('\d+', item.split('>')[2])[0].strip() in months]

billboard = dict()

for day in chart_dates:
    r = requests.get(base_url + day)
    soup = BeautifulSoup(r.content, 'html.parser')

    week = dict()
    chart_items = soup.find_all('div', attrs={'class': 'chart-list-item'})  # find rows indicating the songs
    chart_items = [str(tag) for tag in chart_items]  # convert each tag to a string

    chart_items = [re.sub('<div.+>(?=[0-9])|</div>|<div>|<div.+>', '', item) for item in chart_items]
    chart_items = [re.sub('<a.+">|</a>|<span.+>|</span>', '', item) for item in chart_items]  # remove all a and span
    chart_items = [re.sub('<img.+">|<i.+>', '', item) for item in chart_items]  # remove images
    chart_items = [re.sub('Lyrics', '', item) for item in chart_items]  # remove lyrics
    chart_items = [re.sub('<hr class.+', '', item) for item in chart_items]  # remove all a and span elements
    chart_items = [re.sub('\n\s+\n\s+|\n\s+\n|\n+', '\n', item) for item in chart_items]  # remove multiple \n with one

    chart_items = [re.sub('&amp;', '&', item) for item in chart_items]

    shared_rank = [i for i, j in enumerate(chart_items) if
                   chart_items[i].split('\n')[1].strip() != str(chart_items.index(j) + 1)]

    if len(shared_rank) > 0:
        for double in shared_rank:
            chart_items[double] = re.sub(chart_items[double].split('\n')[1],
                                         str(int(chart_items[double].split('\n')[1]) + 1),
                                         chart_items[double])

    for item in chart_items:
        item_index = chart_items.index(item)
        chart_rank = re.search(r'(?<=\n)[0-9]+|(?<=\n)\s[0-9]+', item)  # where did the song rank
        week[chart_rank.group(0).strip()] = chart_items[item_index][chart_rank.end():]  # dictionary with rank as key

    df = pd.DataFrame.from_dict(week, orient='index')
    df = df[0].str.split('\n', 9, expand=True)
    del df[0]

    if day != '/charts/hot-100/1958-08-04':
        df.loc[df[3] == 'LAST WEEK', 3] = ''
        df.loc[df[5] == 'PEAK POSITION', 5] = ''
        df.loc[df[7] == 'WEEKS ON CHART', 7] = ''

        df.fillna('', inplace=True)  # replace all rows with None to ''

        df.loc[df[4].str.isnumeric(), 5] = df.loc[df[4].str.isnumeric(), 4]
        df.loc[df[4].str.isnumeric(), 4] = ''
        df.loc[df[6].str.isnumeric(), 7] = df.loc[df[6].str.isnumeric(), 6]
        df.loc[df[6].str.isnumeric(), 6] = ''
        df.loc[df[8].str.isnumeric(), 9] = df.loc[df[8].str.isnumeric(), 8]
        df.loc[df[8].str.isnumeric(), 8] = ''

        df.rename(index=str, inplace=True,
                  columns={1: 'Song', 2: 'Artist', 3: 'Last week', 5: 'Peak position', 7: 'Weeks on chart'})

        del df[4], df[6], df[8], df[9]
    else:
        del df[3]
        df.rename(index=str, inplace=True, columns={1: 'Song', 2: 'Artist'})

    df['Week'] = day.split('/')[-1]
    billboard[day.split('/')[-1]] = df

billboard = pd.concat(billboard.values())  # merge all data frames in the dictionary
billboard = billboard[['Week', 'Song', 'Artist', 'Last week', 'Peak position', 'Weeks on chart']]  # reorder columns

billboard['Artist'] = [i.strip() for i in billboard['Artist']]
billboard['Song'] = [i.strip() for i in billboard['Song']]

billboard.to_csv('BillboardHot100-' + user_year + '.csv', encoding='utf-8')

print('Data successfully downloaded and saved in a csv.')
