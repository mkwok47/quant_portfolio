# Portfolio
Samples of code I wrote and use for personal algorithmic trading activities. Main APIs I work with are Alpaca and TDA. I intentionally leave out novel / useful findings for obvious reasons.

Data Functionalities:
1. minute_functions.py: functions that assist with researching and backtesting at the minutely-level
2. alpaca_table2.py: create and maintain stock price datasets (primarily at the minutely-level) in local SQL database via sqlite3

Research:
1. selling_option_prem.ipynb: analyze probabilities of ITM/OTM option expiration and associated premiums
2. top_gainers_effect.ipynb: analyze the following interday gap (if any) and intraday change following a day of high gain for top gainers
3. miss_10bestDays.ipynb: verify a reported statement that if you miss out on the 10 best days of the market per decade since 1930, then your overall return would just be 28%

Deployment:
1. production_script: sample production logic including sleep-time logic, error-handling, emailing, and housekeeping checks (daylight time savings, market open, early close, account balance); Deployed on Amazon Web Services (AWS) cloud EC2 instance, scheduled via crontab.
