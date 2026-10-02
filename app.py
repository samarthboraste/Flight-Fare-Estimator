import json
import joblib
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Flight Price Predictor", page_icon="✈️", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg: #0D1117;
    --card: #161B22;
    --surface: #1C2128;
    --accent: #F5B942;
    --accent-hover: #FFD166;
    --text: #F5F7FA;
    --muted: #9BA4B5;
    --border: #30363D;
}

html, body, .stApp, [class*="css"] {font-family: 'Inter', -apple-system, 'Segoe UI', sans-serif;}
#MainMenu, footer, header {visibility: hidden;}

.stApp {background: var(--bg);}
.block-container {padding-top: 2.8rem; max-width: 780px;}

/* heading */
.eyebrow {color: var(--accent); font-size: 0.74rem; font-weight: 600; letter-spacing: 0.16em;
    text-transform: uppercase; margin-bottom: 0.3rem; animation: rise 0.6s ease both;}
.title-grad {
    font-size: 2.7rem; font-weight: 700; letter-spacing: -0.02em; line-height: 1.15;
    margin: 0 0 0.4rem 0; padding-bottom: 0.1rem; color: var(--text);
    animation: rise 0.6s ease 0.05s both;
}
@media (max-width: 600px) {.title-grad {font-size: 2rem;}}
.sub {color: var(--muted); margin-bottom: 1.6rem; animation: rise 0.6s ease 0.1s both;}
.small {color: var(--muted); font-size: 0.74rem; text-transform: uppercase; letter-spacing: 0.09em;}

/* form card (st.container(key="formcard")) */
.st-key-formcard {
    background: var(--card); border: 1px solid var(--border); border-radius: 18px;
    padding: 1.4rem 1.4rem 0.6rem 1.4rem;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
    animation: rise 0.7s ease 0.15s both;
}

/* labels */
div[data-testid="stWidgetLabel"] p {color: var(--muted) !important; font-size: 0.8rem !important;
    font-weight: 500; letter-spacing: 0.03em;}

/* inputs */
div[data-baseweb="select"] > div, div[data-baseweb="input"], div[data-testid="stNumberInputContainer"] {
    background: var(--surface) !important; border: 1px solid var(--border) !important;
    border-radius: 10px !important; color: var(--text);
    transition: border-color 0.2s ease, box-shadow 0.2s ease;}
div[data-baseweb="select"] > div:hover, div[data-baseweb="input"]:hover {
    border-color: rgba(245, 185, 66, 0.55) !important;}
div[data-baseweb="select"] > div:focus-within, div[data-baseweb="input"]:focus-within {
    border-color: var(--accent) !important; box-shadow: 0 0 0 2px rgba(245, 185, 66, 0.18) !important;}
div[data-baseweb="popover"] ul {background: var(--card) !important; border: 1px solid var(--border); border-radius: 10px;}
div[data-baseweb="popover"] li:hover {background: var(--surface) !important;}

/* button */
div.stButton button {
    width: 100%; border-radius: 10px; padding: 0.75rem; font-weight: 600; letter-spacing: 0.02em;
    color: var(--bg); background: var(--accent); border: 1px solid var(--accent); box-shadow: none;
    transition: background 0.2s ease, border-color 0.2s ease, transform 0.15s ease;}
div.stButton button p {color: var(--bg) !important; font-weight: 600;}
div.stButton button:hover {background: var(--accent-hover); border-color: var(--accent-hover); color: var(--bg) !important;
    transform: translateY(-1px);}
div.stButton button:active {background: var(--accent); transform: translateY(0);}
div.stButton button:focus {color: var(--bg) !important; box-shadow: 0 0 0 2px rgba(245, 185, 66, 0.3) !important;}

/* ticket */
.ticket {
    margin-top: 1.4rem; border-radius: 18px; overflow: hidden;
    background: var(--card); border: 1px solid var(--border);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
    animation: rise 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) both;}
.t-head {display: flex; justify-content: space-between; align-items: center; padding: 0.8rem 1.4rem;
    background: var(--surface); border-bottom: 1px solid var(--border);}
.chip {color: var(--text); font-size: 0.86rem; font-weight: 600;}
.chip.ghost {color: var(--accent); font-weight: 500; border: 1px solid rgba(245, 185, 66, 0.45);
    border-radius: 999px; padding: 0.12rem 0.7rem; font-size: 0.78rem;}

/* flight path above the cities */
.sky {padding: 2.2rem 1.6rem 0 1.6rem;}
.arc {position: relative; height: 60px; border-top: 1px dashed rgba(245, 185, 66, 0.5);
    border-radius: 50% 50% 0 0 / 100% 100% 0 0;}
.arc::before, .arc::after {content: ""; position: absolute; bottom: -4px; width: 8px; height: 8px;
    border-radius: 50%; background: var(--accent);
    animation: pulse 2.4s ease-out infinite;}
.arc::before {left: -4px;}
.arc::after {right: -4px; animation-delay: 1.2s;}
.arc-label {position: absolute; left: 50%; bottom: 10px; transform: translateX(-50%);
    color: var(--muted); font-size: 0.82rem; letter-spacing: 0.02em; white-space: nowrap;}
