Quick guide on how to use historical_analysis.py

1. Obtain the .csv's from: http://api.bitcoincharts.com/v1/csv/
    - Specifically:
        - bitfinexUSD.csv
        - bitstampUSD.csv
        - krakenUSD.csv
        - btceUSD.csv

2. Edit the CSV_DIR in historical_analysis.py to point to the directory
containing the .csv's

3. The other globals at the top of historical_analysis.py that you can manipulate:
    - Exchange List: change which exchanges you want to check for arbitrage history
    - Threshold: the minimum arbitrage % that should be reported
    - Skips: every nth entry in the csv can be skipped for faster data analysis
    - Future check: a time into the future of a given arbitrage to check for profit securing.
    - Saving the list of arbitrages and dataframes
    - Loading the list of arbitrage and dataframes


- The global TOTAL_ARB variable is a list of arbitrage objects that hold the metadata. Iterate the list for analysis.
