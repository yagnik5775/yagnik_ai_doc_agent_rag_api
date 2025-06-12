import os
from dotenv import load_dotenv
from retriever import retrieve_similar
from groq import Groq

# Load environment variables from .env file
load_dotenv()

def generate_response(query):
    # Retrieve chunks from your retriever logic
    chunks = retrieve_similar(query)
    if not chunks:
        return "I couldn't find relevant information to answer your question."
    
    # Join all the text chunks to form the context
    context = "\n".join(chunks)

    # Get Groq API key from environment variable
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        return "Groq API key is not set in the environment."

    # Initialize Groq client with the environment-based API key
    client = Groq(api_key=groq_api_key)

    try:
        # Generate response using Groq's chat model
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a highly intelligent AI assistant specialized in document intelligence. "
                        "You read and analyze PDF-extracted content to provide accurate, concise answers strictly based on the document. "
                        "Do not use external knowledge or make assumptions. If the answer is not found in the text, say: "
                        "'The answer is not available in the provided document.'"
                    )
                },
                {
                    "role": "user",
                    "content": f"Context:\n{context}\n\nQuestion: {query}\n\nProvide a concise answer based only on the context. If you can't answer from the context, say so."
                }
            ],
            model="llama3-8b-8192",
            temperature=0.3,
            max_tokens=1024
        )

        return chat_completion.choices[0].message.content

    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return "An error occurred while calling the Groq API."
