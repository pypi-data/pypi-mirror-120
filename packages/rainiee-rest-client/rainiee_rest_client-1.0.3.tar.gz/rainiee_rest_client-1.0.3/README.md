rainiee_decision_engine
===============
* easy to use as most of the data returned are json 

Installation
--------------

    pip install rainiee_rest_client==1.0.3
    from rainiee_rest_client.rest_client import RestClient
    rainiee_client = RestClient(username,password).choice_rainiee_compute().login()

Upgrade
---------------

    pip install rainiee_rest_client==1.0.3 --upgrade

Quick Start
--------------

algorithm 
  
        1: algorithm_solve_vanilla_mvo
              symbol_list = ['300370.sz','300102.sz','300345.sz']
              rainiee_client.algorithm_solve_vanilla_mvo(symbol_list = symbol_list,start_index=7500,end_index = 7530)
        2: algorithm_solve_maximize_sharpe
              symbol_list = ['300370.sz','300102.sz','300345.sz']
              rainiee_client.algorithm_solve_maximize_sharpe(symbol_list = symbol_list,start_index=7500,end_index = 7530)
        3: algorithm_solve_vanilla_mvo_realtime
              symbol_list = ['300370.sz','300102.sz','300345.sz']
              rainiee_client.algorithm_solve_vanilla_mvo_realtime(symbol_list = symbol_list,start_index=7500,end_index = 7530)
        4: monitoring_baseline
              portf = [{'percentage': 1.0, 'symbol': '300547.sz'}, {'percentage': 0.5, 'symbol': '300647.sz'}]
              hold_index = 2530
              hold_period = 5
              rainiee_client.monitoring_baseline(portf,hold_index,hold_period)
        5: cn_stockstats_returns_matrix
              symbol_list =['300370.sz','300102.sz','300345.sz','300341.sz','300806.sz','300249.sz','300727.sz','300373.sz','300808.sz',
              '300474.sz','300805.sz','300803.sz']
              rainiee_client.cn_stockstats_returns_matrix(symbol_list = symbol_list,start_index=7500,end_index = 7530)

        6: trade_execute_order
              rainiee_client.trade_execute_order('300647.sz',2500,'buy',15)
    