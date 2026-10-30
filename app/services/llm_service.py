from openai import OpenAI
from app.core.config import settings


client = OpenAI(
    base_url=settings.OLLAMA_BASE_URL,
    api_key="dummy"
)

class LLMService:
    @staticmethod
    def generate_rag_answer(question: str, context_notes: list[dict]) -> str:
        # 1. Format the retrieved notes into a single context string
        context_texts = []
        for note in context_notes:
            context_texts.append(f"--- Note ID: {note['id']} ---\nTitle: {note['title']}\nContent: {note['content']}")

        full_context = "\n\n".join(context_texts)

        # 2. Build the System Prompt (Prompt Engineering)
        # Here we lock the AI down so it doesn't hallucinate
        system_prompt = (
            "You are a helpful personal assistant managing a 'Second Brain' note system. "
            "Answer the user's question using ONLY the context provided below. "
            "If the context does not contain the answer, politely state that you cannot answer based on the current notes."
        )

        user_prompt = f"Context:\n{full_context}\n\nQuestion: {question}"

        # 3. Call the LLM API
        try:
            response = client.chat.completions.create(
                model=settings.LLM_MODEL, # maybe llama3-8b-8192
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2 # Low temperature means that the model will be more factual than creative
            )
            return response.choices[0].message.content # type: ignore

        except Exception as e:
            return f"Error communicating with LLM: {str(e)}"
