#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 00:07:25 2022

CRONTAB 6:20am

@author: michaelkwok
"""

global_message = ''

def run_script(production):
    
    # =============================================================================
    # =============================================================================
    # KEYS
    # =============================================================================
    # =============================================================================
    
    script_name = 'SAMPLE'
    contact = not production
    capital = 5000
    account_min = 26000
    account_goal = 50000
    
    # =============================================================================
    # =============================================================================
    # HOUSEKEEPING
    # =============================================================================
    # =============================================================================
        
    def send_email():
        
        sender_email = 
        receiver_email = 
        if contact:
            receiver_email = []
        password = 
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        context = ssl.create_default_context()
        SUBJECT = script_name
        message = 'Subject: {}\n\n{}'.format(SUBJECT, global_message)
        
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
    
    def handle_message(message, append_global=True, print_mess=not production, raise_error=False):
        global global_message, expected_error
        if append_global:
            global_message += message
        if print_mess:
            print(message)
        if raise_error:
            raise ValueError(message)
    
    def sleep_func(wake_time):
        wake = pytz.timezone("US/Pacific").localize(datetime.strptime(wake_time,"%H:%M:%S")).time()
        start = datetime.now(pytz.timezone("US/Pacific")).time()
        sleep_time = (datetime.combine(date.min, wake) - datetime.combine(date.min, start)).seconds
        handle_message(f'\n\nEntering sleep for {sleep_time//3600} hr {int(sleep_time/3600%1*60)} min \
                       {int(sleep_time/3600%1*60%1*60-2)} sec at {datetime.now(pytz.timezone("US/Pacific"))} \
                           PST to {wake_time} PST\n==============================')
        if production:
            time.sleep(sleep_time)
    
    def auth_tda():
        token_path = 'token.json'
        api_key =
        redirect_uri = 'https://127.0.0.1'
        try:
            c = auth.client_from_token_file(token_path, api_key)
        except FileNotFoundError:
            handle_message('\n\nToken path not found, initiating chromedriver creation')
            from selenium import webdriver
            with webdriver.Chrome(executable_path=) as driver:
                c = auth.client_from_login_flow(
                    driver, api_key, redirect_uri, token_path)
            handle_message('\nCode ran fine (please verify)')
        handle_message('\n\nAccount authorized')
        return c
    
    def check_delist(ticker): # TDA
        handle_message(f'\n\ncheck_delist({ticker}) running at \
                       {datetime.now(pytz.timezone("US/Pacific")).time()} PST')
        delisted = c.get_quote(ticker).json()[ticker]['securityStatus'] == 'Halted'
        handle_message(f'\ncheck_delist({ticker}) (result: {delisted}) finished at \
                       {datetime.now(pytz.timezone("US/Pacific")).time()} PST')            
        return delisted
    
    def get_last_price(ticker): # TDA
        handle_message(f'\n\nget_last_price({ticker}) running at \
                       {datetime.now(pytz.timezone("US/Pacific")).time()} PST')
        price = c.get_quote(ticker).json()[ticker]['lastPrice']
        handle_message(f'\nget_last_price({ticker}) (result: {price}) finished at \
                       {datetime.now(pytz.timezone("US/Pacific")).time()} PST')
        return price
    
    def buy_market(ticker, qty):
        handle_message(f'\n\nbuy_market({ticker}, {qty}) running at \
                       {datetime.now(pytz.timezone("US/Pacific")).time()} PST')
        OB = OrderBuilder() # this just becomes a dictionary
        OB.add_equity_leg(EquityInstruction.BUY, ticker, qty)
        OB.set_order_type(OrderType.MARKET)
        OB.set_session(Session.NORMAL)
        OB.set_duration(Duration.DAY)
        OB.set_order_strategy_type(OrderStrategyType.SINGLE)
        c.place_order(account_id, OB.build())
        handle_message(f'\nbuy_market({ticker}, {qty}) finished at \
                       {datetime.now(pytz.timezone("US/Pacific")).time()} PST')
            
    def sell_market(ticker, qty):
        handle_message(f'\n\nsell_market({ticker}, {qty}) running at \
                       {datetime.now(pytz.timezone("US/Pacific")).time()} PST')
        OB = OrderBuilder() # this just becomes a dictionary
        OB.add_equity_leg(EquityInstruction.SELL, ticker, qty)
        OB.set_order_type(OrderType.MARKET)
        OB.set_session(Session.NORMAL)
        OB.set_duration(Duration.DAY)
        OB.set_order_strategy_type(OrderStrategyType.SINGLE)
        c.place_order(account_id, OB.build())
        handle_message(f'\nsell_market({ticker}, {qty}) finished at \
                       {datetime.now(pytz.timezone("US/Pacific")).time()} PST')
    
    import smtplib, ssl
    from datetime import datetime, date
    import pytz
    import time
    import traceback
    
    from tda import auth, client
    from tda.orders.common import EquityInstruction, OrderType, Session, \
        Duration, OrderStrategyType
    from tda.orders.generic import OrderBuilder
    
    from alpaca_trade_api.rest import REST
    import json
    
    import stock_list
    
    try:
    
        handle_message(f'\nRunning {script_name} with production {production} and capital {capital} \
                       at {datetime.now(pytz.timezone("US/Pacific")).time()} PST')
        account_id = 
        tickers = stock_list.tickers
    
        # daylight savings time
        if datetime.now(pytz.timezone("US/Pacific")).tzinfo._dst != 0: # is DST
            handle_message('\n\nDST: true, continuing script')
        else: # is NOT DST
            handle_message('\n\nDST: false, sleeping for 1 hour')
            if production:
                time.sleep(60*60)
                
        # ALPACA API
        headers = json.loads(open("key_real.txt",'r').read())
        trading_url = 'https://api.alpaca.markets'
        trading_api = REST(headers["APCA-API-KEY-ID"], headers["APCA-API-SECRET-KEY"], base_url=trading_url)
        
        # check market open
        if (not trading_api.get_clock().is_open): # note, get_clock is EST
            contact = True
            handle_message('\n\nALERT: Market is currently not open. No trade.', raise_error=production)
            
        # check early close
        if trading_api.get_clock().next_close.time().hour!=16: # note, get_clock is EST
            handle_message(f'\n\nEarly close today: \
                           {trading_api.get_clock().next_close.time().isoformat()} EST. No sleep.')
        else:
            wake_time = '12:38:00'
            sleep_func(wake_time)

    # =============================================================================
    # =============================================================================
    # ENTRY
    # =============================================================================
    # =============================================================================
        
        c = auth_tda()
        notional = round(capital / len(tickers), 2)
        
        for ticker in tickers:
            
            delisted = check_delist(ticker)
            if delisted:
                contact = True
                handle_message(f'\n\nRED ALERT: delisted stock found: {ticker}')
                script_name += ' (RED ALERT DELIST) '
                continue
            
            last_price = get_last_price(ticker)
            qty = notional // last_price
            if qty > 0:
                handle_message(f'\n\nBuying market ${notional} ({qty} shares at last_price {last_price}) \
                               of {ticker} at {datetime.now(pytz.timezone("US/Pacific")).time()} PST')
                if production:
                    buy_market(ticker, qty)
            else:
                handle_message(f'\n\n{ticker} qty is 0, no buy at \
                               {datetime.now(pytz.timezone("US/Pacific")).time()} PST')

    # =============================================================================
    # =============================================================================
    # EXIT
    # =============================================================================
    # =============================================================================
                    
    # (REMOVED)

    # =============================================================================
    # =============================================================================
    # DELIST
    # =============================================================================
    # =============================================================================
        
        c = auth_tda()
        
        for ticker in tickers:
            
            delisted = check_delist(ticker)
            if delisted:
                contact = True
                handle_message(f'\n\nRED ALERT: delisted stock found: {ticker}')
                script_name += f' (RED ALERT DELIST: {ticker}) '
                continue
            
    # =============================================================================
    # =============================================================================
    # ACC BAL
    # =============================================================================
    # =============================================================================
            
        c = auth_tda()
        account = c.get_account(account_id)
        account_bal = account.json()['securitiesAccount']['currentBalances']['liquidationValue']
        # cashBalance is actual cash, liquidationValue is total account
        handle_message(f'\n\nAccount balance: {account_bal}')
        if account_bal < account_min:
            contact = True
            handle_message(f'\n\nRED ALERT: account balance is below {account_min}: {account_bal}')
            script_name += f' (RED ALERT ACC_BAL: {account_bal}) '
        if account_bal > account_goal:
            contact = True
            handle_message(f'\n\nGREEN ALERT: account balance is above {account_goal}: {account_bal}')
            script_name += ' (GREEN ALERT ACC_BAL) '
        
        handle_message('\n\nScript completed, sending email')
        send_email()
        
    except:
        contact = True
        handle_message(f'\n\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\nCode failed and \
                       halted at {datetime.now(pytz.timezone("US/Pacific"))} PST')
        handle_message(f'\nException traceback: \n\n{traceback.format_exc()}')
        script_name += ' (FAILED) '
        send_email()
        
