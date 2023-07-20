import streamlit as st
import pandas as pd
from st_pages import Page, show_pages, add_page_title

# Optional -- adds the title and icon to the current page
add_page_title()

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
show_pages(
    [
        Page("Home.py", "Home", "🏠"),
        Page("pages/01_workday.py", "workday", icon="💪"),
        Page("pages/02_page02.py", "Usage", ":books:"),
    ]
)

st.write("医療情報部　統計ツール")

