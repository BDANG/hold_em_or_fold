SteelHacks 2017 Project
by Brian Dang, Craig Mazzotta, and Xavier Torgerson

Bitcoin Arbitrage Opportunities (BAO)

Arbitrage is:
"the simultaneous buying and selling of securities, currency, or commodities
in different markets or in derivative forms in order to take advantage of differing
prices for the same asset."

The goal of the project is to notify subscribers about possible bitcoin
arbitrage across the exchanges they personally utilize. It
 accounts for the buy/sell fees for each available exchange, and assumes
 the user has significant equity in both BTC and USD on the exchanges they plan
 to execute an arbitrage.


Usage:
- To begin using the service, send any message to +1 724-806-1286.
- Follow prompts for exchanges and arbitrage threshold
  - Exchanges entered as a single string of options.
    - Example: 12345 to sign up for all
  - The arbitrage threshold is the percent difference in the value of bitcoin
  across the different exchanges, taking into account fees for buying/trading.
    - Example: Enter 1.5 for 1.5%
    - Recommended values:
      - Frequent opportunities ~ 3%
      - Less frequent ~ 4%
      - Least frequent ~ 5%


Disclaimer: we are not responsible for any monetary losses.

Dependencies:

- twilio
  - sms messaging
- pandas
  - historical arbitrage analysis
- python request library
  - used for web crawling
- Krakenex API
- BeautifulSoup
  - used for web crawling/scraping along with requests
