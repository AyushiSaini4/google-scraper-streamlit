# PYTHON_TASKS_LW/google_scraper.py

import streamlit as st
import requests
from bs4 import BeautifulSoup

def google_scrape(query):
    # Due to Google's strict bot protection (CAPTCHAs), we'll use DuckDuckGo's HTML version
    # which is much friendlier for basic web scraping using just `requests`.
    url = "https://html.duckduckgo.com/html/"
    headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/120.0.0.0 Safari/537.36"),
    }
    # DuckDuckGo HTML uses POST requests for queries
    res = requests.post(url, headers=headers, data={"q": query})
    soup = BeautifulSoup(res.text, "html.parser")
    results = []

    import urllib.parse
    for a in soup.select("a.result__url"):
        href = a.get("href", "")
        # Clean up the redirect link DuckDuckGo uses
        if href.startswith("//duckduckgo.com/l/?uddg="):
            parsed = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
            href = urllib.parse.unquote(parsed.get("uddg", [href])[0])
            
        title_elem = a.parent.parent.select_one("h2.result__title a")
        title = title_elem.text.strip() if title_elem else a.text.strip()
        
        if href and title:
            results.append({"title": title, "link": href})
        if len(results) >= 5:
            break

    return results

def run():
    st.subheader("🔍 Web Search Scraper (via DuckDuckGo)")

    query = st.text_input("Enter your search query", "OpenAI GPT-4")

    if st.button("Scrape"):
        with st.spinner("Scraping results..."):
            try:
                results = google_scrape(query)
                if results:
                    for i, r in enumerate(results, start=1):
                        st.markdown(f"**{i}. [{r['title']}]({r['link']})**")
                else:
                    st.warning("No results found or the request was blocked.")
            except Exception as e:
                st.error(f"❌ Error while scraping: {e}")

if __name__ == "__main__":
    run()

