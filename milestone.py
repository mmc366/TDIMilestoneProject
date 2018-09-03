# -*- coding: utf-8 -*-
"""
Created on Sat Aug 18 16:06:07 2018

@author: Meghan
"""
import requests
import json
import pandas as pd
from datetime import datetime, date
from bokeh.plotting import figure, output_file, show

#Step 2: Get data from API and put it in pandas

#api_key=QVzRLQ14MtbdhMhm7UcR
#Request filters for rows: ABT, AMGN, GILD, TMO, ABBV, AGN
#Request filters for columns: ticker, date, close, adj_close, open, adj_open

TICKER_NAMES = ("ABT", "AMGN", "GILD", "TMO", "ABBV", "AGN")

def build_urls(ticker_names=TICKER_NAMES):
    """
    Takes one or more ticker names as a sequence<str> (e.g., ["ABT", "AMGN"]) 
    and builds the Quandl API url for the given ticker(s). 
    Returns the urls as a list<str>.
    
    @ticker_names: sequence<str>
        Default: ("ABT", "AMGN", "GILD", "TMO", "ABBV", "AGN")
    @return: list<str> (urls)
    """
    prefix_url = "https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?ticker="
    suffix_url = "&qopts.columns=ticker,date,close,adj_close,open,adj_open&api_key=QVzRLQ14MtbdhMhm7UcR"
       
    return [prefix_url + ticker + suffix_url for ticker in ticker_names]



def get_response(ticker_url):
    """
    Takes a ticker API url as a str (return from build_urls()) and returns a 
    requests.get responses as a str.
    
    @ticker_url: str (url)
    @return: str (requests.get responses)
    """
    return requests.get(ticker_url).text



def get_result(ticker_response):
    """
    Takes a requests.get responses as a str (return from get_response()) and 
    returns a dict (response results).
    
    @ticker_responses: str (requests.get responses)
    @return: json dict (response results)
    """
    return json.loads(ticker_response)

  

def variable_constructor(ticker_result, colnum=None):
    """
    Takes a json result dict (return from get_result()) and creates a sequence 
    of values based on the specified column number of
    the result using zero indexing (e.g., colnum = 2 will 
    construct a list of the 3rd element in each row of the
    result). If column number is not specified, default is column[0].
    
    @ticker_result: json result dict
    @colnum: int
    @return: list<variable data> (type dependent on data type in column)
    """
    if colnum == None:
        colnum = 0
    
    return [ticker_result['datatable']['data'][i][colnum] for i in range(len(ticker_result['datatable']['data']))]


    
def to_date(list_date_strs):
    """
    Takes a sequence of date strings (in the form "1983-04-06") 
    and returns a list of dates.
    
    @str_: sequence<str> (dates)
    @return: list<datetime.date>
    """
    return [datetime.strptime(date_, "%Y-%m-%d").date() for date_ in list_date_strs]

    

#Creating indicies by date:
def build_index(ticker_name):
    """
    Takes a ticker name as a str and generates a
    list<dates> contained in the result dict for the given ticker
    that will be used as the index for the ticker DataFrames.
    
    @ticker_name: str (ticker name)
    @return: list<datetime.date>    
    """
    for data in ticker_name:    
        return to_date(variable_constructor(get_result(get_response(build_urls([ticker_name])[0])), 1)) 
           
    

#Creating data dicts for each ticker:
def build_data_dict(ticker_name):
    """
    Takes a ticker name as a str and generates a dictionary of data
    based on the result dict for the given ticker. 
    Keys include: "Ticker", "Date", "Close", "Adjusted Close", "Open", 
    "Adjusted Open"    
    
    @ticker_name: str (ticker name)
    @return: dict
    """
    data_dict = {}
    
    keys = ["Ticker", "Date", "Close", "Adjusted Close", "Open", "Adjusted Open"]
    
    data_list = [variable_constructor(get_result(get_response(build_urls([ticker_name])[0])), i) for i in range(6)]
       
    for i in range(6):
        if i == 1:
            data_dict[keys[i]] = to_date(data_list[i])
        else: 
            data_dict[keys[i]] = data_list[i]
    return data_dict
            


#Creating full DataFrames for each ticker:
def build_full_df(ticker_name):
    """
    Takes a ticker name as a str and generates a DataFrame for the
    given ticker where index consists of dates and columns consist
    of variables defined in build_data_dict(). This DataFrame includes
    all dates in the ticker's result dict.
    
    @ticker_name: str (ticker name)
    @return: pd DataFrame
    """
    return pd.DataFrame(build_data_dict(ticker_name), index=build_index(ticker_name))



