# Quant Portfolio
Samples of real code I wrote and use for personal algorithmic trading activities. The purpose of the code shared is more so to exhibit infrastructure at a higher level as opposed to sharing novel research findings.

My Approach:
1. overview.txt
2. pillars_of_truth.txt

Data Functionalities:
1. minute_functions.py: functions that assist with researching and backtesting at the minutely-level
2. alpaca_table2.py: create and maintain stock price datasets (primarily at the minutely-level) in local SQL database via sqlite3

Research:
1. selling_option_prem.ipynb: analyze probabilities of ITM/OTM option expiration and associated premiums
2. top_gainers_effect.ipynb: analyze the following interday gap and intraday change following a day of high gain for top gainers
3. miss_10bestDays.ipynb: verify a reported statement that if you miss out on the 10 best days of the market per decade since 1930, then your overall return would just be 28%

Deployment:
1. production_script.py: a real production script I used to automate a trading strategy via brokerage in the cloud; includes order-execution, sleep-time logic, error-handling, emailing, and housekeeping-checks (e.g. daylight time savings)

Main Tools & Technologies:
1. Python, SQL, Linux Command Line Interface (CLI), Git
2. Alpaca Markets and TD Ameritrade APIs for data and brokerage
3. Amazon Web Services (AWS) cloud EC2 instance, crontab automation
