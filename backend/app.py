from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import requests, re
from bs4 import BeautifulSoup
from langchain_google_genai import ChatGoogleGenerativeAI

app = FastAPI()

# Summarization model using LangChain
summarizer = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key="AIzaSyC2YG-msSXWXOxnzaxSlEPnQE4scpNLOAc")

# Base URLs
GOOGLE_SCHOLAR_URL = "https://scholar.google.com/scholar?q="
PAPERS_WITH_CODE_URL = "https://paperswithcode.com/search?q="

@app.get("/")
def home():
    return {"message": "Welcome to the Research Paper Assistant API!"}

@app.get("/scholar_search")
def search_papers(query: str):
    """
    Search Google Scholar for recent papers based on the query.
    """
    try:
        scholar_url = f"{GOOGLE_SCHOLAR_URL}{query.replace(' ', '+')}"
        response = requests.get(scholar_url)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error fetching data from Google Scholar.")

        soup = BeautifulSoup(response.text, "html.parser")
        papers = []

        # Parse results
        for result in soup.select(".gs_ri"):
            title = re.sub(r'\[\s*(html|pdf)\s*\]', '', result.select_one(".gs_rt").text, flags=re.IGNORECASE).strip() if result.select_one(".gs_rt") else "N/A"
            link = result.select_one(".gs_rt a")["href"] if result.select_one(".gs_rt a") else "N/A"
            summary = result.select_one(".gs_rs").text if result.select_one(".gs_rs") else "N/A"
            metadata = result.select_one(".gs_a").text if result.select_one(".gs_a") else "N/A"

            papers.append({
                "title": title,
                "link": link,
                "code": "N/A",
                "summary": summary,
                "metadata": metadata
            })

        return {"papers": papers}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_code")
def fetch_code(query: str):
    """
    Check Papers With Code for available implementations.
    """
    try:
        papers_with_code_url = f"{PAPERS_WITH_CODE_URL}{query.replace(' ', '+')}"
        response = requests.get(papers_with_code_url)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error fetching data from Papers With Code.")

        soup = BeautifulSoup(response.text, "html.parser")
        codes = []

        # Parse results
        for result in soup.select(".paper-card"):
            title = result.select_one("h1").text.strip() if result.select_one("h1") else "N/A"
            link = result.select_one("a")["href"] if result.select_one("a") else "N/A"
            code = f"{link}#code" if link!="N/A" else "N/A"
            summary = result.select_one(".item-strip-abstract").text.strip() if result.select_one(".item-strip-abstract") else "N/A" 
            metadata = result.select_one(".author-name-text").text.strip() if result.select_one(".author-name-text") else "N/A"

            codes.append({
                "title": title if title!="N/A" else "N/A",
                "link": f"https://paperswithcode.com{link}" if link!="N/A" else "N/A",
                "code": f"https://paperswithcode.com{code}" if code!="N/A" else "N/A",
                "summary" : f"{summary}" if summary!="N/A" else "N/A",
                "metadata": f"{metadata}" if metadata!="N/A" else "N/A"
            })

        return {"codes": codes}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search")
def merged_search(query: str):
    """
    Merge results from Google Scholar and Papers With Code.
    """
    try:
        # Fetch papers from Google Scholar
        search_results = search_papers(query=query).get("papers", [])

        # Fetch codes from Papers With Code
        code_results = fetch_code(query=query).get("codes", [])

        # Format code results for consistency and append to search results
        for code in code_results:
            search_results.append({
                "title": code.get("title", "N/A"),
                "link": code.get("link", "N/A"),
                "code": code.get("code", "N/A"),
                "summary": code.get("summary", "N/A"),  # No summary available in code results
                "metadata": code.get("metadata", "N/A"),  # No metadata available in code results
            })

        return {"merged_results": search_results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summarize")
def summarize_text(text: str = Query(..., description="Text to summarize")):
    """
    Summarize the given text.
    """
    try:
        summary = summarizer.invoke(f"summarize the following text in no more than 130 word: {text}")
        return {"summary": summary[0]["summary_text"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
