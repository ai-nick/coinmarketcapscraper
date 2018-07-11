import bs4 as bs
import requests
import re
from datetime import date, timedelta, datetime 


class CoinMarketScraper:

    def getExchange(self, exchange):
    resp = requests.get('https://coinmarketcap.com/exchanges/%s/' %(exchange))
    soup = bs.BeautifulSoup(resp.text, "lxml")
    sevenDay = soup.find("div", {"id":"markets" })
    tab = sevenDay.find('table', {"class": "table"})
    rows = tab.findAll('tr')[1:]
    rowNum = []
    name = []
    symbol = []
    volume = []
    price = []
    volP = []
    for row in rows:            #pack lists
        col = row.findAll('td')
        col0 = col[0].text.strip()
        rowNum.append(col0)
        col1= col[1].text.strip()
        name.append(col1)
        col2 = col[2].text.strip()
        symbol.append(col2)
        col3 = col[3].text.strip()
        volume.append(col3)
        col4 = col[4].text.strip()
        price.append(col4)
        col5 = col[5].text.strip()
        volP.append(col5)   
    tableDict = {'row': rowNum, 'name': name, 'symbol': symbol, 'volume': volume, 'price': price, 'volume%': volP}
    df = pd.DataFrame(tableDict)
    return df

def getCryptoGainers(self):
    resp = requests.get('https://coinmarketcap.com/gainers-losers/')
    soup = bs.BeautifulSoup(resp.text)
    sevenDay = soup.find("div", {"id":"gainers-1h" })
    tab = sevenDay.find('table')
    body = tab.find('tbody')
    rows = body.findAll('tr')
    rowNum = []
    name = []
    symbol = []
    volume = []
    price = []
    gains = []
    for row in rows:            #pack lists
        col = row.findAll('td')
        col0 = col[0].text.strip()
        rowNum.append(col0)
        col1= col[1].text.strip()
        name.append(col1)
        col2 = col[2].text.strip()
        symbol.append(col2)
        col3 = col[3].text.strip()
        volume.append(col3)
        col4 = col[4].text.strip()
        price.append(col4)
        col5 = col[5].text.strip()
        gains.append(col5)
    tableDict = {'row': rowNum, 'name': name, 'symbol': symbol, 'volume': volume, 'price': price, 'gains': gains}
    df = pd.DataFrame(tableDict)
    return df
    
# this gives us the right days to pull 3 months of historical data 
# from ccm
  
def three_months_back(self):
    today = datetime.today().strftime('%Y%m%d') 
    backDate = datetime.today() - timedelta(days=90)
    return (today, backDate.strftime('%Y%m%d') )


# pass a coin by name into this, you could run 
# getExchange, loop through the results and get each coins history by 
# passing its name to this method

def getCryptoHist(self, coin):
    dates = three_months_back()
    print(dates)
    url = 'https://coinmarketcap.com/currencies/'+coin+'/historical-data/?start=%s&end=%s' % (dates[1], dates[0])
    print(url)
    resp = requests.get(url)
    soup = bs.BeautifulSoup(resp.text)
    sevenDay = soup.find("div", {"id":"historical-data" })
    tab = sevenDay.find('table')
    body = tab.find('tbody')
    rows = body.findAll('tr')
    date = []
    openPrice = []
    high = []
    low = []
    close = []
    volume = []
    marketCap = []
    for row in rows:            #pack lists
        col = row.findAll('td')
        col0 = col[0].text.strip()
        date.insert(0,col0)
        col1= col[1].text.strip()
        openPrice.insert(0,float(col1))
        col2 = col[2].text.strip()
        high.insert(0,float(col2))
        col3 = col[3].text.strip()
        low.insert(0,float(col3))
        col4 = col[4].text.strip()
        close.insert(0,float(col4))
        col5 = col[5].text.strip()
        col5 = col5.replace(',', '')
        volume.insert(0,int(col5))
        col6 = col[6].text.strip()
        col6 = col6.replace(',', '')
        marketCap.insert(0, int(col6))
    tableDict = {'date': date, 'open': openPrice, 'high': high, 'low': low, 'close': close, 'volume': volume, 'marketCap': marketCap}
    #df = pd.DataFrame(tableDict)
    return tableDict

# this gives all markets the coin is traded in


def getCoinMarkets(self, coin):
    url = 'https://coinmarketcap.com/currencies/'+coin+'/#markets'
    resp = requests.get(url)
    soup = bs.BeautifulSoup(resp.text)
    tab = soup.find('table', {"id": "markets-table"})
    rows = tab.findAll('tr')[1:]
    names = []
    price = []
    for row in rows:
        col= row.findAll('td')
        col0 = col[1].text.strip()
        names.append(col0)
    return names

    


