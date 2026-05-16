import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="SwingPro Breakout - Nifty 500", layout="wide")

def analyze_breakout_batch(df_all, symbol):
    try:
        if symbol not in df_all.columns.levels[0]:
            return None
            
        df = df_all[symbol].dropna()
        if len(df) < 20: 
            return None

        close_series = df['Close']
        volume_series = df['Volume']

        # 1. BOLLINGER BANDS
        ma20 = close_series.rolling(window=20).mean()
        std20 = close_series.rolling(window=20).std()
        
        upper_band = ma20.iloc[-1] + (2 * std20.iloc[-1])
        lower_band = ma20.iloc[-1] - (2 * std20.iloc[-1])
        ltp = close_series.iloc[-1]

        # 2. VOLUME AVERAGE
        current_vol = volume_series.iloc[-1]
        avg_vol = volume_series.tail(10).mean()
        
        # 3. RSI
        delta = close_series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        
        rs = gain / loss if loss.iloc[-1] != 0 else None
        rsi = 100 - (100 / (1 + rs.iloc[-1])) if rs is not None else 50
        
        if pd.isna(rsi): 
            rsi = 50

        # Breakout Logic
        status = "⚪ Scanning"
        name = symbol.replace(".NS", "")
        
        if ltp > upper_band and current_vol > avg_vol:
            if rsi > 60:
                status = "🚀 STRONG BREAKOUT"
            else:
                status = "📈 BREAKOUT"
        elif ltp < lower_band:
            status = "📉 BREAKDOWN"

        # സ്കാനിംഗിൽ സിഗ്നൽ ഉള്ളവ മാത്രം റിട്ടേൺ ചെയ്യുന്നു
        if status != "⚪ Scanning":
            return {
                "Stock": name,
                "LTP": round(float(ltp), 2),
                "RSI": round(float(rsi), 2),
                "Signal": status
            }
    except:
        return None
    return None

# UI Design
st.markdown("<h1 style='text-align: center; color: #03A9F4;'>Momentum Breakout Scanner ⚡</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Bollinger Bands & RSI ഉപയോഗിച്ച് Nifty 500 ബ്രേക്ക്ഔട്ടുകൾ കണ്ടെത്തുന്നു.</p>", unsafe_allow_html=True)

