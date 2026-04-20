from agents.orchestrator import Orchestrator

if __name__ == "__main__":
    # Ask the user to input a research topic
    # .strip() removes any leading/trailing whitespace
    query = input("Enter research topic: ").strip()

    # If the user enters nothing, fall back to a default query
    if not query:
        print("Using default query: droop control")
        query = "droop control"

    # Create an instance of the orchestrator (pipeline controller)
    orchestrator = Orchestrator()

    # Run the full pipeline with the given query
    orchestrator.run(query)