#Creating truncated DataFrames for each ticker (Jan 2018 data only):
def build_jan18_df(ticker_name):
    """
    Takes a ticker name as a str and generates a DataFrame for the
    given ticker where index consists of dates and columns consist
    of variables defined in build_data_dict(). This DataFrame includes
    only dates in the ticker's result dict between 1/1/18 - 1/31/18 (inclusive).
    
    @ticker_name: str (ticker name)
    @return: pd DataFrame
    """    
    df = build_full_df(ticker_name)
    
    return df.loc[(df["Date"] >= date(2018, 1, 1)) & (df["Date"] <= date(2018, 1, 31))]



#Step 3: Use Bokeh to plot pandas data

#Preparing data for plots:
def plot_coordinates(ticker_name):
    """
    Takes a ticker name as a str and generates the coordinates
    for a plot based on the data in the DataFrame returned by
    build_jan_18_df().
    
    Coordinates include:
        x = Date
        y0 = Close
        y1 = Adjusted Close
        y2 = Open
        y3 = Adjusted Open
    
    @ticker_name: str (ticker name)
    @return: dict of pd Series
    """
    df = build_jan18_df(ticker_name)
    
    return {"x": df.loc[:, "Date"],
            "y0": df.loc[:, "Close"],
            "y1": df.loc[:, "Adjusted Close"],
            "y2": df.loc[:, "Open"],
            "y3": df.loc[:, "Adjusted Open"]}



#Output to static HTML files:
def static_html(ticker_name):
    """
    Takes a ticker name as a str and creates a static
    html output file where plot will be displayed.
    
    @ticker_name: str
    @return: bokeh static html output file
    """
    return output_file(ticker_name + "_ticker_plot.html", title = "Big Pharma Ticker Lookup")


#Creating a new plot:
def create_plot(ticker_name):
    """
    Takes a ticker name as a str and creates a plot figure with 
    a specified title and x-axis label/datetime data type.
    
    @ticker_name: str (ticker name)
    @return: bokeh figure
    """
    return figure(title="Quandl WIKI Stock Prices - " + ticker_name, x_axis_label="Date (January 2018)", x_axis_type="datetime")


#Renders:
def render_plot(ticker_name):
    """
    Takes a ticker name as a str and renders a multi-line plot
    displaying Close, Adjusted Close, Open, and Adjusted Open price
    data for each date in Jaunary 2018 for the given ticker.
    
    @ticker_name: str (ticker name)
    @return: bokeh plot
    """
    static_html(ticker_name)
    plot = create_plot(ticker_name)
    coordinates = plot_coordinates(ticker_name)
    
    #Plots Close line in orange:
    plot.line(coordinates["x"], coordinates["y0"], legend="Close", 
                line_color="orange", line_width=3)
    
    #Plots Adjusted Close line in purple triangles:
    plot.line(coordinates["x"], coordinates["y1"], legend="Adjusted Close", 
                line_color="purple", line_width=1)
    
    plot.triangle(coordinates["x"], coordinates["y1"], legend="Adjusted Close", 
                fill_color="purple", line_color="purple", size=8)
    
    #Plots Open line in blue squares:
    plot.line(coordinates["x"], coordinates["y2"], legend="Open", 
                line_color="blue", line_width=3)
    
    plot.square(coordinates["x"], coordinates["y2"], legend="Open", 
                fill_color="blue", line_color="blue", size=8)
    
    #Plots Adjusted Open line in red circles:
    plot.line(coordinates["x"], coordinates["y3"], legend="Adjusted Open", 
                line_color="red", line_width=1)
    
    plot.circle(coordinates["x"], coordinates["y3"], legend="Adjusted Open", 
                fill_color="red", line_color="red", size=8)
    
    #Customizes legend position:
    plot.legend.location = "top_left"
    
    return show(plot, new="tab")
  

#Main function for application:    
def main():
    urls = build_urls()
       
    for url in urls:
        response = get_response(url)
        get_result(response)
        
    for ticker in TICKER_NAMES:
        build_index(ticker)
        build_data_dict(ticker)
        build_jan18_df(ticker)
        
    return render_plot(ticker)
    
           

if __name__ == "__main__":
    print("Main load successful");