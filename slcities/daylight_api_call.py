import requests
import pandas as pd


class DaylightInfos():
    def __init__(self, start='01-01-2021', end='31-12-2021'):
        self.start = start
        self.end = end
        self.date_df = self.create_date_df()

    def create_date_df(self):
        return pd.DataFrame({"Date": pd.date_range(self.start, self.end)})

    def get_daylight_infos(self):
        url = 'https://api.sunrise-sunset.org/json?+lat=53.350140&lng=-6.266155&date='
        response = []
        for row in self.date_df.Date:
            res = requests.get(url+row.strftime('%Y-%m-%d')).json()
            if res['status']== 'OK':
                response.append(res['results'])
        return pd.json_normalize(response)

if __name__ == 'main':
    d = DaylightInfos()
    daylight_df = d.get_daylight_infos()
    print(daylight_df)
