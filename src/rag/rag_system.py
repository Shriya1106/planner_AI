"""RAG system for knowledge retrieval and generation."""

from typing import Dict, List, Optional
import logging
from .knowledge_base import KnowledgeBase

logger = logging.getLogger(__name__)


class RAGSystem:
    """Retrieval-Augmented Generation system for event planning knowledge."""
    
    def __init__(self, knowledge_base: KnowledgeBase = None):
        """Initialize RAG system.
        
        Args:
            knowledge_base: Knowledge base instance
        """
        self.knowledge_base = knowledge_base or KnowledgeBase()
        self.embeddings = None
        self.vector_store = None
    
    async def query(self, query: str, event_type: str = None, top_k: int = 3) -> Dict:
        """Query the RAG system.
        
        Args:
            query: User query
            event_type: Event type for filtering (optional)
            top_k: Number of results to return
            
        Returns:
            Answer with sources and confidence
        """
        logger.info(f"RAG query: {query}")
        
        # Retrieve relevant documents
        relevant_docs = self._retrieve_documents(query, event_type, top_k)
        
        # Generate answer from retrieved documents
        answer = self._generate_answer(query, relevant_docs)
        
        # Prepare sources
        sources = [
            {
                "title": doc["title"],
                "category": doc.get("category", "general"),
                "relevance": "high"
            }
            for doc in relevant_docs
        ]
        
        return {
            "answer": answer,
            "sources": sources,
            "confidence": 0.85 if relevant_docs else 0.3
        }
    
    def _retrieve_documents(
        self,
        query: str,
        event_type: Optional[str],
        top_k: int
    ) -> List[Dict]:
        """Retrieve relevant documents.
        
        Args:
            query: Search query
            event_type: Event type filter
            top_k: Number of documents to retrieve
            
        Returns:
            List of relevant documents
        """
        # Get documents filtered by event type
        if event_type:
            candidates = self.knowledge_base.get_documents(category=event_type)
            # Also include general documents
            candidates.extend(self.knowledge_base.get_documents(category="general"))
        else:
            candidates = self.knowledge_base.get_documents()
        
        # Simple keyword-based retrieval (in production, use embeddings)
        query_lower = query.lower()
        scored_docs = []
        
        for doc in candidates:
            score = 0
            content_lower = doc["content"].lower()
            title_lower = doc["title"].lower()
            
            # Score based on keyword matches
            query_words = query_lower.split()
            for word in query_words:
                if len(word) > 3:  # Skip short words
                    if word in title_lower:
                        score += 3
                    if word in content_lower:
                        score += 1
            
            # Boost score for matching tags
            for tag in doc.get("tags", []):
                if tag in query_lower:
                    score += 2
            
            if score > 0:
                scored_docs.append((score, doc))
        
        # Sort by score and return top_k
        scored_docs.sort(reverse=True, key=lambda x: x[0])
        return [doc for score, doc in scored_docs[:top_k]]
    
    def _generate_answer(self, query: str, documents: List[Dict]) -> str:
        """Generate answer from retrieved documents.
        
        Args:
            query: User query
            documents: Retrieved documents
            
        Returns:
            Generated answer
        """
        if not documents:
            return (
                "I don't have specific information about that in my knowledge base. "
                "However, I recommend consulting with professional event planners or "
                "researching online resources for detailed guidance."
            )
        
        # Extract relevant content from documents
        context_parts = []
        for doc in documents:
            context_parts.append(f"From '{doc['title']}':\n{doc['content'][:500]}")
        
        # In production, this would use an LLM to generate a coherent answer
        # For now, return a summary of the most relevant document
        top_doc = documents[0]
        
        # Extract the most relevant paragraph
        paragraphs = top_doc["content"].strip().split("\n\n")
        relevant_para = paragraphs[0] if paragraphs else top_doc["content"][:300]
        
        answer = f"{relevant_para}\n\nFor more details, refer to: {top_doc['title']}"
        
        return answer
    
    def add_knowledge(self, document: Dict):
        """Add new knowledge to the system.
        
        Args:
            document: Document to add
        """
        self.knowledge_base.add_document(document)
        logger.info(f"Added knowledge: {document.get('title', 'Untitled')}")
