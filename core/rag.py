"""
RAG pipeline: retrieval, prompt generation, and answer generation.
"""
from typing import List, Optional, Tuple
from langchain.schema import Document
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

from core.config import Config
from core.vectorstore import VectorStore
from core.models import create_chat_model
from core.citations import create_sources_section
from core.logging_utils import get_logger

logger = get_logger(__name__)


# RAG prompt template
RAG_PROMPT_TEMPLATE = """You are a helpful assistant that answers questions based on the provided context from documents.

Context from documents:
{context}

Question: {question}

Instructions:
- Answer the question using ONLY the information from the context above.
- If the context does not contain enough information to answer the question, say "I cannot find that information in the provided documents" and suggest how the user might rephrase their question.
- Be concise and accurate.
- Do not make up information that is not in the context.

Answer:"""


class RAGPipeline:
    """Retrieval-augmented generation pipeline."""
    
    def __init__(
        self,
        config: Config,
        vector_store: VectorStore,
        provider: Optional[str] = None
    ):
        """
        Initialize RAG pipeline.
        
        Args:
            config: Application configuration
            vector_store: Vector store instance
            provider: Model provider (optional, uses config default)
        """
        self.config = config
        self.vector_store = vector_store
        self.provider = provider or config.model_provider
        
        # Create chat model
        self.chat_model = create_chat_model(config, self.provider)
        
        # Create prompt template
        self.prompt = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)
    
    def retrieve_documents(
        self,
        query: str,
        top_k: Optional[int] = None
    ) -> List[Document]:
        """
        Retrieve relevant documents for a query.
        
        Args:
            query: User query
            top_k: Number of documents to retrieve
            
        Returns:
            List of relevant documents
        """
        top_k = top_k or self.config.top_k
        
        try:
            documents = self.vector_store.similarity_search(query, k=top_k)
            logger.info(f"Retrieved {len(documents)} documents for query")
            return documents
        
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}")
            return []
    
    def _format_context(self, documents: List[Document]) -> str:
        """
        Format retrieved documents into context string.
        
        Args:
            documents: List of documents
            
        Returns:
            Formatted context string
        """
        if not documents:
            return "No relevant documents found."
        
        context_parts = []
        for i, doc in enumerate(documents, 1):
            metadata = doc.metadata
            filename = metadata.get('filename', 'Unknown')
            page = metadata.get('page')
            
            source_info = f"[Source: {filename}"
            if page is not None:
                source_info += f", Page {page}"
            source_info += "]"
            
            context_parts.append(f"{source_info}\n{doc.page_content}\n")
        
        return "\n---\n".join(context_parts)
    
    def generate_answer(
        self,
        query: str,
        documents: List[Document]
    ) -> str:
        """
        Generate answer using retrieved documents.
        
        Args:
            query: User query
            documents: Retrieved documents
            
        Returns:
            Generated answer
        """
        try:
            # Format context
            context = self._format_context(documents)
            
            # Create the chain
            chain = (
                {
                    "context": lambda x: context,
                    "question": RunnablePassthrough()
                }
                | self.prompt
                | self.chat_model
                | StrOutputParser()
            )
            
            # Generate answer
            logger.info("Generating answer with LLM")
            answer = chain.invoke(query)
            
            return answer.strip()
        
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            return f"Error generating answer: {str(e)}"
    
    def query(
        self,
        question: str,
        top_k: Optional[int] = None,
        include_citations: bool = True
    ) -> Tuple[str, List[Document]]:
        """
        Complete RAG query: retrieve, generate, and optionally add citations.
        
        Args:
            question: User question
            top_k: Number of documents to retrieve
            include_citations: Whether to include citations in the response
            
        Returns:
            Tuple of (answer, retrieved_documents)
        """
        # Check if vector store has documents
        doc_count = self.vector_store.get_document_count()
        if doc_count == 0:
            return (
                "No documents have been indexed yet. Please upload and index some documents first.",
                []
            )
        
        # Retrieve relevant documents
        documents = self.retrieve_documents(question, top_k)
        
        if not documents:
            return (
                "I couldn't find any relevant information in the indexed documents. "
                "Please try rephrasing your question or upload more relevant documents.",
                []
            )
        
        # Generate answer
        answer = self.generate_answer(question, documents)
        
        # Add citations if requested
        if include_citations:
            citations_section = create_sources_section(documents)
            answer = answer + citations_section
        
        return answer, documents
