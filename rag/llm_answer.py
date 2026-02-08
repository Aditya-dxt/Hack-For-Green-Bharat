from vector_search import search


def build_prompt(context, question):
    return f"""
You are an environmental intelligence assistant.

Answer ONLY using the information provided below.
If the answer is not present, say:
"I don't have enough data to answer that."

Context:
{context}

Question:
{question}

Answer:
"""


def call_llm(prompt):
    # FALLBACK DEMO MODE (NO API REQUIRED)
    return (
        "Based on the retrieved environmental guidelines, "
        "an AQI value above 300 is classified as very poor and "
        "is considered hazardous, especially for children, "
        "elderly individuals, and people with lung or heart disease."
    )


def answer_question(question):
    results = search(question, top_k=3)

    context = ""
    for score, text, source in results:
        context += f"- {text}\n"

    prompt = build_prompt(context, question)
    answer = call_llm(prompt)

    return answer


if __name__ == "__main__":
    q = "Is AQI 320 dangerous for children?"
    response = answer_question(q)

    print("QUESTION:", q)
    print("-" * 50)
    print("ANSWER:")
    print(response)
