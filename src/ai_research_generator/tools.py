
import json
from ddgs import DDGS
from crewai.tools import tool


# --------------------------------------------------
# 1. DuckDuckGo Search Tool
# --------------------------------------------------

@tool("DuckDuckGo Search")
def duckduckgo_search(query: str) -> str:
    """
    Search the web and return research results
    in JSON format.
    """

    try:
        search_results = DDGS().text(
            query,
            max_results=5
        )

        formatted_results = []

        for result in search_results:
            formatted_results.append({
                "title": result.get("title", ""),
                "url": result.get("href", ""),
                "description": result.get("body", "")
            })

        return json.dumps(
            formatted_results,
            indent=2,
            ensure_ascii=False
        )

    except Exception as e:
        return json.dumps({
            "error": f"Search failed: {str(e)}"
        })


# --------------------------------------------------
# 2. Lazy-loaded Embedding Model
# --------------------------------------------------

model = None
similarity_util = None


def get_embedding_model():
    """
    Load Sentence Transformers only when required.
    """

    global model, similarity_util

    if model is None:
        print("Loading semantic embedding model...")

        from sentence_transformers import (
            SentenceTransformer,
            util
        )

        model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        similarity_util = util

        print("Embedding model loaded successfully!")

    return model, similarity_util


# --------------------------------------------------
# 3. Python Semantic Relevance Evaluation
# --------------------------------------------------

def evaluate_relevance(topic: str, research_json: str) -> str:
    """
    Evaluate semantic relevance of research sources.

    This is a normal Python function, not an LLM tool.

    Arguments:
        topic: User's research topic.
        research_json: JSON list containing research sources.

    Returns:
        JSON containing ranked sources and similarity scores.
    """

    try:
        sources = json.loads(research_json)

        if not isinstance(sources, list) or not sources:
            raise ValueError("No valid research sources found.")

        model, util = get_embedding_model()

        documents = [
            f"{source.get('title', '')}. "
            f"{source.get('description', '')}"
            for source in sources
        ]

        topic_embedding = model.encode(
            topic,
            convert_to_tensor=True
        )

        document_embeddings = model.encode(
            documents,
            convert_to_tensor=True
        )

        scores = util.cos_sim(
            topic_embedding,
            document_embeddings
        )[0]

        results = []

        for i, score in enumerate(scores):

            results.append({
                "title": sources[i].get("title", ""),
                "url": sources[i].get("url", ""),
                "description": sources[i].get("description", ""),
                "relevance_score": round(score.item(), 3)
            })

        results.sort(
            key=lambda x: x["relevance_score"],
            reverse=True
        )

        return json.dumps(
            results,
            indent=2,
            ensure_ascii=False
        )

    except Exception as e:
        raise RuntimeError(
            f"Semantic relevance evaluation failed: {str(e)}"
        ) from e

@tool("Python Semantic Relevance Evaluation")
def semantic_relevance_tool(topic: str, research_json: str) -> str:
    """
    Evaluate the semantic relevance of research sources against the topic.
    Returns sources ranked by semantic similarity scores.
    """

    return evaluate_relevance(
        topic=topic,
        research_json=research_json
    )

