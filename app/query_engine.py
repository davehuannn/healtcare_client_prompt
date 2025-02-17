from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from functools import lru_cache
from fastapi import HTTPException
import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, max_requests: int, time_window: int):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = defaultdict(list)
    
    def is_allowed(self, user_id: str) -> bool:
        current_time = time.time()
        user_requests = self.requests[user_id]
        
        # Remove old requests
        user_requests = [req for req in user_requests 
                        if current_time - req < self.time_window]
        self.requests[user_id] = user_requests
        
        if len(user_requests) >= self.max_requests:
            return False
        
        self.requests[user_id].append(current_time)
        return True

class QueryEngine:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0)
        self.prompt_template = """You are a helpful assistant for healthcare system documentation. 
        Use the following pieces of context to answer the question at the end. 
        If you don't know the answer, just say that you don't know.

        Context: {context}

        Question: {question}

        Answer: """
        self.rate_limiter = RateLimiter(max_requests=10, time_window=60)
        self.cache = {}

    def get_answer(self, query: str) -> str:
        # Get relevant documents from ChromaDB
        results = self.collection.query(
            query_texts=[query],
            n_results=3
        )
        
        context = "\n".join(results['documents'][0])
        
        prompt = PromptTemplate(
            template=self.prompt_template,
            input_variables=["context", "question"]
        )
        
        chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.collection.as_retriever(),
            chain_type_kwargs={"prompt": prompt}
        )
        
        return chain.run(query)

    @lru_cache(maxsize=1000)
    def get_cached_answer(self, query: str) -> str:
        return self.get_answer(query)
    
    async def process_query(self, query: str, user_id: str) -> str:
        # Check rate limit
        if not self.rate_limiter.is_allowed(user_id):
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please try again later."
            )
        
        # Check cache first
        cache_key = f"{query}_{user_id}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Get new answer
        answer = await self.get_answer(query)
        
        # Cache the result
        self.cache[cache_key] = answer
        
        return answer 