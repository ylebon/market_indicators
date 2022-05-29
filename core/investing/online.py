import datetime
import pandas as pd
import pytz
from bs4 import BeautifulSoup
from requests import Session


class OnlineMetrics(object):
    def __init__(self):
        self._session = Session()

    def get_pivot(self, symbol):
        """
        Get investing.com pivot
        :return:
        """
        resp = self._session.get("https://www.investing.com/technical/pivot-points",
                                 headers={'User-agent': 'Google Chrome'})
        soup = BeautifulSoup(resp.text, "html.parser")
        table = soup.find(id="classical")
        table_rows = [[td.text for td in row.find_all("td")] for row in table.find_all("tr")[1:]]

        # get headers for dataframe
        table_headers = [th.text for th in table.find_all("th")]

        # build df from tableRows and headers
        df = pd.DataFrame(table_rows, columns=table_headers)
        df['Symbol'] = df['Name'].apply(lambda x: x.strip().replace('/', '_'))
        return df

    def get_historical_data(self, symbol):
        symbol = symbol.lower().replace('_', '-')
        resp = self._session.get("https://www.investing.com/currencies/{symbol}-historical-data".format(symbol=symbol),
                                 headers={'User-agent': 'Google Chrome'})

        soup = BeautifulSoup(resp.content, 'html.parser')
        table = soup.find("table", {"id": "curr_table"})
        table_rows = [[td.text for td in row.find_all("td")] for row in table.find_all("tr")[1:]]

        # get headers for dataframe
        table_headers = [th.text for th in table.find_all("th")]

        # build df from tableRows and headers
        df = pd.DataFrame(table_rows, columns=table_headers)
        df['Change %'] = df['Change %'].apply(lambda x: x.strip().replace('%', ''))
        return df

    def get_technical_summary(self, symbol):
        symbol = symbol.lower().replace('_', '-')
        resp = self._session.get("https://www.investing.com/currencies/{symbol}".format(symbol=symbol),
                                 headers={'User-agent': 'Google Chrome'})

        soup = BeautifulSoup(resp.content, 'html.parser')
        table = soup.find("table", {"class": "technicalSummaryTbl"})
        table_rows = [[td.text for td in row.find_all("td")] for row in table.find_all("tr")[1:]]

        # get headers for dataframe
        table_headers = [th.text for th in table.find_all("th")]

        # build df from tableRows and headers
        df = pd.DataFrame(table_rows, columns=table_headers)
        return df

    def get_technical_indicators(self, symbol):
        symbol = symbol.lower().replace('_', '-')
        resp = self._session.get("https://www.investing.com/currencies/{symbol}-technical".format(symbol=symbol),
                                 headers={'User-agent': 'Google Chrome'})

        soup = BeautifulSoup(resp.content, 'html.parser')
        table = soup.find("table", {"class": "technicalIndicatorsTbl"})
        table_rows = [[td.text.strip().replace('\n', '').replace('\t', '') for td in row.find_all("td")] for row in table.find_all("tr")[1:]]

        # get headers for dataframe
        table_headers = [th.text for th in table.find_all("th")]

        # build df from tableRows and headers
        df = pd.DataFrame(table_rows, columns=table_headers)
        return df

    def get_moving_averages(self, symbol, time_frame=None):
        symbol = symbol.lower().replace('_', '-')
        resp = self._session.get("https://www.investing.com/currencies/{symbol}-technical".format(symbol=symbol),
                                 headers={'User-agent': 'Google Chrome'})

        soup = BeautifulSoup(resp.content, 'html.parser')
        table = soup.find("table", {"class": "movingAvgsTbl"})
        table_rows = [[td.text for td in row.find_all("td")] for row in table.find_all("tr")[1:-1]]

        # get headers for dataframe
        table_headers = [th.text for th in table.find_all("th")]

        # build df from tableRows and headers
        df = pd.DataFrame(table_rows, columns=table_headers)
        df['Simple'] = df['Simple'].apply(
            lambda x: x.strip().replace('\t', '').replace('\n', '').replace('Sell', '').replace('Buy', ''))
        df['Exponential'] = df['Exponential'].apply(
            lambda x: x.strip().replace('\t', '').replace('\n', '').replace('Sell', '').replace('Buy', ''))
        return df

    def get_economic_calendar(self, start_date=None, end_date=None, symbol=None):
        """
        Check calendar date
        :param date:
        :param start_date:
        :param end_date:
        :return:
        """
        resp = self._session.get("https://www.investing.com/economic-calendar/",
                                 headers={'User-agent': 'Google Chrome'})

        soup = BeautifulSoup(resp.content, 'html.parser')

        table = soup.find("table", {"id": "economicCalendarData"})
        # get headers for dataframe
        table_headers = ['date', 'country', 'event', 'volatility', 'sentiment']
        table_rows = table.find_all("tr")
        tz = pytz.timezone("Australia/Melbourne")
        rows = []
        for row in table_rows[3:]:
            tds = row.find_all("td")
            date = tds[0].text
            date = date if date not in ['All Day', 'Tentative'] else None
            if date is not None:
                date = "%s %s" % (datetime.datetime.now().strftime('%Y-%m-%d'), date)
            country = tds[1].text
            volatility = tds[2].attrs.get('title')
            event = tds[3].text.strip()
            try:
                sentiment = tds[4].attrs.get('title')
                if 'in line' in sentiment.lower():
                    sentiment = 'in line'
                elif 'worse' in sentiment.lower():
                    sentiment = 'worse'
                elif 'better' in sentiment.lower():
                    sentiment = 'better'
            except IndexError:
                sentiment = None
            rows.append([date, country, event, volatility, sentiment])

        df = pd.DataFrame(rows, columns=table_headers)
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d %H:%M') + pd.DateOffset(hours=6)
        return df


if __name__ == '__main__':
    o = OnlineMetrics()
    # p = o.get_chistorical_data(symbol='EUR_USD')
    # print p
    # p = o.get_technical_summary(symbol='EUR_USD')
    # print o.get_moving_averages('EUR_USD')
    indicators = o.get_technical_indicators('EUR_USD')
    import re
    pattern = re.compile("Buy:.*Sell:.*Neutral:.*Summary:(.*)")
    name = indicators.iloc[12]['Name']
    match = pattern.match(name)
    print(match.group(1))