from tavily import TavilyClient
from app.config.settings import settings

client = TavilyClient(api_key=settings.TAVILY_API_KEY)

def search_claim(claim: str):
    response = client.search(
        query=claim,
        search_depth="basic",
        max_results=3
    )

    return response