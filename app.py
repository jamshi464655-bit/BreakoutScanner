import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_ta as ta

# Page Configuration
st.set_page_config(page_title="SwingPro Breakout", layout="wide")

URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSsnZ6oD_zaP3JLOVaAbR1ZTzn2TVQ26agPr_G89Iey669ijjuJnwgbiaJDtdBiF1ixVyZ0gtfTA1e8/pub?output=csv"

def analyze_breakout(symbol):
    try:
        ticker = f"{symbol}.NS"
        # 6 മാസത്തെ ഡാറ്റ എടുക്കുന്നു
        df = yf.download(ticker, period="6mo", interval="1d", progress=False)
        
        if df.empty or len(df) < 50: 
            return None

        # CRITICAL FIX: Multi-Index കോളം പ്രശ്നം പരിഹരിക്കാൻ 1D സീരീസ് ആക്കുന്നു
        close_series = df['Close'].squeeze()
        volume_series = df['Volume'].squeeze()
        
        if close_series.empty:
            return None

        # 1. Bollinger Bands (BB) കണക്കാക്കുന്നു
        bb = ta.bbands(close_series, length=20, std=2)
        if bb is None or bb.empty:
            return None
            
        # കോളം നെയിമുകൾ കൃത്യമായി എടുക്കുന്നു
        upper_band = bb.iloc[-1, 2] # BBU_20_2.0
        lower_band = bb.iloc[-1, 0] # BBL_20_2.0
        ltp = close_series.iloc[-1]

        # 2. Volume & RSI
        current_vol = volume_series.iloc[-1]
        avg_vol = volume_series.tail(10).mean()
        
        rsi_series = ta.rsi(close_series, length=14)
        rsi = rsi_series.iloc[-1] if rsi_series is not None else 50

        # Breakout Logic
        status = "⚪ Scanning"
        
        # കണ്ടീഷൻ: വില അപ്പർ ബാൻഡിന് മുകളിൽ പോകുന്നു + വോളിയം കൂടുന്നു
        if ltp > upper_band and current_vol > avg_vol:
            if rsi > 60:
                status = "🚀 STRONG BREAKOUT"
            else:
                status = "📈 BREAKOUT"
        
        # കണ്ടീഷൻ: വില താഴത്തെ ബാൻഡിന് താഴെ പോകുന്നു (വീഴ്ച)
        elif ltp < lower_band:
            status = "📉 BREAKDOWN"

        return {
            "Stock": symbol,
            "LTP": round(float(ltp), 2),
            "RSI": round(float(rsi), 2),
            "Signal": status
        }
    except Exception as e:
        return None

# UI Design
st.markdown("<h1 style='text-align: center; color: #03A9F4;'>Momentum Breakout Scanner ⚡</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Bollinger Bands ഉപയോഗിച്ച് ബ്രേക്ക്ഔട്ട് സംഭവിക്കുന്ന സ്റ്റോക്കുകളെ കണ്ടെത്തുന്നു.</p>", unsafe_allow_html=True)

if st.button('🚀 സ്കാനിംഗ് തുടങ്ങുക'):
    try:
        # Google Sheet വായിക്കുന്നു
        sheet_df = pd.read_csv(URL)
        symbols = sheet_df['Symbol'].dropna().unique().tolist()
        
        # പരമാവധി 60 സ്റ്റോക്കുകളായി പരിമിതപ്പെടുത്തുന്നു (സ്പീഡ് കൂട്ടാൻ)
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
            # Progress bar എറർ വരാതിരിക്കാനുള്ള സുരക്ഷിത വരി
            progress_bar.progress((i + 1) / total_stocks)
            
        status_text.text("✅ സ്കാനിംഗ് പൂർത്തിയായി!")
        
        if results:
            final_df = pd.DataFrame(results)
            # സിഗ്നൽ ഉള്ളവ (Scannning അല്ലാത്തവ) മാത്രം ഫിൽട്ടർ ചെയ്യുന്നു
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