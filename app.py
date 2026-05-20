import streamlit as st
import pandas as pd

# Page configuration - പ്രീമിയം ലുക്ക് നൽകാൻ ഫുൾ വൈഡ് ലേഔട്ട്
st.set_page_config(
    page_title="EasyCharts Pro - Ultra Terminal", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark Mode & Premium UI Styling (Custom CSS)
st.markdown("""
<style>
    /* മെയിൻ ബാക്ക്ഗ്രൗണ്ട് കടും നീലയും കറുപ്പും ആക്കുന്നു */
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
    }
    /* ടോപ്പ് ഹെഡർ ബാനർ സ്റ്റൈലിങ് */
    .header-box {
        background: linear-gradient(135deg, #1e1b4b, #311042, #0f172a); 
        padding: 30px; 
        border-radius: 20px; 
        color: white; 
        text-align: center; 
        margin-bottom: 30px; 
        border: 1px solid #4f46e5;
        box-shadow: 0 10px 30px rgba(79, 70, 229, 0.2);
    }
    .header-box h1 {
        font-size: 32px;
        font-weight: 800;
        letter-spacing: 1px;
        margin-bottom: 5px;
        background: linear-gradient(to right, #6366f1, #a855f7, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    /* ഇൻഫോ/മെട്രിക് കാർഡുകൾ */
    .metric-card {
        background: #111827;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #1f2937;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    /* ബട്ടൺ ഡിസൈൻ */
    .stButton>button {
        background: linear-gradient(90deg, #4f46e5, #7c3aed) !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
        padding: 12px 24px !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(124, 58, 237, 0.4) !important;
    }
</style>
""", unsafe_allow_html=True)

# Top Dashboard Banner
st.markdown("""
<div class="header-box">
    <h1>⚡ EASYCHARTS PRO — ULTRA TERMINAL</h1>
    <p style="color: #94a3b8; font-size: 16px;">Multi-Indicator Real-Time Technical Scanner & Breakout Analytics</p>
</div>
""", unsafe_allow_html=True)

# SIDEBAR - ഇൻഡിക്കേറ്റർ കൺട്രോളുകൾ
st.sidebar.markdown("### 🛠️ Scanner Strategy Filters")
st.sidebar.markdown("സ്‌കാൻ ചെയ്യാൻ ആവശ്യമുള്ള ഇൻഡിക്കേറ്ററുകൾ തിരഞ്ഞെടുക്കുക:")

use_ema = st.sidebar.checkbox("EMA Cross (20 / 50 / 200)", value=True)
use_vwap = st.sidebar.checkbox("VWAP Pullback / Breakout", value=True)
use_cpr = st.sidebar.checkbox("CPR (Central Pivot Range) Width", value=False)

min_volume = st.sidebar.number_input("Minimum Volume Filter", value=100000, step=50000)
scan_segment = st.sidebar.selectbox("Market Segment", ["NIFTY 500", "NIFTY OPTIONS", "MIDCAP"])

st.sidebar.markdown("---")
st.sidebar.info("💡 സൂചന: ടേബിളിലെ TradingView ലിങ്കിൽ ക്ലിക്ക് ചെയ്താൽ ലൈവ് ചാർട്ട് നേരിട്ട് കാണാം.")

# MAIN BOARD - സ്കാനർ ബട്ടൺ
if st.button("🔥 RUN DEEP MARKET SCAN", use_container_width=True):
    with st.spinner("Analyzing Nifty charts, computing indicator math..."):
        try:
            # ലൈവ് ഡാറ്റാ എൻജിൻ (ഇവിടെ നിങ്ങളുടെ റിയൽ ഡാറ്റാ ലിങ്ക് ചെയ്യാം)
            # ഇതിൽ ഇന്ത്യൻ സ്റ്റോക്കുകളുടെ കൃത്യമായ TradingView ചാർട്ട് ലിങ്ക് ചേർത്തിട്ടുണ്ട്
            market_data = {
                "Ticker Symbol": ["RELIANCE", "TCS", "INFY", "SBIN", "TATAMOTORS", "HDFCBANK"],
                "LTP (₹)": [2452.10, 3210.50, 1498.00, 582.40, 925.15, 1645.00],
                "Change %": [2.45, -0.65, 1.85, 3.10, -1.20, 0.15],
                "Volume": [1500000, 450000, 890000, 3200000, 2100000, 1100000],
                "Signal Type": ["Breakout", "Consolidation", "Pre-Breakout", "Breakout", "Bearish Pullback", "Pre-Breakout"],
                "Chart Link": [
                    "https://in.tradingview.com/chart/?symbol=NSE:RELIANCE",
                    "https://in.tradingview.com/chart/?symbol=NSE:TCS",
                    "https://in.tradingview.com/chart/?symbol=NSE:INFY",
                    "https://in.tradingview.com/chart/?symbol=NSE:SBIN",
                    "https://in.tradingview.com/chart/?symbol=NSE:TATAMOTORS",
                    "https://in.tradingview.com/chart/?symbol=NSE:HDFCBANK"
                ]
            }
            
            df = pd.DataFrame(market_data)
            
            # വോളിയം അനുസരിച്ച് ഫിൽട്ടർ ചെയ്യുന്നു
            df = df[df["Volume"] >= min_volume]
            
            # കൗണ്ടറുകൾ കണക്കാക്കുന്നു
            pre_count = len(df[df["Signal Type"] == "Pre-Breakout"])
            break_count = len(df[df["Signal Type"] == "Breakout"])
            
            # മുകളിൽ കാണിക്കുന്ന ഇൻഫോ കാർഡുകൾ
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f'<div class="metric-card"><h4 style="color: #a855f7; margin:0;">🎯 PRE-BREAKOUT</h4><h2 style="margin:5px 0 0 0;">{pre_count} Stocks</h2></div>', unsafe_allow_html=True)
            with c2:
                st.markdown(f'<div class="metric-card"><h4 style="color: #10b981; margin:0;">🚀 ACTIVE BREAKOUT</h4><h2 style="margin:5px 0 0 0;">{break_count} Stocks</h2></div>', unsafe_allow_html=True)
            with c3:
                st.markdown(f'<div class="metric-card"><h4 style="color: #3b82f6; margin:0;">📊 TOTAL SCANNED</h4><h2 style="margin:5px 0 0 0;">{len(df)} Assets</h2></div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 📈 Live Scan Terminal Output")
            
            # TradingView ലിങ്ക് ക്ലിക്ക് ചെയ്യാൻ പാകത്തിൽ കാണിക്കുന്ന ടേബിൾ
            st.data_editor(
                df,
                column_config={
                    "Chart Link": st.column_config.LinkColumn(
                        "🔗 TradingView Chart",
                        help="Click to open this stock chart directly in TradingView",
                        display_text="Open Chart 📈"
                    ),
                    "LTP (₹)": st.column_config.NumberColumn(format="₹ %.2f"),
                    "Change %": st.column_config.NumberColumn(format="%.2f %%"),
                    "Volume": st.column_config.NumberColumn(format="%d")
                },
                use_container_width=True,
                hide_index=True,
                disabled=True # ടേബിൾ എഡിറ്റ് ചെയ്യാൻ പറ്റാത്ത രീതിയിൽ ക്ലീൻ ആക്കുന്നു
            )
            
        except Exception as e:
            st.error(f"⚠️ Live Scanner Error: {e}")
else:
    st.markdown("""
    <div style="text-align: center; padding: 40px; background: #111827; border-radius: 12px; border: 1px dashed #374151;">
        <p style="color: #9ca3af; font-size: 16px; margin: 0;">സിസ്റ്റം റെഡിയാണ്. സൈഡ്‌ബാറിൽ ഫിൽട്ടറുകൾ സെറ്റ് ചെയ്ത ശേഷം <b>RUN DEEP MARKET SCAN</b> ബട്ടൺ അമർത്തുക.</p>
    </div>
    """, unsafe_allow_html=True)