# 📋 NIFTY 500 FULL STOCK LIST
nifty500_symbols = [
    "360ONE.NS", "3MINDIA.NS", "ABB.NS", "ACC.NS", "AIAENG.NS", "APLAPOLLO.NS", "AUBANK.NS", "AADHARHFC.NS", "AAKASH.NS", "AAVAS.NS",
    "ABBOTINDIA.NS", "ACE.NS", "ADANIENSOL.NS", "ADANIENT.NS", "ADANIGREEN.NS", "ADANIPORTS.NS", "ADANIPOWER.NS", "ATGL.NS", "AWL.NS", "ABCAPITAL.NS",
    "ABFRL.NS", "ABREL.NS", "AEGISLOG.NS", "AETHER.NS", "AFFLE.NS", "AGIIL.NS", "ALKEM.NS", "ALKYLAMINE.NS", "ALLCARGO.NS", "ALOKINDS.NS",
    "ALRE.NS", "AMBER.NS", "AMBUJACEM.NS", "AMD.NS", "AMRUTANJAN.NS", "ANANDRATHI.NS", "ANANTRAJ.NS", "APARIND.NS", "APEX.NS", "APOLLOHOSP.NS",
    "APOLLOTYRE.NS", "APTUS.NS", "ARE&M.NS", "ASAHIINDIA.NS", "ASHOKA.NS", "ASHOKLEY.NS", "ASIANPAINT.NS", "ASTERDM.NS", "ASTRAL.NS", "ASTRAZEN.NS",
    "ASTROCON.NS", "ATUL.NS", "AUROPHARMA.NS", "AVANTIFEED.NS", "AWFIS.NS", "AXISBANK.NS", "BEML.NS", "BLS.NS", "BSE.NS", "BAJAJ-AUTO.NS",
    "BAJAJCON.NS", "BAJAJELEC.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS", "BAJAJHLDNG.NS", "BALAMINES.NS", "BALKRISIND.NS", "BALMLAWRIE.NS", "BALRAMCHIN.NS", "BANDHANBNK.NS",
    "BANKBARODA.NS", "BANKINDIA.NS", "MAHABANK.NS", "BANSALWIRE.NS", "BARBEQUE.NS", "BASF.NS", "BATAINDIA.NS", "BAYERCROP.NS", "BEECCON.NS", "BEL.NS",
    "BENTLEY.NS", "BERGERPAINT.NS", "BHARATFORG.NS", "BHEL.NS", "BHARATWIRE.NS", "BPCL.NS", "BHARTIARTL.NS", "BIOCON.NS", "BIKAJI.NS", "BIRLACORPN.NS",
    "BIRLAMONEY.NS", "BLUEDART.NS", "BLUESTARCO.NS", "BOMDYEING.NS", "BOSCHLTD.NS", "BPPL.NS", "BRIGADE.NS", "BRITANNIA.NS", "MAPMYINDIA.NS", "CCL.NS",
    "CESC.NS", "CGPOWER.NS", "CIEINDIA.NS", "CINEVISTA.NS", "CIPLA.NS", "CLEAN.NS", "COALINDIA.NS", "COCHINSHIP.NS", "COFORGE.NS", "COLPAL.NS",
    "CONCOR.NS", "COROMANDEL.NS", "CRAFTSMAN.NS", "CREDITACC.NS", "CRISIL.NS", "CROMPTON.NS", "CUB.NS", "CUMMINSIND.NS", "CYIENT.NS", "DCAL.NS",
    "DCBBANK.NS", "DCMSHRIRAM.NS", "DLF.NS", "DOMS.NS", "DABUR.NS", "DALBHARAT.NS", "DATAPATTERNS.NS", "DATAMATICS.NS", "DEEPAKFERT.NS", "DEEPAKNTR.NS",
    "DELHIVERY.NS", "DELTAPCORP.NS", "DEN.NS", "DEVYANI.NS", "DHANI.NS", "DHANUKA.NS", "DILIPBUILD.NS", "DISHTV.NS", "DIVISLAB.NS", "DIXON.NS",
    "DODLA.NS", "DOLATALGO.NS", "DONEAR.NS", "DRREDDY.NS", "DREAMFOLKS.NS", "DREDGECORP.NS", "DYNAMATECH.NS", "EIDPARRY.NS", "EIHOTEL.NS", "EPL.NS",
    "EASEMYTRIP.NS", "EDELWEISS.NS", "EICHERMOT.NS", "ELECON.NS", "ELGIEQUIP.NS", "EMAMILTD.NS", "EMCURE.NS", "ENDURANCE.NS", "ENGINERSIN.NS", "EQUITASBNK.NS",
    "ERIS.NS", "ESCORTS.NS", "EXIDEIND.NS", "FDC.NS", "FEDERALBNK.NS", "FACT.NS", "FIEMIND.NS", "FINCABLES.NS", "FINPIPE.NS", "FSL.NS",
    "FIVESTAR.NS", "FOOTCLEAN.NS", "FORTIS.NS", "GAIL.NS", "GMMPFAUDL.NS", "GMRINFRA.NS", "GABRIEL.NS", "GALAXY.NS", "GANESHHOUC.NS", "GARDREACH.NS",
    "GARFIBRES.NS", "GATEWAY.NS", "GEECEE.NS", "GENUSPOWER.NS", "GEOJITFSL.NS", "GEPIL.NS", "GESHIP.NS", "GHCL.NS", "GICRE.NS", "GILLETTE.NS",
    "GLAND.NS", "GLAXO.NS", "GLENMARK.NS", "GOCOLORS.NS", "GODFRYPHLP.NS", "GODREJAGRO.NS", "GODREJCP.NS", "GODREJIND.NS", "GODREJPROP.NS", "GOKEX.NS",
    "GOPAL.NS", "GPIL.NS", "GPPL.NS", "GRANULES.NS", "GRAPHITE.NS", "GRASIM.NS", "GRAVITA.NS", "GREAVESCOCOT.NS", "GRINDWELL.NS", "GRSE.NS",
    "GSFC.NS", "GSPL.NS", "GUEST.NS", "GUJALKALI.NS", "GUJGASLTD.NS", "GNFC.NS", "GULFOILLUB.NS", "HAL.NS", "HAPPYFORGE.NS", "HBLPOWER.NS",
    "HCLTECH.NS", "HDFCBANK.NS", "HDFCLIFE.NS", "HDFCAMC.NS", "HFCL.NS", "HGINFRA.NS", "HLEGLAS.NS", "HMAAGRO.NS", "HONAUT.NS", "HPL.NS",
    "HSCL.NS", "HUDCO.NS", "HATSUN.NS", "HAVELLS.NS", "HEG.NS", "HEROMOTOCO.NS", "HERANBA.NS", "HEXAWARE.NS", "HIKAL.NS", "HINDALCO.NS",
    "HINDCOPPER.NS", "HINDPETRO.NS", "HINDUNILVR.NS", "HINDZINC.NS", "HITACHI.NS", "HOMFIRST.NS", "IOB.NS", "ICICIBANK.NS", "ICICIGI.NS", "ICICIPRULI.NS",
    "ISEC.NS", "IDBI.NS", "IDFCFIRSTB.NS", "IDFC.NS", "IIFL.NS", "IRB.NS", "IRCON.NS", "IRCTC.NS", "IRFC.NS", "IREDA.NS",
    "ITI.NS", "INDIACEM.NS", "IBULHSGFIN.NS", "INDIAMART.NS", "INDIHOTEL.NS", "INDIANB.NS", "IEX.NS", "IOC.NS", "IOB.NS", "INDIGO.NS",
    "INDIGOPNTS.NS", "INDOCO.NS", "INDOSTAR.NS", "INDUSINDBK.NS", "INDUSTOWER.NS", "INFIBEAM.NS", "INFY.NS", "INOXGFL.NS", "INOXINDIA.NS", "INOXWIND.NS",
    "INTELLECT.NS", "IPCALAB.NS", "JBCHEPHARM.NS", "JKCEMENT.NS", "JKLAC.NS", "JKPAPER.NS", "JKTYRE.NS", "JMFINANCIL.NS", "JSL.NS", "JSWENERGY.NS",
    "JSWINFRA.NS", "JSWSTEEL.NS", "JAIBALAJI.NS", "J&KBANK.NS", "JPASSOCIAT.NS", "JPPOWER.NS", "JAYBAR Maruti.NS", "JINDALSAW.NS", "JINDALSTEL.NS", "JIOFIN.NS",
    "JUBILANT.NS", "JUBLFOOD.NS", "JUBLINGREA.NS", "JUSTDIAL", "JYOTHYLAB.NS", "JYOTICNC.NS", "KIMS.NS", "KNRCON.NS", "KPITTECH.NS", "KPIGREEN.NS",
    "KPT.NS", "KRBL.NS", "KSB.NS", "KSCL.NS", "KAJAJSANMT.NS", "KAJARIACER.NS", "KALPATPOWR.NS", "KALYANKJIL.NS", "KANSAINER.NS", "KARURVYSYA.NS",
    "KAYNES.NS", "KEC.NS", "KEI.NS", "KENNAMET.NS", "KFINTECH.NS", "KIRLOSBROS.NS", "KIRLOSENG.NS", "KIRLOSIND.NS", "KOTAKBANK.NS", "KOTAKGOLD.NS",
    "KREBSBIO.NS", "KRYSTAL.NS", "LT.NS", "LTIM.NS", "LTTS.NS", "LICHSGFIN.NS", "LICI.NS", "LGBBROSLTD.NS", "LLOYDSME.NS", "LAKSHVILAS.NS",
    "LAOPALA.NS", "LAURUSLABS.NS", "LAXMICHEM.NS", "LEMONTREE.NS", "LINDEINDIA.NS", "LUPIN.NS", "LUXIND.NS", "MMTC.NS", "MOIL.NS", "MRF.NS",
    "M&M.NS", "M&MFIN.NS", "MANAPPURAM.NS", "MANGCHEFER.NS", "MANGALAM.NS", "MANINFRA.NS", "MARICO.NS", "MARUTI.NS", "MASTEK.NS", "MASTERS.NS",
    "MATRIMONY.NS", "MAXHEALTH.NS", "MAXESTATES.NS", "MAZDOCK.NS", "MEDANTA.NS", "MEDIASSIST.NS", "MEDPLUS.NS", "METROPOLIS.NS", "MINDACORP.NS", "MSUMI.NS",
    "MISHRADHAT.NS", "MITCON.NS", "MOLDTEKPAC.NS", "MONTECARLO.NS", "MOTILALOFS.NS", "MOTHERSON.NS", "MPHASIS.NS", "MCX.NS", "MUKANDLTD.NS", "MUTHOOTFIN.NS",
    "NATCOPHARM.NS", "NBCC.NS", "NCC.NS", "NESCO.NS", "NFL.NS", "NH.NS", "NHPC.NS", "NLCINDIA.NS", "NMDC.NS", "NOCIL.NS",
    "NTPC.NS", "NUCLEUS.NS", "NUVAMA.NS", "NUVOCO.NS", "NATIONALUM.NS", "NAVA.NS", "NAVINFLUOR.NS", "NAZARA.NS", "NEOGEN.NS", "NESRECO.NS",
    "NESTLEIND.NS", "NETWEB.NS", "NETWORK18.NS", "NILKAMAL.NS", "NIPPON.NS", "NURECA.NS", "NYKAA.NS", "OBEROIRLTY.NS", "ONGC.NS", "OIL.NS",
    "OMAXE.NS", "OMINFRAL.NS", "ORIENTCEM.NS", "ORIENTELEC.NS", "ORISSAMINE.NS", "PCBL.NS", "PENNIND.NS", "PFC.NS", "PGINVIT.NS", "PGHL.NS",
    "PGHH.NS", "PIIND.NS", "PNB.NS", "PNBGILTS.NS", "PNBHOUSING.NS", "PNCINFRA.NS", "PPLPHARMA.NS", "PRUDENTIAL.NS", "PTC.NS", "PUNJABCHEM.NS",
    "PVRINOX.NS", "PARADEEP.NS", "PARAGMILK.NS", "PARAS.NS", "PATELENG.NS", "PATANJALI.NS", "PAYTM.NS", "PERSISTENT.NS", "PETRONET.NS", "PHOENIXLTD.NS",
    "PILANIIND.NS", "POLYMED.NS", "POLYCAP.NS", "POLYCAB.NS", "POONAWALLA.NS", "POWERGRID.NS", "POWERMECH.NS", "PRAJIND.NS", "PRAKASH.NS", "PRESTIGE.NS",
    "PRICOLLTD.NS", "PRINCEPIPE.NS", "PRIVISCL.NS", "PRUDENT.NS", "QUESS.NS", "RBLBANK.NS", "RECLTD.NS", "RHIM.NS", "RITES.NS", "RPOWER.NS",
    "RICOAUTO.NS", "RAILTEL.NS", "RAIN.NS", "RAJESHEXPO.NS", "RAMASTEEL.NS", "RAMCOCEM.NS", "RAMCOIND.NS", "RAMCOSYS.NS", "RATNAMANI.NS", "RTNPOWER.NS",
    "RAYMOND.NS", "REDINGTON.NS", "RELAXO.NS", "RELIANCE.NS", "RELIGARE.NS", "RENUKA.NS", "REPCOHOME.NS", "RESPONIND.NS", "RBL.NS", "ROSSARI.NS",
    "ROLEXRINGS.NS", "ROUTE.NS", "RVNL.NS", "SBICARD.NS", "SBILIFE.NS", "SJVN.NS", "SKFINDIA.NS", "SRF.NS", "SAFARI.NS", "SAGCEM.NS",
    "SAIL.NS", "SALASAR.NS", "SAMHI.NS", "SANOFI.NS", "SANSERA.NS", "SAPPHIRE.NS", "SARDAEN.NS", "SAREGAMA.NS", "SBIN.NS", "SCHAEFFLER.NS",
    "SCHNEIDER.NS", "SEAMECLTD.NS", "SENSEX.NS", "SEQUENT.NS", "SERVO.NS", "SESHAPAPER.NS", "SETCO.NS", "SHAKTIPUMP.NS", "SHALBY.NS", "SHANKARA.NS",
    "SHARED.NS", "SHREECEM.NS", "SHREEPUSHK.NS", "SHRENIK.NS", "SHREERAMA.NS", "SHRIRAMFIN.NS", "SHRIRAMPPS.NS", "SHYAMMETL.NS", "SIEMENS.NS", "SIGACHI.NS",
    "SIGNATURE.NS", "SILVER.NS", "SINGER.NS", "SOBHA.NS", "SOLARINDS.NS", "SOMANYCERA.NS", "SONACOMS.NS", "SONATSOFTW.NS", "SOUTHBANK.NS", "SPANDANA.NS",
    "SPARC.NS", "SRIHARI.NS", "STARCEMENT.NS", "STARHEALTH.NS", "STERTOOLS.NS", "STOVEKRAFT.NS", "SUBEXLTD.NS", "SUBROS.NS", "SUDARSCHEM.NS", "SULA.NS",
    "SUMITCHEM.NS", "SUNPHARMA.NS", "SUNTECK.NS", "SUNTV.NS", "SUNDARAM.NS", "SUNDRMFAST.NS", "SUNILHITEC.NS", "SUPERIOR.NS", "SUPRAJIT.NS", "SUPREMEIND.NS",
    "SURYODAY.NS", "SURYAROSNI.NS", "SUVENPHAR.NS", "SUZLON.NS", "SWANENERGY.NS", "SWARAJENG.NS", "SYENE.NS", "SYNGENE.NS", "SYRMA.NS", "TASTYBITE.NS",
    "TATACOMM.NS", "TATACONSUM.NS", "TATAELXSI.NS", "TATAINV.NS", "TATAMOTORS.NS", "TATAMTRDVR.NS", "TATAPOWER.NS", "TATATECH.NS", "TATASTEEL.NS", "TTML.NS",
    "TCS.NS", "TECHM.NS", "TECHNOE.NS", "TEJASNET.NS", "TEXRAIL.NS", "THERMAX.NS", "THOMASCOOK.NS", "THROUGH.NS", "THYROCARE.NS", "TIINDIA.NS",
    "TI.NS", "TIMKEN.NS", "TIPSMUSIC.NS", "TITAN.NS", "TODAY.NS", "TORNTPOWER.NS", "TORNTPHARM.NS", "TREJHARA.NS", "TRENT.NS", "TRIDENT.NS",
    "TRITURBINE.NS", "TRIVENI.NS", "TRUST.NS", "TTKPRESTIG.NS", "TV18BRDCST.NS", "TVSSCS.NS", "TVSMOTOR.NS", "TVTODAY.NS", "UBL.NS", "UDEV.NS",
    "UFLEX.NS", "UCOBANK.NS", "UJJIVANSFB.NS", "ULTRACEMCO.NS", "UNIONBANK.NS", "UNIENTER.NS", "UNITEDTEA.NS", "UNITDSPR.NS", "UNOMINDA.NS", "UPL.NS",
    "UTIAMC.NS", "VAIBHAVGBL.NS", "VAKRANGEE.NS", "VALIANTORG.NS", "VAMSHI.NS", "VARDHACRMN.NS", "VARROC.NS", "VBL.NS", "VEDL.NS", "VENKEYS.NS",
    "VGUARD.NS", "VIPIND.NS", "VSTIND.NS", "VATECHWAB.NS", "VINOXY.NS", "VINATIORGA.NS", "VISAKAIND.NS", "VOLTAS.NS", "VRLLOG.NS", "WSTCSTPAPR.NS",
    "WELCORP.NS", "WELENT.NS", "WELSPUNLIV.NS", "WESTLIFE.NS", "WHIRLPOOL.NS", "WIPRO.NS", "WOCKHARDT.NS", "WONDERLA.NS", "XCHANGING.NS", "YATHARTH.NS",
    "YESBANK.NS", "ZEEL.NS", "ZEELEARN.NS", "ZENSARTECH.NS", "ZFCVINDIA.NS", "ZOMATO.NS", "ZOTA.NS", "ZUARI.NS", "ZYDUSWELL.NS", "ZYDUSLIFE.NS"
]

