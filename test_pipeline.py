import pytest
from agents.orchestrator import Orchestrator
from agents.processing import ProcessingAgent
from agents.storage import StorageAgent


# ----------------------------
# TEST ORCHESTRATOR FACTORY
# ----------------------------

def create_test_orchestrator(tmp_path):
    # Create a normal orchestrator instance
    orch = Orchestrator()

    # Override storage so tests write to a temporary directory instead of real files
    orch.storage = StorageAgent(output_prefix=str(tmp_path / "pipeline"))

    return orch


# ----------------------------
# CLEANING TEST
# ----------------------------

def test_cleaning_removes_invalid_and_duplicates():
    # Create processing agent (unit under test)
    agent = ProcessingAgent()

    # Raw input includes:
    # - duplicate paper
    # - empty title (invalid)
    # - empty authors (invalid)
    raw = [
        {"title": "Paper A", "authors": ["X"], "year": "2020", "doi": "1"},
        {"title": "Paper A", "authors": ["X"], "year": "2020", "doi": "1"},
        {"title": "", "authors": ["X"], "year": "2020", "doi": "2"},
        {"title": "Paper B", "authors": [], "year": "2020", "doi": "3"},
    ]

    # Run cleaning step
    cleaned = agent.clean(raw)

    # Only one valid unique paper should remain
    assert len(cleaned) == 1
    assert cleaned[0]["title"] == "Paper A"


# ----------------------------
# CLASSIFICATION TEST
# ----------------------------

def test_classification_outputs_relevance_score():
    # Create processing agent
    agent = ProcessingAgent()

    # Sample papers with different topics
    papers = [
        {"title": "photovoltaic solar energy microgrid", "authors": ["A"], "year": "2020", "doi": "1"},
        {"title": "deep learning image classification", "authors": ["B"], "year": "2021", "doi": "2"},
    ]

    # Run TF-IDF classification
    result = agent.classify(papers)

    # Ensure both papers are processed
    assert len(result) == 2

    # Check that each result contains relevance scoring
    for r in result:
        assert "relevance_score" in r

        # Score should always be normalized between 0 and 1
        assert 0.0 <= r["relevance_score"] <= 1.0


# ----------------------------
# STORAGE TEST
# ----------------------------

def test_storage_creates_files(tmp_path):
    # Create storage agent pointing to temporary test directory
    storage = StorageAgent(output_prefix=str(tmp_path / "test_papers"))

    # Sample input paper
    papers = [
        {"title": "Test Paper", "authors": ["A"], "year": "2023", "doi": "123"}
    ]

    # Save pipeline output
    storage.save(papers)

    # Ensure all expected output files exist
    assert (tmp_path / "test_papers.csv").exists()
    assert (tmp_path / "test_papers.json").exists()
    assert (tmp_path / "test_papers.db").exists()


# ----------------------------
# FULL PIPELINE TEST
# ----------------------------

def test_orchestrator_pipeline_runs_end_to_end(tmp_path):
    # Create orchestrator with isolated storage
    orch = create_test_orchestrator(tmp_path)

    # Run full pipeline
    result = orch.run("machine learning")

    # Basic validation of output structure
    assert isinstance(result, dict)
    assert "status" in result

    # Ensure pipeline produced storage output
    assert (tmp_path / "pipeline.csv").exists()