.plane {position: absolute; font-size: 22px; line-height: 1; display: inline-block;
    left: calc(0% - 11px); top: 49px; animation: fly 4s linear infinite;}

.t-route {display: flex; align-items: flex-start; justify-content: space-between; padding: 0.9rem 1.6rem 1.2rem 1.6rem;}
.city {font-size: 1.55rem; font-weight: 700; letter-spacing: -0.01em; color: var(--text);}
.when {color: var(--muted); font-size: 0.85rem; margin-top: 2px;}

.t-grid {display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.8rem; padding: 0.2rem 1.6rem 1.3rem 1.6rem;}
.v {color: var(--text); font-size: 1rem; font-weight: 500; margin-top: 3px;}

.t-foot {display: flex; justify-content: space-between; align-items: center; padding: 1.1rem 1.6rem;
    border-top: 1px dashed var(--border); background: var(--surface);}
.price {font-size: 2.2rem; font-weight: 700; letter-spacing: -0.02em; color: var(--accent);
    animation: pop 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) 0.25s both;}
.note {color: var(--muted); font-size: 0.74rem; margin-top: 3px;}

.footer-note {margin-top: 2rem; text-align: center; animation: rise 0.7s ease 0.3s both;}

/* animations */
@keyframes rise {from {opacity: 0; transform: translateY(14px);} to {opacity: 1; transform: translateY(0);}}
@keyframes pop {from {opacity: 0; transform: scale(0.92);} to {opacity: 1; transform: scale(1);}}
@keyframes pulse {0% {box-shadow: 0 0 0 0 rgba(245, 185, 66, 0.4);} 70%, 100% {box-shadow: 0 0 0 8px rgba(245, 185, 66, 0);}}
@keyframes fly {
    0%   {left: calc(0% - 11px);     top: 49px;  transform: rotate(-45deg); opacity: 0;}
    10%  {left: calc(2.5% - 11px);   top: 30px;  transform: rotate(17deg);  opacity: 1;}
    20%  {left: calc(9.5% - 11px);   top: 14px;  transform: rotate(32deg);}
    30%  {left: calc(20.5% - 11px);  top: 1px;   transform: rotate(38deg);}
    40%  {left: calc(34.5% - 11px);  top: -8px;  transform: rotate(42deg);}
    50%  {left: calc(50% - 11px);    top: -11px; transform: rotate(45deg);}
    60%  {left: calc(65.5% - 11px);  top: -8px;  transform: rotate(48deg);}
    70%  {left: calc(79.5% - 11px);  top: 1px;   transform: rotate(52deg);}
    80%  {left: calc(90.5% - 11px);  top: 14px;  transform: rotate(58deg);}
    90%  {left: calc(97.5% - 11px);  top: 30px;  transform: rotate(73deg);  opacity: 1;}
    100% {left: calc(100% - 11px);   top: 49px;  transform: rotate(135deg); opacity: 0;}
}
@media (max-width: 600px) {.t-grid {grid-template-columns: repeat(2, 1fr);} .city {font-size: 1.25rem;}}
@media (prefers-reduced-motion: reduce) {* {animation: none !important; transition: none !important;}}
/* site footer */
.site-footer {margin-top: 2.2rem; border: 1px solid rgba(255, 255, 255, 0.10); border-radius: 18px;
    overflow: hidden; background: #0b0e13; animation: rise 0.7s ease 0.3s both;}
.sf-top {padding: 2rem 1.5rem 1.6rem 1.5rem; text-align: center;}
.sf-title {color: var(--text); font-size: 1.5rem; font-weight: 600; letter-spacing: -0.01em;}
.sf-desc {color: var(--muted); font-size: 0.88rem; line-height: 1.7; max-width: 520px; margin: 0.6rem auto 1.3rem auto;}
.sf-icons {display: flex; justify-content: center; gap: 0.9rem;}
.sf-icons a {width: 38px; height: 38px; border-radius: 50%; border: 1px solid rgba(255, 255, 255, 0.35);
    display: flex; align-items: center; justify-content: center; color: var(--text); text-decoration: none;
    transition: border-color 0.2s ease, color 0.2s ease, transform 0.2s ease;}
.sf-icons a:hover {border-color: var(--accent); color: var(--accent); transform: translateY(-2px);}
.sf-icons i {width: 17px; height: 17px; display: block; background-color: currentColor;
    -webkit-mask-size: contain; mask-size: contain; -webkit-mask-repeat: no-repeat; mask-repeat: no-repeat;
    -webkit-mask-position: center; mask-position: center;}
.sf-icons i.gh {-webkit-mask-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'><path d='M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z'/></svg>");
    mask-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'><path d='M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z'/></svg>");}
.sf-icons i.li {-webkit-mask-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><path d='M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z'/></svg>");
    mask-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><path d='M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z'/></svg>");}
.sf-bar {display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;
    padding: 0.9rem 1.5rem; background: #05070a; border-top: 1px solid rgba(255, 255, 255, 0.08);
    font-size: 0.82rem; color: var(--text);}
.sf-bar a {color: var(--accent); text-decoration: none; font-weight: 500;}
.sf-bar a:hover {text-decoration: underline;}
.sf-bar span {color: var(--muted);}
</style>
""", unsafe_allow_html=True)


@st.cache_resource(show_spinner=False)
def load_files():
    model = joblib.load("rf_model.pkl")
    columns = json.load(open("columns.json"))
    encoders = joblib.load("encoders.pkl")
    return model, columns, encoders


model, columns, encoders = load_files()


def options(col):
    """Return {display label: raw value} for a categorical column."""
    return {v.replace("_", " ").title(): v for v in encoders[col].classes_}


def inr(n):
    s = str(int(round(n)))
    if len(s) <= 3:
        return "₹" + s
    head, tail, parts = s[:-3], s[-3:], []
    while len(head) > 2:
        parts.insert(0, head[-2:])
        head = head[:-2]
    if head:
        parts.insert(0, head)
    return "₹" + ",".join(parts) + "," + tail


def fmt_duration(hours):
    total = round(hours * 60)
    h, m = divmod(total, 60)
    return f"{h}h {m}m" if m else f"{h}h"


def fmt_stops(raw):
    return {"zero": "Non-stop", "one": "1 stop", "two_or_more": "2+ stops"}.get(raw, raw)


airlines = options("airline")
classes = options("class")
cities = options("source_city")
times = options("departure_time")
stops_opt = options("stops")

st.markdown('<div class="eyebrow">Fare estimator</div>', unsafe_allow_html=True)
st.markdown('<div class="title-grad">Flight Price Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">Estimate a domestic ticket fare from the route, timing and booking window.</div>',
            unsafe_allow_html=True)

with st.container(key="formcard"):
    c1, c2 = st.columns(2)
    airline = c1.selectbox("Airline", list(airlines))
    flight_class = c2.selectbox("Class", list(classes))
    source = c1.selectbox("From", list(cities), index=0)
    dest = c2.selectbox("To", list(cities), index=1)
    dep = c1.selectbox("Departure time", list(times), index=1)
    arr = c2.selectbox("Arrival time", list(times), index=2)
    stops = c1.selectbox("Stops", list(stops_opt))
    duration = c2.number_input("Duration (hours)", min_value=0.5, max_value=50.0,
                               value=2.5, step=0.05, format="%.2f")
    days_left = st.slider("Days left before departure", 1, 49, 15)

predict_clicked = st.button("Predict price", width="stretch")

if predict_clicked:
    if source == dest:
        st.error("Source and destination cities cannot be the same.")
    else:
        row = pd.DataFrame([{
            "airline": airlines[airline], "source_city": cities[source],
            "departure_time": times[dep], "stops": stops_opt[stops],
            "arrival_time": times[arr], "destination_city": cities[dest],
            "class": classes[flight_class], "duration": duration, "days_left": days_left,
        }])
        for col, enc in encoders.items():
            row[col] = enc.transform(row[col])
        price = model.predict(row[columns])[0]

        st.markdown(f"""
<div class="ticket">
<div class="t-head"><span class="chip">{airline}</span><span class="chip ghost">{flight_class}</span></div>
<div class="sky"><div class="arc"><span class="plane">✈️</span><span class="arc-label">{fmt_duration(duration)} · {fmt_stops(stops_opt[stops])}</span></div></div>
<div class="t-route">
<div><div class="city">{source}</div><div class="when">{dep}</div></div>
<div style="text-align:right"><div class="city">{dest}</div><div class="when">{arr}</div></div>
</div>
<div class="t-grid">
<div><div class="small">Stops</div><div class="v">{stops}</div></div>
<div><div class="small">Duration</div><div class="v">{duration:g} h</div></div>
<div><div class="small">Days left</div><div class="v">{days_left}</div></div>
<div><div class="small">Class</div><div class="v">{flight_class}</div></div>
</div>
<div class="t-foot"><div><div class="small">Estimated fare</div><div class="note">Typical error about ₹1,136</div></div><div class="price">{inr(price)}</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="small footer-note">Random Forest Regressor · R² 98.58% · MAE ₹1,136 · RMSE ₹2,705 · evaluated on unseen test data · estimate only</div>',
            unsafe_allow_html=True)

st.markdown("""
<div class="site-footer">
<div class="sf-top">
<div class="sf-title">Flight Price Predictor</div>
<div class="sf-desc">A machine learning project that estimates domestic flight fares in India using a Random Forest regression model, built with Python, scikit-learn and Streamlit.</div>
<div class="sf-icons">
<a href="https://github.com/samarthboraste" target="_blank" rel="noopener" title="GitHub"><i class="gh"></i></a>
<a href="https://www.linkedin.com/in/samarthb77/" target="_blank" rel="noopener" title="LinkedIn"><i class="li"></i></a>
</div>
</div>
<div class="sf-bar"><div>Made by <a href="https://www.linkedin.com/in/samarthb77/" target="_blank" rel="noopener">Samarth</a></div><span>© 2026 · Data Science Project</span></div>
</div>
""", unsafe_allow_html=True)