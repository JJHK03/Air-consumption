import pandas as pd
import streamlit as st
import yfinance as yf
import altair as alt

st.title('可視化アプリ')

st.sidebar.write("""
                 可視化ツールです。以下のオプションから表示日時を指定""")
st.sidebar.write("""##表示日数選択""")

days = st.sidebar.slider('日数', 1, 50, 20)
st.write(f"""過去**{days}**の株価""")


@st.cache_resource
def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f'{days}d')
        hist.index = hist.index.strftime('%d %B %Y')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = 'Name'
        df = pd.concat([df, hist])
    return df


try:
    st.sidebar.write("""
                    ###株価の範囲指定
                    # """)
    ymin, ymax = st.sidebar.slider('範囲を指定', 0.0, 3500.0,(0.0, 3500.0))


    tickers = {
        'Apple' : 'AAPL',
        'Meta Platforms': 'META',
        'google':'GOOGL',
        'microsoft':'MSFT',
        'netflix':'NFLX',
        'amazon':'AMZN',
    }

    df = get_data(days, tickers)

    companies = st.multiselect('Select companies',list(df.index), )

    if not companies:
        st.error('select a company at least')
    else:
        data = df.loc[companies]
        st.write("###　株価（USD）", data.sort_index())
        data = data.T.reset_index()
        data = pd.melt(data, id_vars = ['Date'],value_name='Stock Prices(USD)')
        chart = (alt.Chart(data)
                .mark_line(opacity= 0.8, clip = True)
                .encode(
                    x= "Date:T", y= alt.Y("Stock Prices(USD):Q",stack = None),color ='Name:N'))
        st.altair_chart(chart, use_container_width=True)

except:
    st.error("Oh,,error")