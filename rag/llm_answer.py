from vector_search import search

def build_prompt(context, question):
    return f"""
You are an environmental intelligence assistant.

Answer ONLY using the information provided below.
If the answer is not present, say:
"I don't have enough data to answer that."

Do NOT guess.
Do NOT add new facts.
Do NOT make predictions.

Context:
{context}

Question:
{question}

Answer:
"""

def fake_llm(prompt):
    """
    This simulates an LLM for demo purposes.
    In real deployment, replace this with OpenAI/Claude API call.
    """
    # Very simple: just return the context-based explanation
    return prompt.split("Context:")[1].split("Question:")[0].strip()

def answer_question(question):
    # 1. Retrieve relevant chunks
    results = search(question, top_k=3)

    # 2. Build context
    context = ""
    for score, text, source in results:
        context += f"- {text}\n"

    # 3. Build prompt
    prompt = build_prompt(context, question)

    # 4. Get answer from LLM
    answer = fake_llm(prompt)

    return answer


if __name__ == "__main__":
    q = "Is AQI 320 dangerous for children?"
    response = answer_question(q)

    print("QUESTION:", q)
    print("-" * 50)
    print("ANSWER:")
    print(response)


