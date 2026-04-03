from agents.planner import planner_agent
from agents.retriever import retriever_agent
from agents.generator import generator_agent


def ask_question_agentic(db, query):
    """
    Full Agentic RAG Pipeline:
    1. Planner Agent → decides steps
    2. Retriever Agent → fetches relevant context
    3. Generator Agent → produces answer
    """

    print("\n==============================")
    print("🧠 STEP 1: Planner Agent")
    print("==============================")

    plan = planner_agent(query)
    print(plan)

    print("\n==============================")
    print("🔎 STEP 2: Retriever Agent")
    print("==============================")

    context = retriever_agent(db, query)

    # Debug: show small preview of context
    print("\n📄 Retrieved Context Preview:\n")
    print(context[:500])  # first 500 chars

    print("\n==============================")
    print("🤖 STEP 3: Generator Agent")
    print("==============================")

    answer = generator_agent(query, context)

    print("\n==============================")
    print("✅ FINAL ANSWER")
    print("==============================")

    return answer