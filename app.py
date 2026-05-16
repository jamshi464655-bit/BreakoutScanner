import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="SwingPro Breakout", layout="wide")

URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSsnZ6oD_zaP3JLOVaAbR1ZTzn2TVQ26agPr_G89Iey669ijjuJnwgbiaJDtdBiF1ixVyZ0gtfTA1e8/pub?output=csv"

def analyze_breakout(symbol):
    try:
        ticker = f"{symbol}.NS"
        df = yf.download(ticker, period="6mo", interval="1d", progress=False)
        
        if df.empty or len(df) < 20: 
            return None

        # Multi-Index കോളം പ്രശ്നം പരിഹരിക്കുന്നു
        close_series = df['Close'].squeeze()
        volume_series = df['Volume'].squeeze()
        
        if close_series.empty or len(close_series) < 20:
            return None

        # 1. BOLLINGER BANDS (പാണ്ഡാസ് ഉപയോഗിച്ച് നേരിട്ട് കണക്കാക്കുന്നു)
        ma20 = close_series.rolling(window=20).mean()
        std20 = close_series.rolling(window=20).std()
        
        upper_band = ma20.iloc[-1] + (2 * std20.iloc[-1])
        lower_band = ma20.iloc[-1] - (2 * std20.iloc[-1])
        ltp = close_series.iloc[-1]

        # 2. VOLUME AVERAGE
        current_vol = volume_series.iloc[-1]
        avg_vol = volume_series.tail(10).mean()
        
        # 3. RSI (പാണ്ഡാസ് ഉപയോഗിച്ച് നേരിട്ട് കണക്കാക്കുന്നു)
        delta = close_series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        
        rs = gain / loss if loss.iloc[-1] != 0 else None
        rsi = 100 - (100 / (1 + rs.iloc[-1])) if rs is not None else 50
        
        if pd.isna(rsi): 
            rsi = 50

        # Breakout Logic
        status = "⚪ Scanning"
        if ltp > upper_band and current_vol > avg_vol:
            if rsi > 60:
                status = "🚀 STRONG BREAKOUT"
            else:
                status = "📈 BREAKOUT"
        elif ltp < lower_band:
            status = "📉 BREAKDOWN"

        return {
            "Stock": symbol,
            "LTP": round(float(ltp), 2),
            "RSI": round(float(rsi), 2),
            "Signal": status
        }
    except:
        return None

# UI Design
st.markdown("<h1 style='text-align: center; color: #03A9F4;'>Momentum Breakout Scanner ⚡</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Bollinger Bands ഉപയോഗിച്ച് ബ്രേക്ക്ഔട്ട് സംഭവിക്കുന്ന സ്റ്റോക്കുകളെ കണ്ടെത്തുന്നു.</p>", unsafe_allow_html=True)

if st.button('🚀 സ്കാനിംഗ് തുടങ്ങുക'):
    try:
        sheet_df = pd.read_csv(URL)
        symbols = sheet_df['Symbol'].dropna().unique().tolist()
        
        scan_symbols = symbols[:60] 
        total_stocks = len(scan_symbols)
        
        results = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, s in enumerate(scan_symbols):
            status_text.text(f"Scanning ({i+1}/{total_stocks}): {s}")
            res = analyze_breakout(s)
            if res: 
                results.append(res)
            progress_bar.progress((i + 1) / total_stocks)
            
        status_text.text("✅ സ്കാനിംഗ് പൂർത്തിയായി!")
        
        if results:
            final_df = pd.DataFrame(results)
            breakout_stocks = final_df[final_df['Signal'].str.contains("BREAKOUT|BREAKDOWN")]
            
            if not breakout_stocks.empty:
                st.subheader("🎯 കണ്ടെത്തിയ സിഗ്നലുകൾ")
                st.dataframe(breakout_stocks, use_container_width=True, hide_index=True)
            else:
                st.info("നിലവിൽ ബ്രേക്ക്ഔട്ട് സിഗ്നലുകൾ ഒന്നും തന്നെ ലഭ്യമല്ല.")
        else:
            st.warning("മാർക്കറ്റ് ഡാറ്റ ലഭ്യമായില്ല.")
            
    except Exception as e:
        st.error(f"Error: {e}")
