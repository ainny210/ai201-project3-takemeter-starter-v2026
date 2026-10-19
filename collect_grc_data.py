import csv
import json
import time
from urllib.parse import urlencode
from urllib.request import urlopen

searches = {
    "governance": [
        "information security policy",
        "security governance",
        "organizational security policy",
        "AI governance"
    ],
    "security_risk": [
        "data breach",
        "sensitive data exposure",
        "security risk assessment",
        "AI security"
    ],
    "compliance": [
        "SOC 2",
        "ISO 27001",
        "GDPR compliance",
        "security audit"
    ],
    "vendor_risk": [
        "vendor assessment",
        "third party risk",
        "supplier security",
        "vendor compliance"
    ]
}

all_questions = {}

for topic, search_terms in searches.items():
    for search_term in search_terms:
        params = urlencode({
            "site": "security",
            "q": search_term,
            "pagesize": 100,
            "sort": "relevance"
        })

        url = f"https://api.stackexchange.com/2.3/search/advanced?{params}"

        with urlopen(url, timeout=30) as response:
            data = json.load(response)

        for question in data.get("items", []):
            question_id = question["question_id"]

            if question_id not in all_questions:
                all_questions[question_id] = {
                    "question_id": question_id,
                    "title": question["title"],
                    "source_url": question["link"],
                    "author": question.get("owner", {}).get(
                        "display_name", "Unknown"
                    ),
                    "search_topic": topic
                }

        print(
            f"{topic} | {search_term}: "
            f"{len(data.get('items', []))} candidates"
        )

        time.sleep(2)

with open("candidate_posts.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "question_id",
            "title",
            "source_url",
            "author",
            "search_topic"
        ]
    )

    writer.writeheader()
    writer.writerows(all_questions.values())

print(f"\nTotal unique candidates: {len(all_questions)}")
print("Saved to candidate_posts.csv")