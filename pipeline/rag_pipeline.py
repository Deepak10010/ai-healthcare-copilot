from agents.planner import planner_agent
from agents.retriever import retriever_agent
from agents.generator import generator_agent
from agents.evaluator import evaluator_agent


def ask_question_agentic(db, query, max_retries=2):

    print("\n==============================")
    print("🧠 STEP 1: Planner Agent")
    print("==============================")

    plan = planner_agent(query)
    print(plan)

    print("\n==============================")
    print("🔎 STEP 2: Retriever Agent")
    print("==============================")

    context = retriever_agent(db, query)

    print("\n==============================")
    print("🤖 STEP 3: Generator Agent")
    print("==============================")

    attempt = 0

    while attempt <= max_retries:

        print(f"\n🔁 Attempt {attempt + 1}")

        answer = generator_agent(query, context)

        print("\n🧪 Evaluating answer...")
        evaluation = evaluator_agent(query, context, answer)

        print("\n📊 Evaluation Result:\n")
        print(evaluation)

        # Simple rule-based check
        if "GOOD" in evaluation.upper():
            print("\n✅ Answer accepted!")
            return answer

        print("\n⚠️ Answer not good, retrying...\n")

        attempt += 1

    print("\n❌ Max retries reached. Returning best attempt.")
    return answer