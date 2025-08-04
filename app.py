import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

st.set_page_config(page_title="H1 EMA20 Triggers by Index", layout="centered")
st.title("H1 EMA20 Cross-Up Triggers for Daily AO < 0")

# -- INDEX DEFINITIONS ------------------------------------------------------
INDEX_TICKERS = {
    "S&P 100": [
        "NVDA", "MSFT", "AAPL", "AMZN", "GOOG", "META", "AVGO", "TSLA", "JPM", "WMT",
        "LLY", "V", "ORCL", "NFLX", "MA", "XOM", "COST", "JNJ", "PG", "HD",
        "BAC", "ABBV", "PLTR", "KO", "PM", "UNH", "CSCO", "IBM", "WFC", "CVX",
        "GE", "TMUS", "CRM", "ABT", "MS", "AMD", "AXP", "LIN", "DIS", "INTU",
        "GS", "NOW", "MRK", "MCD", "T", "UBER", "TXN", "RTX", "BX", "CAT",
        "ISRG", "ACN", "BKNG", "PEP", "VZ", "QCOM", "BA", "SCHW", "BLK", "ADBE",
        "SPGI", "C", "AMGN", "TMO", "AMAT", "HON", "BSX", "NEE", "SYK", "PGR",
        "GEV", "PFE", "DHR", "UNP", "ETN", "GILD", "COF", "TJX", "MU", "DE",
        "PANW", "CMCSA", "ANET", "LRCX", "CRWD", "LOW", "ADP", "KKR", "KLAC", "ADI",
        "VRTX", "COP", "APH", "MDT", "CB", "NKE", "SBUX", "LMT", "MMC", "ICE",
    ],
    "FTSE 100": [
        # Add your FTSE 100 tickers here, e.g. 'HSBA.L', 'BP.L', ...
        'III.L', 'ADM.L', 'AAF.L', 'ALW.L', 'AAL.L', 'ANTO.L', 'AHT.L', 'ABF.L', 'AZN.L', 'AUTO.L',
        'AV.L',  'BAB.L', 'BA.L',  'BARC.L','BTRW.L','BEZ.L', 'BKG.L','BP.L',  'BATS.L','BT-A.L',
        'BNZL.L','CNA.L','CCEP.L','CCH.L','CPG.L','CTEC.L','CRDA.L','DCC.L','DGE.L','DPLM.L',
        'EDV.L','ENT.L','EZJ.L','EXPN.L','FCIT.L','FRES.L','GAW.L','GLEN.L','GSK.L','HLN.L',
        'HLMA.L','HIK.L','HSX.L','HWDN.L','HSBA.L','IHG.L','IMI.L','IMB.L','INF.L','ICG.L',
        'IAG.L','ITRK.L','JD.L','KGF.L','LAND.L','LGEN.L','LLOY.L','LMP.L','LSEG.L','MNG.L',
        'MKS.L','MRO.L','MNDI.L','NG.L',  'NWG.L','NXT.L','PSON.L','PSH.L','PSN.L','PHNX.L',
        'PCT.L','PRU.L','RKT.L','REL.L','RTO.L','RMV.L','RIO.L','RR.L', 'SGE.L','SBRY.L',
        'SDR.L','SMT.L','SGRO.L','SVT.L','SHEL.L','SMIN.L','SN.L','SPX.L','SSE.L','STAN.L',
        'STJ.L','TW.L',  'TSCO.L','ULVR.L','UU.L', 'UTG.L','VOD.L','WEIR.L','WTB.L','WPP.L',
    ],
    "STOXX 50": [
        # Add your EURO STOXX 50 tickers here
        'ADS.DE', 'ADYEN.AS', 'AD.AS', 'AI.PA', 'AIR.PA', 'ALV.DE', 'ABI.BR', 'ASML.AS', 'CS.PA', 'BAS.DE',
        'BAYN.DE', 'BBVA.MC', 'SAN.MC', 'BMW.DE', 'BNP.PA', 'BN.PA', 'DB1.DE', 'DHL.DE', 'DTE.DE', 'ENEL.MI',
        'ENI.MI', 'EL.PA', 'RACE.MI', 'FLTR.L', 'RMS.PA', 'IBE.MC', 'ITX.MC', 'IFX.DE', 'INGA.AS', 'ISP.MI',
        'KER.PA', 'OR.PA', 'MC.PA', 'MBG.DE', 'MUV2.DE', 'NOKIA.HE', 'NDA-FI.HE', 'RI.PA', 'PRX.AS', 'SAF.PA',
        'SGO.PA', 'SAN.PA', 'SAP.DE', 'SU.PA', 'SIE.DE', 'STLAM.MI', 'TTE.PA', 'DG.PA', 'UCG.MI', 'VOW.DE',
    ],
    "CAC 40": [
        # Add your CAC 40 tickers here
        'AC.PA', 'AI.PA', 'AIR.PA', 'MT.AS', 'CS.PA', 'BNP.PA', 'EN.PA', 'CAP.PA', 'CA.PA', 'ACA.PA',
        'BN.PA', 'DSY.PA', 'EDEN.PA', 'ENGI.PA', 'EL.PA', 'ERF.PA', 'RMS.PA', 'KER.PA', 'OR.PA', 'LR.PA',
        'MC.PA', 'ML.PA', 'ORA.PA', 'RI.PA', 'PUB.PA', 'RNO.PA', 'SAF.PA', 'SGO.PA', 'SAN.PA', 'SU.PA',
        'GLE.PA', 'STLA.PA', 'STM.PA', 'TEP.PA', 'HO.PA', 'TTE.PA', 'URW.PA', 'VIE.PA', 'DG.PA', 'VIV.PA',
    ],
    "DAX 40": [
        # Add your DAX 40 tickers here
        'ADS.DE', 'AIR.PA', 'ALV.DE', 'BAS.DE', 'BAYN.DE', 'BEI.DE', 'BMW.DE', 'BNR.DE', 'CBK.DE', 'CON.DE',
        '1COV.DE', 'DTG.DE', 'DBK.DE', 'DB1.DE', 'DHL.DE', 'DTE.DE', 'EOAN.DE', 'FRE.DE', 'FME.DE', 'HNR1.DE',
        'HEI.DE', 'HEN3.DE', 'IFX.DE', 'MBG.DE', 'MRK.DE', 'MTX.DE', 'MUV2.DE', 'P911.DE', 'PAH3.DE', 'QIA.DE',
        'RHM.DE', 'RWE.DE', 'SAP.DE', 'SRT3.DE', 'SIE.DE', 'ENR.DE', 'SHL.DE', 'SY1.DE', 'VOW3.DE', 'VNA.DE',
        'ZAL.DE'
    ],
    "NIKKEI 225": [
        # Add your Nikkei 225 tickers here
        '7203.T', '8306.T', '6758.T', '6501.T', '9984.T', '7974.T', '8316.T', '9983.T', '6861.T', '8035.T',
        '9432.T', '6098.T', '8766.T', '4519.T', '7011.T', '8058.T', '8001.T', '9434.T', '8411.T', '9433.T',
        '4063.T', '8031.T', '6857.T', '2914.T', '4502.T', '4568.T', '6503.T', '7741.T', '7267.T', '6702.T',
        '6701.T', '6902.T', '6367.T', '6146.T', '4661.T', '3382.T', '8002.T', '8725.T', '8053.T', '6301.T',
    ],
}

