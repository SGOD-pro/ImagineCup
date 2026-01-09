from tavily import TavilyClient

tavily_client = TavilyClient(api_key="tvly-YOUR_API_KEY")
response = tavily_client.extract("Who is Leo Messi?",urls=["https://en.wikipedia.org/wiki/Leo_Messi"])

print(response)     