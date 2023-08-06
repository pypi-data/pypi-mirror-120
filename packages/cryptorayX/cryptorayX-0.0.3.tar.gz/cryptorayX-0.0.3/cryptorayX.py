import requests
from currency_converter import CurrencyConverter

url = "https://api.wazirx.com/api/v2/tickers"
response = dict(requests.get(url).json())

class cryptorayX :

    def price(self,coin,currency):
        
        try:
            currencyObject = CurrencyConverter()
            
            crypto = coin.lower() + "inr"
            currentPrice = float(response[crypto]["last"])
            try:
                price = currencyObject.convert(currentPrice, 'INR', currency.upper(),)
                return price
            except ValueError:
               return (currency + " is invalid.")
        
        except KeyError:
            return (coin + " is invalid.")