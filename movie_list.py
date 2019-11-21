import csv
import requests
from pprint import pprint
from datetime import datetime, timedelta
from decouple import config

BASE_URL = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json'
key = config('API_KEY')
weekGb = '0'

for i in range(3):
    targetDt = datetime(2019, 11, 17) - timedelta(weeks=i)
    targetDt = targetDt.strftime('%Y%m%d')
    API_URL = f'{BASE_URL}?key={key}&targetDt={targetDt}&weekGb=0'

    response = requests.get(API_URL)
    data = response.json()
    # pprint(data)
    movie_data = {}

    showRange = data['boxOfficeResult']['showRange']

    for movie in data['boxOfficeResult']['weeklyBoxOfficeList']:
        movie_data[movie.get('movieCd')] = {
            '기간': showRange ,
            '영화코드': movie.get('movieCd'),
            '영화제목': movie.get('movieNm'),
            '순위': movie.get('rank'),
        }

        pprint(movie_data)

    with open('movie.csv', 'w', encoding='utf-8') as f:
        fieldnames = ['기간', '영화코드', '영화제목', '순위']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in movie_data.values():
            writer.writerow(item)
