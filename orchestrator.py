from agents.retrieval_agent import RetrievalAgent
from agents.processing import ProcessingAgent
from agents.storage import StorageAgent
from agents.logger import Logger
from tqdm import tqdm
import time


class Orchestrator:
    def __init__(self):
        # Initialize each agent used in the pipeline
        self.retrieval = RetrievalAgent()   # Responsible for fetching raw papers
        self.processing = ProcessingAgent() # Handles cleaning + classification
        self.storage = StorageAgent()       # Saves final results

    def run(self, query):
        # Record start time to measure total runtime
        start_time = time.time()

        # Log the start of the pipeline
        Logger.log(f"Starting pipeline for: {query}")

        # Wrap query in a list (allows easy extension to multiple queries later)
        queries = [query]

        # Store all retrieved papers across queries
        all_papers = []

        # Loop through queries with a progress bar
        for q in tqdm(queries, desc="Queries"):
            # Fetch papers for the current query
            papers = self.retrieval.fetch(q)

            # If results exist, add them to the master list
            if papers:
                all_papers.extend(papers)

            # Small delay to avoid hitting API rate limits
            time.sleep(1)

        # Log how many papers were retrieved
        Logger.log(f"Retrieved {len(all_papers)} papers")

        # Clean/normalize the raw data
        cleaned = self.processing.clean(all_papers)
        Logger.log(f"After cleaning: {len(cleaned)} papers")

        # Classify/rank papers based on relevance to the query
        ranked = self.processing.classify(cleaned, query=query)

        # If no valid results after classification, stop early
        if not ranked:
            Logger.error("No valid papers after ranking.")
            return {
                "status": "failed",
                "retrieved": len(all_papers),
                "cleaned": len(cleaned),
                "classified": 0,
                "runtime": time.time() - start_time
            }

        # Save the final ranked results (CSV, JSON, DB)
        self.storage.save(ranked)

        # Calculate total runtime
        total_time = time.time() - start_time

        # Log completion time
        Logger.log(f"Pipeline completed in {total_time:.2f}s")

        # Return a summary of the pipeline execution
        return {
            "status": "success",
            "retrieved": len(all_papers),
            "cleaned": len(cleaned),
            "classified": len(ranked),
            "runtime": total_time,
            # Return the highest relevance score (top-ranked paper)
            "top_score": ranked[0]["relevance_score"] if ranked else 0
        }