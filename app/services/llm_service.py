import time

from openai import OpenAI
from app.core.config import settings
from app.core.logger import logger


client = OpenAI(
    base_url=settings.OLLAMA_BASE_URL,
    api_key="dummy"
)

class LLMService:
    @staticmethod
    def generate_rag_answer(question: str, context_notes: list[dict]) -> str:
        context_texts = []
        for note in context_notes:
            context_texts.append(f"--- Note ID: {note['id']} ---\nTitle: {note['title']}\nContent: {note['content']}")

        full_context = "\n\n".join(context_texts)

        system_prompt = (
            "You are a helpful personal assistant managing a 'Second Brain' note system. "
            "Answer the user's question using ONLY the context provided below. "
            "If the context does not contain the answer, politely state that you cannot answer based on the current notes. "
            "Answer in Brazilian Portuguese."
        )
        user_prompt = f"Context:\n{full_context}\n\nQuestion: {question}"

        logger.info(f"Starting LLM generation for question: '{question}' with {len(context_notes)} context notes.")
        start_time = time.time()

        try:
            response = client.chat.completions.create(
                model=settings.LLM_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2 
            )

            inference_time = time.time() - start_time
            logger.info(f"LLM Generation successful. Inference time: {inference_time:.2f}s")

            return response.choices[0].message.content # type: ignore

        except Exception as e:
            logger.error(f"Error communicating with local LLM: {str(e)}")
            return f"Error communicating with local LLM: {str(e)}"
