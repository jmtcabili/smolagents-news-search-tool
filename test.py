#from tools.news_search import NewsSearchTool

#ai_news_search = NewsSearchTool()

#print(ai_news_search.forward(company="Openai"))

import os, requests
from dotenv import load_dotenv

load_dotenv() 


r = requests.get(
    "https://generativelanguage.googleapis.com/v1beta/models",
    params={"key": os.environ["GEMINI_KEY"], "pageSize": 100},
    timeout=20,
)
for m in r.json()["models"]:
    if "generateContent" in m.get("supportedGenerationMethods", []):
        print(m["name"].replace("models/", "gemini/"))