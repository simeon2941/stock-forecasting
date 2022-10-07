from tracemalloc import start
import streamlit as st
import yfinance as yf
import pandas as pd
#from fbprophet.plot import plot_plotly
import cufflinks as cf
import datetime
import pandas as pd
from prophet import Prophet


st.markdown('''
# Stock Analysis App
''')
st.write('---')

#Sidebar

st.sidebar.subheader('Query Params')
start_date = st.sidebar.date_input("Start date", datetime.date(2019,1,1))
end_date = st.sidebar.date_input("End date", datetime.date.today())

#Retrive Ticker info
ticker_list = pd.read_csv('S&P500-Symbols.csv')
tickerSymbol = st.sidebar.selectbox('Stock ticker', ticker_list) # Select ticker symbol
tickerData = yf.Ticker(tickerSymbol) # Get ticker data
tickerDf = tickerData.history(period='1d', start=start_date, end=end_date) #get the historical prices for this ticker

# Ticker information
string_logo = '<img src=%s>' % tickerData.info['logo_url']
st.markdown(string_logo, unsafe_allow_html=True)

string_name = tickerData.info['longName']
st.header('**%s**' % string_name)

# string_summary = tickerData.info['longBusinessSummary']
# st.info(string_summary)

# Ticker data
st.header('**Ticker data**')
st.checkbox("Use container width", value=False, key="use_container_width")
st.write(tickerDf,  use_container_width=st.session_state.use_container_width)

# # Bollinger bands
st.header('**Bollinger Bands**')
qf=cf.QuantFig(tickerDf,title='First Quant Figure',legend='top',name='GS')
qf.add_bollinger_bands()
fig = qf.iplot(asFigure=True)
st.plotly_chart(fig)

# #  fbProphet
df = tickerData.history(period='1d', start=start_date, end=end_date)#[['Date','Open']]


df = pd.DataFrame()

df['ds'] = tickerDf.index
df['y'] = tickerDf['Open'].values

st.write(df.head())

m = Prophet()
m.fit(df)
future = m.make_future_dataframe(365, freq='h')
forecast = m.predict(future)

# Show and plot forecast
st.subheader('Forecast data')

st.write(f'Forecast data')

st.write(m.plot(forecast))

st.write(m.plot_components(forecast))



####
st.write('---')
st.write(tickerData.info)
