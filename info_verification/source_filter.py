from typing import List, Literal, Optional
from abc import ABC, abstractmethod
import hashlib
import pickle
import os
from pathlib import Path

# BM25 imports
try:
    from rank_bm25 import BM25Okapi
except ImportError:
    BM25Okapi = None

import litellm
# OpenAI Embedding
import openai
import tiktoken
import numpy as np
import asyncio


class EmbeddingCache:
    """Class to cache embedding results"""
    
    def __init__(self, cache_dir: str = "embedding_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
    
    def _get_cache_key(self, text: str, model: str) -> str:
        """Generate a cache key from text and model name"""
        content = f"{model}:{text}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def get(self, text: str, model: str) -> Optional[List[float]]:
        """Get embedding from cache"""
        cache_key = self._get_cache_key(text, model)
        cache_file = self.cache_dir / f"{cache_key}.pkl"
        
        if cache_file.exists():
            try:
                with open(cache_file, 'rb') as f:
                    return pickle.load(f)
            except Exception:
                # Ignore if cache file is corrupted
                pass
        return None
    
    def set(self, text: str, model: str, embedding: List[float]):
        """Save embedding to cache"""
        cache_key = self._get_cache_key(text, model)
        cache_file = self.cache_dir / f"{cache_key}.pkl"
        
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(embedding, f)
        except Exception:
            # Ignore cache save failures
            pass


# Global cache instance
_embedding_cache = EmbeddingCache()


class ChunkSelector(ABC):
    @abstractmethod
    async def select(self, queries: List[str], chunks: List[str], top_k: int) -> str:
        pass

class BM25ChunkSelector(ChunkSelector):
    async def select(self, queries: List[str], chunks: List[str], top_k: int) -> str:
        if BM25Okapi is None:
            raise ImportError("rank_bm25 module is not installed. Please install it with `pip install rank-bm25`.")
            
        selected_indices = set()
        bm25 = BM25Okapi([chunk.split() for chunk in chunks])
        
        # Select top-k chunks for each query
        for query in queries:
            scores = bm25.get_scores(query.split())
            # Sort indices by descending score
            ranked_indices = np.argsort(scores)[::-1]
            # Select top-k
            for i in range(min(top_k, len(ranked_indices))):
                selected_indices.add(ranked_indices[i])
        
        # Join chunks in their original order
        selected_indices = sorted(selected_indices)
        selected_chunks = [chunks[i] for i in selected_indices]
        # return '\n\n'.join(selected_chunks)
        return "\n\n...\n\n".join(selected_chunks)

class OpenAIEmbeddingChunkSelector(ChunkSelector):
    def __init__(self, model: str = "text-embedding-3-large"):
        # openai.api_key = openai_api_key
        self.model = model

    async def get_embedding(self, text: str) -> List[float]:
        # Check cache first
        cached_embedding = _embedding_cache.get(text, self.model)
        if cached_embedding is not None:
            return cached_embedding
        
        # If not in cache, call API
        try:
            response = await litellm.aembedding(self.model, input=[text])
            embedding = response['data'][0]['embedding']
            
            # Save to cache
            _embedding_cache.set(text, self.model, embedding)
            return embedding
        except Exception as e:
            print(f"Error getting OpenAI embedding: {e}")
            return [0.0] * 1536  # Default dimension

    def cosine_similarity(self, a, b):
        a = np.array(a)
        b = np.array(b)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    async def select(self, queries: List[str], chunks: List[str], top_k: int) -> str:
        selected_indices = set()
        
        # Pre-calculate chunk embeddings
        chunk_embs = await asyncio.gather(*(self.get_embedding(chunk) for chunk in chunks))

        # Select top-k chunks for each query
        for query in queries:
            query_emb = await self.get_embedding(query)
            scores = [self.cosine_similarity(query_emb, emb) for emb in chunk_embs]
            # Sort indices by descending score
            ranked_indices = np.argsort(scores)[::-1]
            # Select top-k
            for i in range(min(top_k, len(ranked_indices))):
                selected_indices.add(ranked_indices[i])
        
        # Join chunks in their original order
        selected_indices = sorted(selected_indices)
        selected_chunks = [chunks[i] for i in selected_indices]
        return '\n\n'.join(selected_chunks)

class GeminiChunkSelector(ChunkSelector):
    def __init__(self, model: str = "gemini-embedding-001"):
        from google import genai
        self.model = model
        self.client = genai.Client()
    
    def cosine_similarity(self, a, b):
        a = np.array(a)
        b = np.array(b)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
    async def get_embeddings_batch(self, texts: List[str], task_type: str = "SEMANTIC_SIMILARITY") -> List[List[float]]:
        """Get embeddings in batch (with caching)"""
        from google.genai import types

        embeddings = []
        texts_to_embed = []
        cache_indices = []
        
        # Include task_type in cache key
        cache_model_key = f"{self.model}_{task_type}"
        
        # Check cache first
        for i, text in enumerate(texts):
            cached_embedding = _embedding_cache.get(text, cache_model_key)
            if cached_embedding is not None:
                embeddings.append(cached_embedding)
            else:
                embeddings.append(None)  # Placeholder
                texts_to_embed.append(text)
                cache_indices.append(i)
        
        # Embed uncached texts in batch
        if texts_to_embed:
            try:
                result = self.client.models.embed_content(
                    model=self.model,
                    contents=texts_to_embed,
                    config=types.EmbedContentConfig(task_type=task_type)
                )
                
                batch_embeddings = [np.array(e.values).tolist() for e in result.embeddings]
                
                # Place results in original positions and save to cache
                for i, embedding in enumerate(batch_embeddings):
                    original_index = cache_indices[i]
                    embeddings[original_index] = embedding
                    _embedding_cache.set(texts_to_embed[i], cache_model_key, embedding)
                    
            except Exception as e:
                print(f"Error getting Gemini embeddings: {e}")
                # Return dummy embeddings if failed
                for i in cache_indices:
                    embeddings[i] = [0.0] * 768  # Default dimension
        
        return embeddings
    
    async def select(self, queries: List[str], chunks: List[str], top_k: int) -> str:
        selected_indices = set()
        print("let's go gemini")
        
        # Embed query and chunks with different task_types
        query_embeddings = await self.get_embeddings_batch(queries, task_type="FACT_VERIFICATION")
        chunk_embeddings = await self.get_embeddings_batch(chunks, task_type="RETRIEVAL_DOCUMENT")
        
        # Select top-k chunks for each query
        for query_emb in query_embeddings:
            scores = [self.cosine_similarity(query_emb, chunk_emb) for chunk_emb in chunk_embeddings]
            # Sort indices by descending score
            ranked_indices = np.argsort(scores)[::-1]
            # Select top-k
            for i in range(min(top_k, len(ranked_indices))):
                selected_indices.add(ranked_indices[i])
        
        # Join chunks in their original order
        selected_indices = sorted(selected_indices)
        selected_chunks = [chunks[i] for i in selected_indices]
        return '\n\n'.join(selected_chunks)

class SentenceTransformerChunkSelector(ChunkSelector):
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(model_name)

    async def select(self, queries: List[str], chunks: List[str], top_k: int) -> str:
        selected_indices = set()
        
        # Pre-calculate chunk embeddings
        chunk_embs = self.model.encode(chunks)
        
        # Select top-k chunks for each query
        for query in queries:
            query_emb = self.model.encode([query])[0]
            scores = [np.dot(query_emb, emb) / (np.linalg.norm(query_emb) * np.linalg.norm(emb)) for emb in chunk_embs]
            # Sort indices by descending score
            ranked_indices = np.argsort(scores)[::-1]
            # Select top-k
            for i in range(min(top_k, len(ranked_indices))):
                selected_indices.add(ranked_indices[i])
        
        # Join chunks in their original order
        selected_indices = sorted(selected_indices)
        selected_chunks = [chunks[i] for i in selected_indices]
        return '\n\n'.join(selected_chunks)

def split_text_by_tokens(text, model_name="cl100k_base", max_tokens=4000):
    """
    Function to split text into chunks based on token count
    """
    # Retrieve encoder for the model
    encoding = tiktoken.get_encoding(model_name)
    
    # Convert text to tokens
    cleaned_text = text.replace('<|endoftext|>', '').replace('<|endofprompt|>', '')

    tokens = encoding.encode(cleaned_text)
    
    # Split tokens up to max_tokens limit
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk_tokens = tokens[i:i + max_tokens]
        chunk_text = encoding.decode(chunk_tokens)
        chunks.append(chunk_text)
    
    return chunks


async def limit_tokens_by_chunk(queries: list[str], content, chunk_size=1000, top_k=2, model_name="cl100k_base",
                           method: Literal["bm25", "openai", "sentence_transformer", "gemini"] = "bm25",
                           sentence_transformer_model: str = None,
                           openai_model: str = "text-embedding-3-large",
                           gemini_model: str = "gemini-embedding-001"):
    """
    Selects top K chunks most relevant to each query using the specified method,
    removes duplicates, and merges them in their original order (Caching supported).

    Args:
        queries: List of query strings
        content: Original content to be searched
        chunk_size: Maximum tokens per chunk
        top_k: Number of most relevant chunks to filter per query
        model_name: Name of model for tokenization
        method: Chunk selection method ("bm25", "openai", "sentence_transformer", "gemini")
        sentence_transformer_model: SentenceTransformer model name
        openai_model: OpenAI embedding model name
        gemini_model: Gemini embedding model name
        
    Returns:
        str: Selected chunks merged in their original order
    """
    # Split content into chunks
    chunks = split_text_by_tokens(content, max_tokens=chunk_size, model_name=model_name)

    if len(chunks) <= top_k * len(queries):
        # If the number of chunks is equal to or less than top_k, return entire content
        return content
    
    # Create selector
    if method == "bm25":
        selector = BM25ChunkSelector()
    elif method == "openai":
        selector = OpenAIEmbeddingChunkSelector(model=openai_model)
    elif method == "sentence_transformer":
        selector = SentenceTransformerChunkSelector(sentence_transformer_model or "all-MiniLM-L6-v2")
    elif method == "gemini":
        selector = GeminiChunkSelector(model=gemini_model)
    else:
        raise ValueError(f"Unknown method: {method}. Choose from: bm25, openai, sentence_transformer, gemini")
    
    return await selector.select(queries, chunks, top_k)


# Legacy BM25 function (kept for backward compatibility)
async def limit_tokens_by_chunk_bm25_only(queries: list[str], content, chunk_size=1000, top_k=2, model_name="cl100k_base"):
    """
    Selects top K chunks most relevant to each query based on BM25 score,
    removes duplicates, and merges them in their original order.

    Args:
        queries: List of query strings
        content: Original content to be searched
        chunk_size: Maximum tokens per chunk
        top_k: Number of most relevant chunks to filter per query
        model_name: Name of model for tokenization
        
    Returns:
        str: Selected chunks merged in their original order
    """
    # Split content into chunks
    chunks = split_text_by_tokens(content, max_tokens=chunk_size, model_name=model_name)

    if len(chunks) <= top_k * len(queries):
        # If the number of chunks is equal to or less than top_k, return entire content
        return content

    # Tokenize each chunk
    tokenized_chunks = [chunk.split() for chunk in chunks]
    
    # Create BM25 Index
    if BM25Okapi is None:
        raise ImportError("rank_bm25 module is not installed for BM25ChunkSelector.")
        
    bm25 = BM25Okapi(tokenized_chunks)
    
    # Collect all selected chunk indices across queries
    selected_indices = set()
    
    for query in queries:
        # Tokenize query and get scores
        tokenized_query = query.split()
        scores = bm25.get_scores(tokenized_query)
        
        # Select top K chunk indices
        top_k_indices = np.argsort(scores)[::-1][:top_k].tolist()
        selected_indices.update(top_k_indices)
    
    # Sort the selected indices in their original order
    sorted_indices = sorted(selected_indices)
    
    # Fetch corresponding chunks and merge
    selected_chunks = [chunks[i] for i in sorted_indices]
    
    return "\n\n...\n\n".join(selected_chunks)
