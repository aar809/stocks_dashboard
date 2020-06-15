from flask import Flask, render_template,request
import plotly
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import json
import yfinance as yf


app = Flask(__name__)

# sample_df = pd.read_csv("data/hsi.csv")
# gspc = pd.read_csv("data/gspc.csv")
# dji = pd.read_csv("data/dji.csv")
# ixic = pd.read_csv("data/ixic.csv")
# msft = yf.Ticker("^GSPC")
# stock = msft.history(period="max")

symbol = ""


@app.route('/', methods = ["GET","POST"])
def index():
	if request.method == "POST":
		stock="GOOG"
		stock2="GOOG"
		feature="Line"
		stock = request.form.get("symbol")
		timeframe = request.form.get("timeframe")
		feature = request.form.get("feature")
		bar = create_plot(feature, stock, timeframe)
		stock2 = request.form.get("symbol2")
		bar2 = create_plot(feature, stock2, timeframe)
		stock = stock.upper()
		df0 = yf.Ticker(stock)
		holders = df0.institutional_holders
		info = df0.info
		return render_template('index.html', plot=bar, stock=stock, stock2=stock2, plot2=bar2,timeframe=timeframe, tables=[holders.to_html(classes='data', header="true")], **info)

	else:
		stock = "^GSPC"
		feature = 'Line'
		timeframe="24mo"
		bar = create_plot(feature, stock, timeframe)
		return render_template('index.html', plot=bar, stock=stock)

# @app.route('/homepage')
# def homepage():
#     return render_template('homepage.html')

# @app.route('/plot', methods=["GET", "POST"])
# def index():
# 	symbol = request.form.get("symbol")
# 	#write the API line to retrieve JSON object response from IEX based on user's input of stock ticker.
# 	bar = create_plot()
# 	return render_template('index.html', plot=bar, symbol=symbol)

def create_plot(feature, stock, timeframe):
	if feature == 'Line':
		# N = 40
		# x = np.linspace(0, 1, N)
		# y = np.random.randn(N)
		# df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe
		# df = pd.read_csv(f'data/{stock}.csv')
		df0 = yf.Ticker(stock)
		df = df0.history(period=timeframe)
		# df["Volatility"] = df["Close"] - df["Open"]
		# df["Change"] = df["Close"] - df["Close"].shift(1)
		# df["PercentChange"] = (df["Close"] - df["Close"].shift(1))/df["Close"].shift(1)*100
		data = [
			go.Line(
				x=df.index, # assign x as the dataframe column 'x'
				y=df.iloc[:,3],
				name = stock
		)]
	
	elif feature == "Scatter":
		# N = 1000
		# random_x = np.random.randn(N)
		# random_y = np.random.randn(N)
		# random_x = [1,2,3,4,5]
		# random_y = [1,2,3,4,5]
		# df = pd.read_csv(f'data/{stock}.csv')
		# random_x = sample_df.iloc[:,0]
		# random_y = sample_df.iloc[:,5]
		
		df0 = yf.Ticker(stock)
		df = df0.history(period="12mo")
		random_x = df.index
		random_y = df.iloc[:,3]

        # Create a trace
		data = [go.Scatter(
			x = random_x,
			y = random_y,
			mode = 'markers'
		)]


	elif feature =="Percentage Change":
		df0 = yf.Ticker(stock)
		df = df0.history(period=timeframe)
		# df["Volatility"] = df["Close"] - df["Open"]
		# df["Change"] = df["Close"] - df["Close"].shift(1)
		df["PercentChange"] = (df["Close"] - df["Close"].shift(1))/df["Close"].shift(1)*100
		data = [
			go.Line(
				x=df.index, # assign x as the dataframe column 'x'
				y=df.iloc[:,7],
				name = stock
		)]

	elif feature == "Experiment":
		df0 = yf.Ticker(stock)
		df = df0.history(period=timeframe)
		# df["Volatility"] = df["Close"] - df["Open"]
		# df["Change"] = df["Close"] - df["Close"].shift(1)
		# df["PercentChange"] = (df["Close"] - df["Close"].shift(1))/df["Close"].shift(1)*100
		data = [
			go.Line(
				x=df.index, # assign x as the dataframe column 'x'
				y=df.iloc[:,3],
				name = stock
		)]

	else:
		df0 = yf.Ticker(stock)
		df = df0.history(period=timeframe)
		data = [
			go.Line(
				x=df.index, 
				y=df.iloc[:,3],
				name = stock
		)]

	graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
	return graphJSON	

@app.route('/bar', methods=['GET', 'POST'])
def change_features():

	feature = request.args['selected']
	graphJSON= create_plot(feature)

	return graphJSON




if __name__ == '__main__':
	app.run()