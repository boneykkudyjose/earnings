from earnings import *
import pandas as pd
import streamlit as st
from streamlit_calendar import calendar


def get_sp500_ticker_list():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    tables = pd.read_html(url)
    sp500_table = tables[0]
    tickers = sp500_table["Symbol"].tolist()
    return tickers


def convert_ticker(ticker):
    # Replace dot with a hyphen if present in the ticker
    return ticker.replace("-", ".")


def get_calendar_event_nonapi(tickers):
    # Converts the parsed json from FMP API into a list of events to be passed into streamlit_calendar
    calendar_events = []
    i = 0
    for ticker in tickers:
        ticker = convert_ticker(ticker)

        calendar_event = {}
        calendar_event["id"] = i
        e = Earnings(ticker)

        calendar_event["title"] = "☀ " + ticker
        if isinstance(e.getNextEarningsDate(), datetime.datetime):
            # calendar_event["start"] =  e.getNextEarningsDate().strftime("%m/%d/%Y, %H:%M:%S")
            calendar_event["ticker"] = ticker
            calendar_event["start"] = e.getNextEarningsDate().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            calendar_event["end"] = e.getNextEarningsDate().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            calendar_events.append(calendar_event)
        i += 1

    return calendar_events


def get_calendar_option():
    calendar_options = {
        "editable": "true",
        "navLinks": "true",
        "headerToolbar": {
            "left": "today prev,next",
            "center": "title",
            "right": "dayGridDay,dayGridWeek,dayGridMonth,listMonth",
        },
        # "initialDate": today.strftime('%Y-%m-%d'),
        "initialView": "dayGridMonth",
    }
    return calendar_options


def get_custom_css():
    custom_css = """
        .fc-event-past {
            opacity: 0.8;
        }
        .fc-event-time {
            font-style: italic;
        }
        .fc-event-title {
            font-weight: 700;
        }
        .fc-toolbar-title {
            font-size: 2rem;
        }
    """
    return custom_css


st.header("Stock Earnings Calendar 📆")

# Cache SP500 tickers since they don't change often
@st.cache_data
def load_sp500_tickers():
    return get_sp500_ticker_list()

# Cache calendar events since they probably don't need to be fetched on every rerun
@st.cache_data
def load_calendar_events(tickers):
    return get_calendar_event_nonapi(tickers)

# Cache options and CSS if they're static
@st.cache_data
def load_calendar_options():
    return get_calendar_option()

@st.cache_data
def load_custom_css():
    return get_custom_css()

# Load cached data
sp500_tickers = load_sp500_tickers()
cal_events = load_calendar_events(sp500_tickers)
calendar_options = load_calendar_options()
custom_css = load_custom_css()

# Calendar style override
calendar_style = """
    <style>
        iframe[title="streamlit_calendar.calendar"] {
            height: 1500px; 
        }
    </style>
"""
st.markdown(calendar_style, unsafe_allow_html=True)

# Display calendar
calendar_component = calendar(events=cal_events, options=calendar_options, custom_css=custom_css)
st.write(calendar_component)
