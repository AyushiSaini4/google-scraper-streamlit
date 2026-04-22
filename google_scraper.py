import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse

# Page config
st.set_page_config(page_title="Web Search App", page_icon="🔍")


def search_duckduckgo(query):
    url = "https://html.duckduckgo.com/html/"
    headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/120.0.0.0 Safari/537.36"),
    }

    res = requests.post(url, headers=headers, data={"q": query})
    soup = BeautifulSoup(res.text, "html.parser")

    results = []

    for a in soup.select("a.result__url"):
        href = a.get("href", "")

        # Clean DuckDuckGo redirect links
        if href.startswith("//duckduckgo.com/l/?uddg="):
            parsed = urllib.parse.parse_qs(
                urllib.parse.urlparse(href).query
            )
            href = urllib.parse.unquote(parsed.get("uddg", [href])[0])

        title_elem = a.parent.parent.select_one("h2.result__title a")
        title = title_elem.text.strip() if title_elem else a.text.strip()

        if href and title:
            results.append({"title": title, "link": href})

        if len(results) >= 5:
            break

    return results


def run():
    st.title("🔍 Smart Web Search App")
    st.caption("Search the web using DuckDuckGo (No API needed)")

    query = st.text_input(
        "🔎 Enter your search query",
        placeholder="e.g. AI tools, startups, Python projects"
    )

    if st.button("🚀 Search"):
        if not query.strip():
            st.warning("Please enter a query.")
            return

        with st.spinner("Searching..."):
            try:
                results = search_duckduckgo(query)

                if results:
                    st.success(f"Found {len(results)} results")

                    for i, r in enumerate(results, start=1):
                        st.markdown(f"### {i}. [{r['title']}]({r['link']})")
                        st.write(r['link'])
                        st.divider()
                else:
                    st.warning("No results found or request was blocked.")

            except Exception:
                st.error("⚠️ Something went wrong. Please try again.")


if __name__ == "__main__":
    run()
