# Quant Portfolio
Samples of real code I wrote and use for personal algorithmic trading activities. The purpose is more so to showcase infrastructure as opposed to share meaningful research findings.

1. My Approach:
    1. overview.txt
    2. pillars_of_truth.txt
2. Research:
    1. utils/alpaca_table2.py: create and maintain stock price datasets in local SQL database via sqlite3
    2. utils/minute_functions.py: functions that assist with researching and backtesting at the minutely-level
    3. selling_option_prem.ipynb: analyze probabilities of ITM/OTM option expiration and associated premiums
    4. top_gainers_effect.ipynb: analyze the following interday gap and intraday change for top gainers
    5. miss_10bestDays.ipynb: verify a statement regarding the 10 best days of the market per decade
3. Deployment:
    1. utils/production_functions.py: functions that assist with production, including order-execution
    2. production_script.py: a generalized production script I use to automate trading strategies

Tools & Technologies:
1. Python/Pandas, SQL, Linux Command Line, Git
2. Alpaca Markets and TD Ameritrade APIs for data and brokerage
3. Amazon Web Services cloud EC2 instance, crontab automation