if st.button('🚀 Nifty 500 സ്കാനിംഗ് തുടങ്ങുക'):
    try:
        results = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("⚡ Fetching Market Data for 500 Stocks at Ultra-Speed...")
        
        # 500 സ്റ്റോക്കുകളുടെയും ഡാറ്റ ഒരൊറ്റ റിക്വസ്റ്റിൽ ഡൗൺലോഡ് ചെയ്യുന്നു (ആപ്പ് ഹാങ്ങ് ആകില്ല)
        all_data = yf.download(nifty500_symbols, period="1mo", interval="1d", group_by="ticker", progress=False)
        
        total_stocks = len(nifty500_symbols)
        
        for i, s in enumerate(nifty500_symbols):
            if i % 25 == 0:  # പ്രോഗ്രസ് ബാർ അപ്‌ഡേറ്റ് സ്മൂത്ത് ആക്കാൻ
                status_text.text(f"Analyzing Technical Patterns: {i}/{total_stocks} Stocks Done")
                progress_bar.progress((i + 1) / total_stocks)
                
            res = analyze_breakout_batch(all_data, s)
            if res: 
                results.append(res)
                
        progress_bar.progress(1.0)
        status_text.text("✅ Nifty 500 സ്കാനിംഗ് പൂർത്തിയായി!")
        
        if results:
            final_df = pd.DataFrame(results)
            
            # കണ്ടെത്തിയ ബ്രേക്ക്ഔട്ടുകൾ ഫിൽട്ടർ ചെയ്ത് കാണിക്കുന്നു
            breakout_df = final_df[final_df['Signal'].str.contains("BREAKOUT")]
            breakdown_df = final_df[final_df['Signal'].str.contains("BREAKDOWN")]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🎯 Bullish Breakouts (📈)")
                if not breakout_df.empty:
                    st.dataframe(breakout_df.sort_values(by="RSI", ascending=False), use_container_width=True, hide_index=True)
                else:
                    st.info("ബുള്ളിഷ് ബ്രേക്ക്ഔട്ടുകൾ ഒന്നും തന്നെ നിലവിലില്ല.")
                    
            with col2:
                st.subheader("⚠️ Bearish Breakdowns (📉)")
                if not breakdown_df.empty:
                    st.dataframe(breakdown_df.sort_values(by="RSI", ascending=True), use_container_width=True, hide_index=True)
                else:
                    st.info("ബെയറിഷ് ബ്രേക്ക്ഡൗണുകൾ ഒന്നും തന്നെ നിലവിലില്ല.")
        else:
            st.info("നിലവിൽ ബ്രേക്ക്ഔട്ട് സിഗ്നലുകൾ ഒന്നും തന്നെ ലഭ്യമല്ല.")
            
    except Exception as e:
        st.error(f"Error: {e}")