DAYS_LOOKBACK = 60

# -- UTILITIES --------------------------------------------------------------
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i+n]


def calculate_ao(median_df: pd.DataFrame) -> pd.DataFrame:
    """
    Awesome Oscillator: SMA5(median_price) - SMA34(median_price)
    median_df should be a DataFrame where each column is (High+Low)/2 for a ticker.
    """
    sma5  = median_df.rolling(window=5,  min_periods=5).mean()
    sma34 = median_df.rolling(window=34, min_periods=34).mean()
    ao    = sma5 - sma34
    ao.index = ao.index.date  # convert to dates for easy lookup
    return ao

@st.cache_data(ttl=86400)
def get_ticker_names(tickers):
    names = {}
    for t in tickers:
        try:
            info = yf.Ticker(t).info
            names[t] = info.get('longName') or info.get('shortName') or t
        except Exception:
            names[t] = t
    return names

@st.cache_data(ttl=3600)
def fetch_daily_ao(tickers, days):
    df = yf.download(tickers, period=f"{days}d", interval="1d",
                     progress=False, auto_adjust=False)
    if isinstance(df.columns, pd.MultiIndex):
        median = (df['High'] + df['Low']) / 2
    else:
        median = pd.DataFrame({tickers[0]: (df['High'] + df['Low'])/2})
    ao = calculate_ao(median)
    return ao

