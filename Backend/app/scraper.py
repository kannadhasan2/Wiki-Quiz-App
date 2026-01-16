import re
import requests
from bs4 import BeautifulSoup

WIKI_HOSTS = ("en.wikipedia.org",)

def _clean(text: str) -> str:
    text = re.sub(r"\[\d+\]", "", text)  # remove citation markers like [1]
    text = re.sub(r"\s+", " ", text).strip()
    return text

def scrape_wikipedia(url: str) -> dict:
    # Hard guard: must be wikipedia article
    if "wikipedia.org/wiki/" not in url:
        raise ValueError("Only Wikipedia article URLs are allowed (must contain wikipedia.org/wiki/).")

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; WikiQuizBot/1.0; +https://example.com/bot)"
    }
    r = requests.get(url, headers=headers, timeout=20)
    r.raise_for_status()

    html = r.text
    soup = BeautifulSoup(html, "lxml")

    title_tag = soup.select_one("#firstHeading")
    title = _clean(title_tag.get_text(" ")) if title_tag else "Untitled"

    # main content
    content = soup.select_one("div#mw-content-text")
    if not content:
        raise ValueError("Could not find Wikipedia article content.")

    # summary = first 1-2 non-empty paragraphs
    paragraphs = content.select("p")
    summary_parts = []
    for p in paragraphs:
        t = _clean(p.get_text(" "))
        if t:
            summary_parts.append(t)
        if len(summary_parts) >= 2:
            break
    summary = " ".join(summary_parts) if summary_parts else None

    # sections from headings
    section_tags = content.select("h2 .mw-headline, h3 .mw-headline")
    sections = []
    for s in section_tags[:30]:
        st = _clean(s.get_text(" "))
        if st and st.lower() not in ("references", "external links", "see also"):
            sections.append(st)

    # full text: paragraphs + list items (clipped)
    text_chunks = []
    for el in content.select("p, li"):
        t = _clean(el.get_text(" "))
        if t:
            text_chunks.append(t)
    full_text = "\n".join(text_chunks)

    return {
        "url": url,
        "title": title,
        "summary": summary,
        "sections": sections,
        "full_text": full_text,
        "raw_html": html,  # bonus: store raw HTML
    }
