import requests
import os
import logging

print("📥 Імпортовано confluence.py")

def search_confluence(query):
    BASE_URL = os.getenv("CONFLUENCE_BASE_URL")
    TOKEN = os.getenv("CONFLUENCE_API_TOKEN")

    if not BASE_URL or not TOKEN:
        raise ValueError("❗ BASE_URL або TOKEN не задані.")

    url = f"{BASE_URL}/rest/api/content/search"
    params = {
        "cql": f'text ~ "{query}"',
        "limit": 3,
        "expand": "body.summary"
    }

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/json"
    }

    logging.info(f"🔎 Виконую GET {url} з query: {query}")
    response = requests.get(url, params=params, headers=headers)

    if not response.ok:
        raise Exception(f"❗ Помилка Confluence API: {response.status_code} — {response.text}")

    results = response.json().get("results", [])
    logging.info(f"✅ Отримано {len(results)} результат(и)")

    return [
        {
            "title": r["title"],
            "link": f"{BASE_URL}{r['_links']['webui']}",
            "summary": r.get("body", {}).get("summary", {}).get("value", "...")
        } for r in results
    ]
