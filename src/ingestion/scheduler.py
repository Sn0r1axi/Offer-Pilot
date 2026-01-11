
import asyncio
from typing import List
from src.ingestion.crawler import UniversityCrawler, University

async def main():
    """
    Main entry point to schedule and run the university crawler.
    """
    
    # Target Universities (Top 5 "Vibe Check")
    target_universities = [
        University(name="MIT", url="https://www.mit.edu/admissions/", rank=1),
        University(name="Cambridge", url="https://www.undergraduate.study.cam.ac.uk/", rank=2),
        University(name="Oxford", url="https://www.ox.ac.uk/admissions", rank=3),
        University(name="Harvard", url="https://college.harvard.edu/admissions", rank=4),
        University(name="Stanford", url="https://www.stanford.edu/admission/", rank=5)
    ]
    
    crawler = UniversityCrawler()
    
    print(f"Initializing crawl for {len(target_universities)} universities...")
    
    # Run sequentially using the batch method
    results = await crawler.crawl_universities(target_universities)
    
    await crawler.save_results(results)
    print("Crawl session completed.")

if __name__ == "__main__":
    asyncio.run(main())