@st.cache_data(ttl=1800)
def find_h1_triggers(tickers, days, daily_ao):
    triggers = []
    for batch in chunks(tickers, 10):
        h1 = yf.download(
            batch,
            period=f"{days}d",
            interval="1h",
            progress=False,
            auto_adjust=False
        )
        # flatten multiindex if present
        if isinstance(h1.columns, pd.MultiIndex):
            # columns: (feature, ticker)
            close = h1['Close']
        else:
            close = pd.DataFrame(h1['Close'])
        # for each ticker in this batch
        for t in batch:
            if t not in close.columns:
                continue
            series = close[t]
            if series.empty or len(series) < 21:
                st.warning(f"Not enough H1 data for {t}, skipping.")
                continue
            ema20 = series.ewm(span=20, adjust=False).mean()
            prev_close = series.shift(1)
            prev_ema   = ema20.shift(1)
            cross_up = (prev_close < prev_ema) & (series > ema20)
            for idx in series.index[cross_up]:
                # drop tz info
                dt = idx.tz_localize(None)
                date = dt.date()
                if date in daily_ao.index and daily_ao.at[date, t] < 0:
                    triggers.append({
                        'Date':   date,
                        'Time':   dt.time(),
                        'Ticker': t,
                        'Price':  round(series.at[idx], 4)
                    })
    return pd.DataFrame(triggers)

# -- MAIN ANALYSIS FUNCTION ------------------------------------------------
def run_analysis(tickers):
    daily_ao = fetch_daily_ao(tickers, DAYS_LOOKBACK)
    negative = [t for t in tickers if t in daily_ao.columns and daily_ao[t].iloc[-1] < 0]
    st.write(f"Tickers with latest Daily AO < 0 ({len(negative)} of {len(tickers)}): {', '.join(negative)}")
    df_triggers = find_h1_triggers(negative, DAYS_LOOKBACK, daily_ao)

    if df_triggers.empty:
        st.info("No H1 EMA20 cross-up triggers found…")
    else:
        uniq = df_triggers['Ticker'].unique().tolist()
        name_map = get_ticker_names(uniq)
        df_triggers['Name'] = df_triggers['Ticker'].map(name_map)
        st.subheader("H1 EMA20 Cross-Up Triggers (Daily AO < 0)")
        st.dataframe(
            df_triggers
              .loc[:, ['Date', 'Time', 'Ticker', 'Name', 'Price']]
              .sort_values(['Date','Time','Ticker'])
              .reset_index(drop=True)
        )

def show_ao_summary():
    summary = pd.DataFrame()
    days = 20

    for index_name, tickers in INDEX_TICKERS.items():
        ao = fetch_daily_ao(tickers, DAYS_LOOKBACK)
        # For each day, count how many tickers had AO < 0
        count_series = (ao[tickers] < 0).sum(axis=1).rename(index_name)
        summary[index_name] = count_series

    # Keep only the most recent 20 days
    summary = summary.tail(days)
    summary.index.name = "Date"
    
    st.dataframe(summary)
    
    csv = summary.to_csv(index=True).encode("utf-8")
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="ao_negative_summary.csv",
        mime="text/csv"
    )

# -- SIDEBAR INDEX BUTTONS --------------------------------------------------
st.sidebar.header("Run Analysis by Index")
for idx_name, idx_tickers in INDEX_TICKERS.items():
    if st.sidebar.button(idx_name):
        st.header(f"Results for {idx_name}")
        run_analysis(idx_tickers)

st.sidebar.markdown("---")
if st.sidebar.button("Show AO<0 Summary"):
    st.header("Daily AO < 0 Count Summary (Last 20 Days)")
    show_ao_summary()

