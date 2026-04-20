from agents.orchestrator import Orchestrator


def evaluate(query):
    # Create an instance of the orchestrator (pipeline controller)
    orch = Orchestrator()

    # Run the full pipeline using the given query
    result = orch.run(query)

    # Extract key metrics from the pipeline result
    retrieved = result["retrieved"]   # Total papers fetched
    cleaned = result["cleaned"]       # Papers remaining after cleaning
    classified = result["classified"] # Papers successfully ranked/classified

    # Ratio of cleaned papers to retrieved papers
    # Measures how much useful data remains after cleaning
    retrieval_clean_ratio = cleaned / retrieved if retrieved else 0

    # Ratio of classified papers to cleaned papers
    # Measures how many cleaned papers are actually usable/relevant
    validity_ratio = classified / cleaned if cleaned else 0

    # Weighted quality score
    # 40% weight on cleaning effectiveness, 60% on classification quality
    quality_score = (retrieval_clean_ratio * 0.4) + (validity_ratio * 0.6)

    # Store all evaluation metrics in a dictionary
    report = {
        "retrieved": retrieved,
        "cleaned": cleaned,
        "classified": classified,
        "retrieval_clean_ratio": retrieval_clean_ratio,
        "validity_ratio": validity_ratio,
        "quality_score": quality_score,
        "runtime": result.get("runtime", 0)  # Default to 0 if runtime missing
    }

    # Print a formatted evaluation report
    print("\n📊 EVALUATION REPORT")
    for k, v in report.items():
        print(f"{k}: {v}")

    # Return report for further use (e.g., logging, testing, comparisons)
    return report


if __name__ == "__main__":
    # Prompt user to input a test query
    query = input("Enter test query: ")

    # Run evaluation on the input query
    evaluate(query)