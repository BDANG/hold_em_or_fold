# BAO (Bitcoin Arbitrage Opportunities)

SteelHacks 2017 Project  
by Brian Dang, Craig Mazzotta, and Xavier Torgerson

## What is arbitrage?
*"the simultaneous buying and selling of securities, currency, or commodities
in different markets or in derivative forms in order to take advantage of differing
prices for the same asset."*

In terms of bitcoin, arbitrage is taking advantage of the different cost for 1 BTC between two different exchanges.  These differences can net small margins if they are greater than the fees from transfering between exchanges.

The goal of the project is to notify users about bitcoin
arbitrage opportunities based on exchanges they are watching.  It
 accounts for the buy/sell fees for each available exchange, and assumes
 the user has significant equity in both BTC and USD on the exchanges they plan
 to execute an arbitrage.


## Usage
1. To begin using the service, send any message to +1 724-806-1286.
2. Follow prompts to configure notification preferences
  - Exchanges entered as a single string of options.
    - Example: 12345 to sign up for all
  - The arbitrage threshold is the percent difference in the value of bitcoin
  across the different exchanges, taking into account fees for buying/trading.
    - Example: Enter 1.5 for 1.5%
    - Recommended values:
      - Frequent opportunities ~ 3%
      - Less frequent ~ 4%
      - Least frequent ~ 5%


###### Disclaimer: we are not responsible for any monetary losses.

#### Dependencies

- twilio
  - sms messaging
- pandas
  - historical arbitrage analysis
- python request library
  - used for web crawling
- Krakenex API
- BeautifulSoup
  - used for web crawling/scraping along with requests

  If you want to do analysis against historical data look in the backtest/ folder.
