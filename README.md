# Quant Portfolio
Samples of real code I wrote and use for personal algorithmic trading activities. The purpose is more so to showcase infrastructure as opposed to share meaningful research findings.

1. My Approach:
    1. overview.txt
    2. pillars_of_truth.txt
2. Research:
    1. utils/alpaca_table2.py: create and maintain stock price datasets in local SQL database via sqlite3
    2. utils/minute_functions.py: functions that assist with researching and backtesting at the minutely-level
    3. selling_option_prem.ipynb: analyze probabilities of ITM/OTM option expiration and associated premiums
    4. top_gainers_effect.ipynb: analyze the following interday gap and intraday change following a day of high gain for top gainers
    5. miss_10bestDays.ipynb: verify a reported statement that if you miss out on the 10 best days of the market per decade since 1930, then your overall return would just be 28%
3. Deployment:
    1. utils/production_functions.py: functions that assist with production, including order-execution and emailing
    2. production_script.py: a generalized, sample production script I use to automate a trading strategy via brokerage in the cloud

Tools & Technologies:
1. Python/Pandas, SQL, Linux CLI, Git
2. Alpaca Markets and TD Ameritrade APIs for data and brokerage
3. Amazon Web Services (AWS) cloud EC2 instance, crontab automation
