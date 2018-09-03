# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 09:33:41 2018

@author: Meghan
"""
from milestone import build_urls, get_response, get_result, variable_constructor, to_date, build_index, build_data_dict, build_full_df, build_jan18_df, plot_coordinates
from datetime import datetime, date

#This module contains all tests for functions defined in milestone.py.

#Tests build_urls()
def build_urlsTest():
    assert ["https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?ticker=ABT&qopts.columns=ticker,date,close,adj_close,open,adj_open&api_key=QVzRLQ14MtbdhMhm7UcR"] == build_urls(["ABT"])
    assert ["https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?ticker=GILD&qopts.columns=ticker,date,close,adj_close,open,adj_open&api_key=QVzRLQ14MtbdhMhm7UcR",
            "https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?ticker=TMO&qopts.columns=ticker,date,close,adj_close,open,adj_open&api_key=QVzRLQ14MtbdhMhm7UcR"] == build_urls(("GILD", "TMO"))


#Tests get_response()
def get_responseTest():
    assert 500000 < len(get_response(build_urls(["ABT"])[0]))


#Tests get_result()
def get_resultTest():
    assert 2 == len(get_result(get_response(build_urls(["AGN"])[0]))) 


#Tests variable_constructor()    
def variable_constructorTest():
    assert 1000 < len(variable_constructor(get_result(get_response(build_urls(["ABBV"])[0]))))
    assert "ABBV" == variable_constructor(get_result(get_response(build_urls(["ABBV"])[0])))[0]


#Tests to_date()
def to_dateTest():
    assert [date(1983, 4, 6), date(2000, 1, 31)] == to_date(["1983-04-06", "2000-01-31"])


#Tests build_index()    
def build_indexTest():
    assert date(1983, 4, 6) == build_index("ABT")[-1]
    
    
#Tests build_data_dict()
def build_data_dictTest():
    assert "GILD" == build_data_dict("GILD")["Ticker"][0]
    assert date(2018, 3, 27) == build_data_dict("GILD")["Date"][0]
    assert 6 == len(build_data_dict("GILD"))
    
    
#Tests build_full_df()
def build_full_dfTest():
    assert (1316, 6) == build_full_df("ABBV").shape
    assert date(2017, 10, 27) == build_full_df("ABBV")["Date"][100]
    
    
#Tests build_jan18_df()  
def build_jan18_dfTest():
    assert 21 == len(build_jan18_df("AMGN"))
    assert date(2018, 1, 31) == build_jan18_df("TMO")["Date"].max()
    assert date(2018, 1, 2) == build_jan18_df("ABBV")["Date"].min()
    
    
#Tests plot_coordinates()  
def plot_coordinatesTest():
    assert 62.439999999999998 == plot_coordinates("ABT")["y0"][1]
    assert 5 == len(plot_coordinates("GILD"))
    assert date(2018, 1, 31) == plot_coordinates("TMO")["x"][0]
    assert date(2018, 1, 2) == plot_coordinates("AMGN")["x"][20]


#Tests all test functions in milestone_test.py    
def run_all_tests():
    """
    Runs all test functions contained in milestone_test.py,
    printing individual test status updates to console.
    
    @return: "All tests passed successfully." (if no exceptions thrown)
    """
    tests = [build_urlsTest(), get_responseTest(), get_resultTest(),
    variable_constructorTest(), to_dateTest(), build_indexTest(),
    build_data_dictTest(), build_full_dfTest(), build_jan18_dfTest(),
    plot_coordinatesTest()]
             
    g = (i for i in range(len(tests))) #generator expression        
       
    for test in tests:
        
        start_statement = "Starting test # "+ str(next(g)) + "...."
        end_statement = "Test passed!"
        
        print(start_statement)
        test
        print(end_statement)
    
    return "All tests passed successfully."
    