# shopkart_rag.py — minimal RAG loop for ShopKart customer support

import os  # Read environment variables like GROQ_API_KEY
import chromadb  # Vector database for storing and searching policy chunks
from sentence_transformers import SentenceTransformer  # Loads the BGE embedding model for retriever
from groq import Groq  # Client for LLM generation API calls (free, OpenAI-compatible)

# ---------------------------------------------------------------------------
# ShopKart policy records — these are our knowledge sources for this lab
# Each dict becomes one row in Chroma: id, text, metadata
# ---------------------------------------------------------------------------
POLICY_RECORDS = [
    {  # Returns policy chunk
        "id": "shopkart_returns_1",  # Unique primary key for this policy row
        "text": (
            "Unopened items may be returned within 7 calendar days of delivery. "
            "Opened or used items are not eligible unless defective."
        ),  # Human-readable returns rule — source of truth for return questions
        "metadata": {"category": "returns", "source": "returns_policy"},  # Tags for display and later filtering
    },
    {  # Shipping policy chunk
        "id": "shopkart_shipping_1",  # Unique id for shipping row
        "text": (
            "Standard delivery takes 3 to 5 business days after dispatch. "
            "Express delivery (paid) arrives in 1 to 2 business days in metro cities only."
        ),  # Shipping timelines customers ask about often
        "metadata": {"category": "shipping", "source": "shipping_policy"},  # Shipping category tag
    },
    {  # Warranty policy chunk
        "id": "shopkart_warranty_1",  # Unique id for warranty row
        "text": (
            "Electronics carry a 12-month manufacturer warranty from the date of delivery. "
            "Warranty does not cover physical damage or liquid exposure."
        ),  # Warranty coverage and exclusions
        "metadata": {"category": "warranty", "source": "warranty_policy"},  # Warranty category tag
    },
    {  # Refund policy chunk
        "id": "shopkart_refunds_1",  # Unique id for refund row
        "text": (
            "Refunds are credited within 5 to 7 business days after the returned item "
            "passes warehouse verification. Cash-on-delivery orders are refunded to the "
            "original UPI or bank account only."
        ),  # Refund timing and COD path
        "metadata": {"category": "refunds", "source": "refunds_policy"},  # Refunds category tag
    },
]

# Embedding model name — MUST stay the same for documents and every query
EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"  # Free BGE model from Hugging Face

# LLM model name for generation — free Groq model; swap for any model Groq lists
GENERATION_MODEL_NAME = "llama-3.3-70b-versatile"  # Groq-hosted LLM used as the generator