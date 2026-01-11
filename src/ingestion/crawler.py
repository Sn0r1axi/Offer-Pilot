import asyncio
import re
from typing import List, Optional, Set
from pydantic import BaseModel, HttpUrl
from crawl4ai import AsyncWebCrawler

class Page(BaseModel):
    url: str
    content: str

class University(BaseModel):
    """
    Pydantic model representing a University.
    """
    name: str
    url: HttpUrl
    rank: int
    content: Optional[str] = None
    sub_pages: List[Page] = []

class UniversityCrawler:
    """
    Async crawler for university admission pages using Crawl4AI.
    """

    def __init__(self):
        """Initializes the UniversityCrawler."""
        self.keywords = [
            "admission", "apply", "requirement", "tuition", "deadline", 
            "undergraduate", "international", "fee", "cost", "scholarship"
        ]

    def _is_relevant_url(self, url: str, base_url: str) -> bool:
        """Checks if a URL is relevant for admissions."""
        # Ensure it belongs to the same domain (rough check) or is a relative link
        if not url.startswith(base_url) and not url.startswith("/"):
             # Handle subdomains or different paths if strictly matching base is too restrictive
             # For now, simplistic check: contain base domain or be relative
             pass
        
        # Check against keywords
        lower_url = url.lower()
        return any(k in lower_url for k in self.keywords)

    async def crawl_universities(self, universities: List[University]) -> List[University]:
        """
        Crawls a list of universities sequentially using a single browser session.
        Performs a depth=2 crawl for relevant admission pages.

        Args:
            universities (List[University]): List of universities to crawl.

        Returns:
            List[University]: The updated list with content.
        """
        async with AsyncWebCrawler(verbose=True) as crawler:
            for uni in universities:
                print(f"Starting crawl for {uni.name} at {uni.url}...")
                try:
                    # 1. Crawl Main Page
                    result = await crawler.arun(url=str(uni.url))
                    if not result.success:
                        print(f"Failed to crawl main page for {uni.name}: {result.error_message}")
                        continue
                    
                    uni.content = result.markdown
                    print(f"  - Main page fetched ({len(result.markdown)} bytes)")

                    # 2. Extract Links (Depth=1 candidates)
                    # Crawl4AI might provide links, or we parse from markdown/html.
                    # For simplicity, let's assume we can regex specific links or if Crawl4AI has a links property.
                    # Looking at Crawl4AI docs (simulated), result usually has .links
                    # If not, we rely on a simple regex on the markdown or using a helper if available.
                    # Let's try to infer links from the markdown for now as a fallback or use result.links if standard
                    
                    # NOTE: Assuming result.links exists as list of dicts or strings. 
                    # If not, we will need to implement a parser.
                    # Let's rely on 'result.links' (common in crawlers). 
                    # If it fails, I'll add a beautifulsoup fallback in next step.
                    
                    extracted_urls = set()
                    
                    # 1. Try result.links
                    if hasattr(result, 'links') and result.links:
                        links = result.links
                        if isinstance(links, dict):
                             extracted_urls.update(links.keys())
                        elif isinstance(links, list):
                             for item in links:
                                 if isinstance(item, dict):
                                     href = item.get('href')
                                     if href:
                                         extracted_urls.add(href)
                                 elif isinstance(item, str):
                                     extracted_urls.add(item)
                    
                    # 2. Always try Regex on Markdown (for safety and relative links)
                    # Catches [text](url) where url can be anything not containing )
                    markdown_links = re.findall(r'\[.*?\]\(([^)]+)\)', result.markdown)
                    extracted_urls.update(markdown_links)
                    
                    print(f"  - Found {len(extracted_urls)} unique links on main page (combined sources).")
                    
                    print(f"  - Found {len(extracted_urls)} links on main page.")

                    # 3. Filter Relevant Links
                    relevant_urls = []
                    base_domain = str(uni.url).split("://")[-1].split("/")[0] # naive domain extraction
                    
                    for link in extracted_urls:
                        # Normalize relative links (rudimentary)
                        if link.startswith("/"):
                            link = f"{str(uni.url).rstrip('/')}{link}"
                        
                        if base_domain in link and self._is_relevant_url(link, str(uni.url)):
                            relevant_urls.append(link)

                    # Deduplicate
                    relevant_urls = list(set(relevant_urls))
                    print(f"  - Identifying {len(relevant_urls)} relevant sub-pages to crawl.")

                    # 4. Crawl Sub-pages (Depth=2)
                    # Limit to avoid taking forever (e.g., max 10 sub-pages)
                    max_sub_pages = 5
                    for sub_url in relevant_urls[:max_sub_pages]:
                         print(f"    -> Crawling sub-page: {sub_url}")
                         sub_result = await crawler.arun(url=sub_url)
                         if sub_result.success:
                             uni.sub_pages.append(Page(url=sub_url, content=sub_result.markdown))
                         else:
                             print(f"       Failed: {sub_result.error_message}")
                    
                except Exception as e:
                    print(f"Error crawling {uni.name}: {e}")
        
        return universities

    async def save_results(self, universities: List[University], output_dir: str = "data/raw"):
        """
        Saves the crawled data to JSON files.

        Args:
            universities (List[University]): List of crawled university objects.
            output_dir (str): Directory to save the files.
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        for uni in universities:
            if uni.content:
                filename = f"{output_dir}/{uni.name.replace(' ', '_').lower()}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(uni.model_dump_json(indent=2))
                print(f"Saved data for {uni.name} to {filename}")
