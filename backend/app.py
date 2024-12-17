from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import requests, re
from bs4 import BeautifulSoup
from langchain_google_genai import ChatGoogleGenerativeAI

#from transformers import pipeline

app = FastAPI()

# Summarization model using Hugging Face Transformers
#summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
summarizer = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key="AIzaSyC2YG-msSXWXOxnzaxSlEPnQE4scpNLOAc")

# Base URLs
GOOGLE_SCHOLAR_URL = "https://scholar.google.com/scholar?q="
PAPERS_WITH_CODE_URL = "https://paperswithcode.com/search?q="


@app.get("/")
def home():
    return {"message": "Welcome to the Research Paper Assistant API!"}


@app.get("/search")
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
            title = result.select_one(".paper-title").text.strip() if result.select_one(".paper-title") else "N/A"
            link = result.select_one("a")["href"] if result.select_one("a") else "N/A"
            is_code_available = bool(result.select_one(".badge-primary"))

            codes.append({
                "title": title,
                "link": f"https://paperswithcode.com{link}",
                "code_available": is_code_available
            })

        return {"codes": codes}

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


@app.get("/compare_papers")
def compare_papers(query: str):
    """
    Fetch papers, check for code, and generate a comparative review.
    """
    try:
        # Fetch papers from Google Scholar
        papers = search_papers(query=query).get("papers", [])

        # Fetch code availability from Papers With Code
        codes = fetch_code(query=query).get("codes", [])

        # Generate comparison
        comparison = []
        for paper in papers:
            paper_code = next((code for code in codes if code["title"] in paper["title"]), None)
            comparison.append({
                "title": paper["title"],
                "summary": paper["summary"],
                "link": paper["link"],
                "metadata": paper["metadata"],
                "code_available": bool(paper_code),
                "code_link": paper_code["link"] if paper_code else None
            })

        return {"comparison": comparison}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
