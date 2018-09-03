from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template('index.html')
    
    else: #Request was a POST
        
        if request.form["ticker_select"] == "ABT":
            return render_template('ABT_ticker_plot.html')
        
        if request.form["ticker_select"] == "AMGN":
            return render_template('AMGN_ticker_plot.html')
        
        if request.form["ticker_select"] == "GILD":
            return render_template('GILD_ticker_plot.html')
        
        if request.form["ticker_select"] == "TMO":
            return render_template('TMO_ticker_plot.html')
        
        if request.form["ticker_select"] == "ABBV":
            return render_template('ABBV_ticker_plot.html')
        
        if request.form["ticker_select"] == "AGN":
            return render_template('AGN_ticker_plot.html')
        
        else:
            return "Not a valid ticker selection. Please try again."
        
@app.route('/about') #Shows which code to run
def about():
  return render_template('about.html')

if __name__ == '__main__':
  app.run(port=33507, debug=True)

#App running at http://127.0.0.1:33507 (index.html)
#App running at http://127.0.0.1:33507/about (about.html)