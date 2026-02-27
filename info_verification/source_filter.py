from typing import List, Literal, Optional
from abc import ABC, abstractmethod
import hashlib
import pickle
import os
from pathlib import Path

# BM25 관련 임포트
try:
    from rank_bm25 import BM25Okapi
except ImportError:
    BM25Okapi = None

import litellm
# OpenAI 임베딩
import openai
import tiktoken
import numpy as np
import asyncio


class EmbeddingCache:
    """임베딩 결과를 캐시하는 클래스"""
    
    def __init__(self, cache_dir: str = "embedding_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
    
    def _get_cache_key(self, text: str, model: str) -> str:
        """텍스트와 모델명으로 캐시 키 생성"""
        content = f"{model}:{text}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def get(self, text: str, model: str) -> Optional[List[float]]:
        """캐시에서 임베딩 가져오기"""
        cache_key = self._get_cache_key(text, model)
        cache_file = self.cache_dir / f"{cache_key}.pkl"
        
        if cache_file.exists():
            try:
                with open(cache_file, 'rb') as f:
                    return pickle.load(f)
            except Exception:
                # 캐시 파일이 손상된 경우 무시
                pass
        return None
    
    def set(self, text: str, model: str, embedding: List[float]):
        """캐시에 임베딩 저장"""
        cache_key = self._get_cache_key(text, model)
        cache_file = self.cache_dir / f"{cache_key}.pkl"
        
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(embedding, f)
        except Exception:
            # 캐시 저장 실패는 무시
            pass


# 전역 캐시 인스턴스
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
        
        # 각 쿼리별로 top-k 청크 선택
        for query in queries:
            scores = bm25.get_scores(query.split())
            # 점수가 높은 순으로 인덱스 정렬
            ranked_indices = np.argsort(scores)[::-1]
            # 상위 k개 선택
            for i in range(min(top_k, len(ranked_indices))):
                selected_indices.add(ranked_indices[i])
        
        # 원래 순서대로 정렬하여 청크 합치기
        selected_indices = sorted(selected_indices)
        selected_chunks = [chunks[i] for i in selected_indices]
        # return '\n\n'.join(selected_chunks)
        return "\n\n...\n\n".join(selected_chunks)

class OpenAIEmbeddingChunkSelector(ChunkSelector):
    def __init__(self, model: str = "text-embedding-3-large"):
        # openai.api_key = openai_api_key
        self.model = model

    async def get_embedding(self, text: str) -> List[float]:
        # 캐시에서 먼저 확인
        cached_embedding = _embedding_cache.get(text, self.model)
        if cached_embedding is not None:
            return cached_embedding
        
        # 캐시에 없으면 API 호출
        try:
            response = await litellm.aembedding(self.model, input=[text])
            embedding = response['data'][0]['embedding']
            
            # 캐시에 저장
            _embedding_cache.set(text, self.model, embedding)
            return embedding
        except Exception as e:
            print(f"Error getting OpenAI embedding: {e}")
            return [0.0] * 1536  # 기본 차원

    def cosine_similarity(self, a, b):
        a = np.array(a)
        b = np.array(b)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    async def select(self, queries: List[str], chunks: List[str], top_k: int) -> str:
        selected_indices = set()
        
        # 청크 임베딩 미리 계산
        chunk_embs = await asyncio.gather(*(self.get_embedding(chunk) for chunk in chunks))

        # 각 쿼리별로 top-k 청크 선택
        for query in queries:
            query_emb = await self.get_embedding(query)
            scores = [self.cosine_similarity(query_emb, emb) for emb in chunk_embs]
            # 점수가 높은 순으로 인덱스 정렬
            ranked_indices = np.argsort(scores)[::-1]
            # 상위 k개 선택
            for i in range(min(top_k, len(ranked_indices))):
                selected_indices.add(ranked_indices[i])
        
        # 원래 순서대로 정렬하여 청크 합치기
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
        """배치로 임베딩 가져오기 (캐싱 포함)"""
        from google.genai import types

        embeddings = []
        texts_to_embed = []
        cache_indices = []
        
        # 캐시 키에 task_type도 포함
        cache_model_key = f"{self.model}_{task_type}"
        
        # 캐시에서 먼저 확인
        for i, text in enumerate(texts):
            cached_embedding = _embedding_cache.get(text, cache_model_key)
            if cached_embedding is not None:
                embeddings.append(cached_embedding)
            else:
                embeddings.append(None)  # 자리 표시자
                texts_to_embed.append(text)
                cache_indices.append(i)
        
        # 캐시되지 않은 텍스트들을 배치로 임베딩
        if texts_to_embed:
            try:
                result = self.client.models.embed_content(
                    model=self.model,
                    contents=texts_to_embed,
                    config=types.EmbedContentConfig(task_type=task_type)
                )
                
                batch_embeddings = [np.array(e.values).tolist() for e in result.embeddings]
                
                # 결과를 원래 위치에 배치하고 캐시에 저장
                for i, embedding in enumerate(batch_embeddings):
                    original_index = cache_indices[i]
                    embeddings[original_index] = embedding
                    _embedding_cache.set(texts_to_embed[i], cache_model_key, embedding)
                    
            except Exception as e:
                print(f"Error getting Gemini embeddings: {e}")
                # 실패한 경우 더미 임베딩 반환
                for i in cache_indices:
                    embeddings[i] = [0.0] * 768  # 기본 차원
        
        return embeddings
    
    async def select(self, queries: List[str], chunks: List[str], top_k: int) -> str:
        selected_indices = set()
        print("let's go gemini")
        
        # 쿼리와 청크를 각각 다른 task_type으로 임베딩
        query_embeddings = await self.get_embeddings_batch(queries, task_type="FACT_VERIFICATION")
        chunk_embeddings = await self.get_embeddings_batch(chunks, task_type="RETRIEVAL_DOCUMENT")
        
        # 각 쿼리별로 top-k 청크 선택
        for query_emb in query_embeddings:
            scores = [self.cosine_similarity(query_emb, chunk_emb) for chunk_emb in chunk_embeddings]
            # 점수가 높은 순으로 인덱스 정렬
            ranked_indices = np.argsort(scores)[::-1]
            # 상위 k개 선택
            for i in range(min(top_k, len(ranked_indices))):
                selected_indices.add(ranked_indices[i])
        
        # 원래 순서대로 정렬하여 청크 합치기
        selected_indices = sorted(selected_indices)
        selected_chunks = [chunks[i] for i in selected_indices]
        return '\n\n'.join(selected_chunks)

class SentenceTransformerChunkSelector(ChunkSelector):
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(model_name)

    async def select(self, queries: List[str], chunks: List[str], top_k: int) -> str:
        selected_indices = set()
        
        # 청크 임베딩 미리 계산
        chunk_embs = self.model.encode(chunks)
        
        # 각 쿼리별로 top-k 청크 선택
        for query in queries:
            query_emb = self.model.encode([query])[0]
            scores = [np.dot(query_emb, emb) / (np.linalg.norm(query_emb) * np.linalg.norm(emb)) for emb in chunk_embs]
            # 점수가 높은 순으로 인덱스 정렬
            ranked_indices = np.argsort(scores)[::-1]
            # 상위 k개 선택
            for i in range(min(top_k, len(ranked_indices))):
                selected_indices.add(ranked_indices[i])
        
        # 원래 순서대로 정렬하여 청크 합치기
        selected_indices = sorted(selected_indices)
        selected_chunks = [chunks[i] for i in selected_indices]
        return '\n\n'.join(selected_chunks)

def split_text_by_tokens(text, model_name="cl100k_base", max_tokens=4000):
    """
    텍스트를 토큰 단위로 분할하는 함수
    """
    # 모델에 맞는 인코더 가져오기
    encoding = tiktoken.get_encoding(model_name)
    
    # 텍스트를 토큰으로 변환
    #jh
    cleaned_text = text.replace('<|endoftext|>', '').replace('<|endofprompt|>', '')

    tokens = encoding.encode(cleaned_text)
    
    # 토큰을 max_tokens 크기로 분할
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
    선택한 방법을 사용해 queries와 가장 관련성이 높은 상위 K개 chunk들을 각 쿼리별로 가져온 후
    중복을 제거하고 원래 순서대로 합쳐서 반환 (캐싱 지원)

    Args:
        queries: 쿼리 문자열 리스트
        content: 검색할 전체 컨텐츠
        chunk_size: 각 청크의 최대 토큰 수
        top_k: 각 쿼리당 가져올 상위 청크 개수
        model_name: 토큰화에 사용할 모델명
        method: 청크 선택 방법 ("bm25", "openai", "sentence_transformer", "gemini")
        sentence_transformer_model: SentenceTransformer 모델명
        openai_model: OpenAI 임베딩 모델명
        gemini_model: Gemini 임베딩 모델명
        
    Returns:
        str: 선택된 청크들을 원래 순서대로 합친 텍스트
    """
    # content를 chunk로 분할
    chunks = split_text_by_tokens(content, max_tokens=chunk_size, model_name=model_name)

    if len(chunks) <= top_k * len(queries):
        # 만약 chunk의 개수가 top_k보다 작거나 같다면, 전체 content를 반환
        return content
    
    # 선택기 생성
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


# 기존 BM25 전용 함수 (호환성을 위해 유지)
async def limit_tokens_by_chunk_bm25_only(queries: list[str], content, chunk_size=1000, top_k=2, model_name="cl100k_base"):
    """
    BM25 점수를 기반으로 queries와 가장 관련성이 높은 상위 K개 chunk들을 각 쿼리별로 가져온 후
    중복을 제거하고 원래 순서대로 합쳐서 반환

    Args:
        queries: 쿼리 문자열 리스트
        content: 검색할 전체 컨텐츠
        chunk_size: 각 청크의 최대 토큰 수
        top_k: 각 쿼리당 가져올 상위 청크 개수
        model_name: 토큰화에 사용할 모델명
        
    Returns:
        str: 선택된 청크들을 원래 순서대로 합친 텍스트
    """
    # content를 chunk로 분할
    chunks = split_text_by_tokens(content, max_tokens=chunk_size, model_name=model_name)

    if len(chunks) <= top_k * len(queries):
        # 만약 chunk의 개수가 top_k보다 작거나 같다면, 전체 content를 반환
        return content

    # 각 chunk를 토큰화
    tokenized_chunks = [chunk.split() for chunk in chunks]
    
    # BM25 인덱스 생성
    if BM25Okapi is None:
        raise ImportError("rank_bm25 module is not installed for BM25ChunkSelector.")
        
    bm25 = BM25Okapi(tokenized_chunks)
    
    # 모든 쿼리에서 선택된 청크 인덱스들을 수집
    selected_indices = set()
    
    for query in queries:
        # query 토큰화 및 점수 계산
        tokenized_query = query.split()
        scores = bm25.get_scores(tokenized_query)
        
        # 상위 K개 chunk 인덱스 선택
        top_k_indices = np.argsort(scores)[::-1][:top_k].tolist()
        selected_indices.update(top_k_indices)
    
    # 선택된 인덱스들을 원래 순서대로 정렬
    sorted_indices = sorted(selected_indices)
    
    # 해당 chunk들을 원래 순서대로 가져와서 연결
    selected_chunks = [chunks[i] for i in sorted_indices]
    
    return "\n\n...\n\n".join(selected_chunks)
