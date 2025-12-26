"""
RAG (Retrieval Augmented Generation) Service using ChromaDB
Enables semantic search over agricultural knowledge base
"""
import os
from typing import List, Dict, Any, Optional
import json

import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document

from config.settings import settings


# ============================================================================
# CHROMA CLOUD CONFIGURATION
# ============================================================================

# Load from environment variables
CHROMA_API_KEY = os.getenv("CHROMA_API_KEY")
CHROMA_TENANT = os.getenv("CHROMA_TENANT")
# Note: Database name has trailing space in Chroma Cloud
CHROMA_DATABASE = os.getenv("CHROMA_DATABASE", "Project Samarth ")
# Ensure trailing space if not present (Chroma Cloud quirk)
if CHROMA_DATABASE and not CHROMA_DATABASE.endswith(" "):
    CHROMA_DATABASE = CHROMA_DATABASE + " "


# ============================================================================
# AGRICULTURAL KNOWLEDGE BASE
# ============================================================================

AGRICULTURAL_KNOWLEDGE = [
    # Data source descriptions
    {
        "content": "APEDA (Agricultural and Processed Food Products Export Development Authority) provides state-level export data for agricultural products from 2019 to 2024. Categories include Agri (cereals, grains), Fruits, Vegetables, Spices, LiveStock, Plantations, and Floriculture.",
        "metadata": {"source": "data_sources", "type": "apeda", "years": "2019-2024"}
    },
    {
        "content": "District-level crop production data covers years 2013 to 2015. This dataset includes production quantities, area cultivated, and yield for major crops across all Indian districts.",
        "metadata": {"source": "data_sources", "type": "crop_production", "years": "2013-2015"}
    },
    {
        "content": "Daily rainfall data is available at district level from 2019 to 2024. This includes daily precipitation measurements useful for recent weather pattern analysis.",
        "metadata": {"source": "data_sources", "type": "daily_rainfall", "years": "2019-2024"}
    },
    {
        "content": "Historical rainfall data spans from 1901 to 2015 at the state level. Includes monthly, seasonal, and annual rainfall totals. Ideal for long-term climate trend analysis.",
        "metadata": {"source": "data_sources", "type": "historical_rainfall", "years": "1901-2015"}
    },
    
    # Crop information
    {
        "content": "Rice is India's primary food grain crop, grown extensively in states like West Bengal, Uttar Pradesh, Punjab, and Tamil Nadu. Kharif crop requiring 100-200cm rainfall.",
        "metadata": {"source": "crop_info", "crop": "rice", "season": "kharif"}
    },
    {
        "content": "Wheat is the second most important food grain in India, primarily grown in Punjab, Haryana, Uttar Pradesh, and Madhya Pradesh. Rabi crop requiring cool climate.",
        "metadata": {"source": "crop_info", "crop": "wheat", "season": "rabi"}
    },
    {
        "content": "Cotton is a major cash crop grown in Maharashtra, Gujarat, Andhra Pradesh, and Punjab. Requires warm climate with moderate rainfall.",
        "metadata": {"source": "crop_info", "crop": "cotton", "season": "kharif"}
    },
    {
        "content": "Sugarcane is grown in Uttar Pradesh, Maharashtra, Karnataka, and Tamil Nadu. Requires hot and humid climate with good irrigation.",
        "metadata": {"source": "crop_info", "crop": "sugarcane", "season": "annual"}
    },
    {
        "content": "Pulses including lentils, chickpeas, and beans are protein-rich crops grown across Madhya Pradesh, Maharashtra, Rajasthan. Important for soil nitrogen fixation.",
        "metadata": {"source": "crop_info", "crop": "pulses", "season": "rabi"}
    },
    
    # Regional information
    {
        "content": "Punjab is known as the 'Granary of India' due to its high wheat and rice production. Uses extensive canal irrigation from rivers.",
        "metadata": {"source": "regional_info", "state": "Punjab", "specialty": "wheat, rice"}
    },
    {
        "content": "Maharashtra is the largest producer of sugarcane, grapes, and mangoes in India. Also significant cotton production.",
        "metadata": {"source": "regional_info", "state": "Maharashtra", "specialty": "sugarcane, fruits"}
    },
    {
        "content": "Kerala is famous for spices, coconut, and rubber plantations. Receives heavy monsoon rainfall.",
        "metadata": {"source": "regional_info", "state": "Kerala", "specialty": "spices, coconut"}
    },
    {
        "content": "Andhra Pradesh and Telangana are major producers of rice, chillies, and tobacco. Krishna and Godavari river deltas are highly fertile.",
        "metadata": {"source": "regional_info", "state": "Andhra Pradesh", "specialty": "rice, chillies"}
    },
    
    # System capabilities
    {
        "content": "Project Samarth uses a two-model architecture: QueryRouter for intelligent dataset selection and QueryProcessor for answer generation. Both use Google Gemini 2.5-flash.",
        "metadata": {"source": "system_info", "type": "architecture"}
    },
    {
        "content": "The system integrates 5 government data sources covering agricultural production and rainfall from 1901 to 2024, spanning over 120 years of historical data.",
        "metadata": {"source": "system_info", "type": "data_coverage"}
    },
    {
        "content": "MongoDB caching reduces response time from 13 seconds to 0.1 seconds (130x improvement) by storing query results with smart TTL-based expiration.",
        "metadata": {"source": "system_info", "type": "caching"}
    }
]


# ============================================================================
# RAG SERVICE CLASS
# ============================================================================

class RAGService:
    """
    RAG (Retrieval Augmented Generation) service for agricultural queries
    Uses ChromaDB for vector storage and Google Embeddings
    """
    
    def __init__(self, use_cloud: bool = True):
        """
        Initialize RAG service
        
        Args:
            use_cloud: If True, use Chroma Cloud. If False, use local persistence.
        """
        print("DEBUG: Initializing RAG Service...")
        
        self.use_cloud = use_cloud
        self.collection_name = "agricultural_knowledge"
        
        # Initialize embeddings using HuggingFace (FREE, no API limits!)
        # all-MiniLM-L6-v2 is a fast, efficient embedding model
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # Initialize LLM for generation
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0.7
        )
        
        # Initialize Chroma client
        if use_cloud:
            self._init_cloud_client()
        else:
            self._init_local_client()
        
        # Initialize vector store
        self._init_vector_store()
        
        print("DEBUG: RAG Service initialized successfully!")
    
    def _init_cloud_client(self):
        """Initialize Chroma Cloud client"""
        try:
            self.chroma_client = chromadb.CloudClient(
                api_key=CHROMA_API_KEY,
                tenant=CHROMA_TENANT,
                database=CHROMA_DATABASE
            )
            print("DEBUG: Connected to Chroma Cloud")
        except Exception as e:
            print(f"DEBUG: Chroma Cloud connection failed: {e}, falling back to local")
            self._init_local_client()
            self.use_cloud = False
    
    def _init_local_client(self):
        """Initialize local Chroma client with persistence"""
        persist_dir = os.path.join(os.path.dirname(__file__), "..", "..", "chroma_db")
        os.makedirs(persist_dir, exist_ok=True)
        
        self.chroma_client = chromadb.PersistentClient(path=persist_dir)
        print(f"DEBUG: Using local Chroma at {persist_dir}")
    
    def _init_vector_store(self):
        """Initialize or load the vector store"""
        try:
            # Try to get existing collection
            collection = self.chroma_client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description": "Agricultural knowledge base for Project Samarth"}
            )
            
            # Check if collection is empty
            count = collection.count()
            print(f"DEBUG: Collection '{self.collection_name}' has {count} documents")
            
            # Create LangChain Chroma wrapper
            self.vector_store = Chroma(
                client=self.chroma_client,
                collection_name=self.collection_name,
                embedding_function=self.embeddings
            )
            
            # Populate if empty
            if count == 0:
                print("DEBUG: Populating knowledge base...")
                self._populate_knowledge_base()
                
        except Exception as e:
            print(f"DEBUG: Vector store init error: {e}")
            raise
    
    def _populate_knowledge_base(self):
        """Populate the vector store with agricultural knowledge"""
        documents = []
        
        for item in AGRICULTURAL_KNOWLEDGE:
            doc = Document(
                page_content=item["content"],
                metadata=item["metadata"]
            )
            documents.append(doc)
        
        # Add documents to vector store
        self.vector_store.add_documents(documents)
        print(f"DEBUG: Added {len(documents)} documents to knowledge base")
    
    def search(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """
        Search the knowledge base for relevant documents
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of relevant documents with scores
        """
        try:
            results = self.vector_store.similarity_search_with_score(query, k=k)
            
            documents = []
            for doc, score in results:
                documents.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "relevance_score": 1 - score  # Convert distance to similarity
                })
            
            return documents
            
        except Exception as e:
            print(f"DEBUG: Search error: {e}")
            return []
    
    def query_with_rag(self, question: str) -> str:
        """
        Answer a question using RAG (Retrieval + Generation)
        
        Args:
            question: User's question
            
        Returns:
            Generated answer with retrieved context
        """
        # Retrieve relevant documents
        relevant_docs = self.search(question, k=3)
        
        if not relevant_docs:
            return "I couldn't find relevant information to answer your question."
        
        # Build context from retrieved documents
        context = "\n\n".join([
            f"[Source: {doc['metadata'].get('source', 'unknown')}]\n{doc['content']}"
            for doc in relevant_docs
        ])
        
        # Create RAG prompt
        rag_prompt = PromptTemplate(
            template="""Use the following context to answer the question. 
If the context doesn't contain relevant information, say so.

Context:
{context}

Question: {question}

Answer:""",
            input_variables=["context", "question"]
        )
        
        # Build and invoke chain
        chain = rag_prompt | self.llm | StrOutputParser()
        
        try:
            answer = chain.invoke({
                "context": context,
                "question": question
            })
            return answer
        except Exception as e:
            print(f"DEBUG: RAG generation error: {e}")
            return f"Error generating answer: {str(e)}"
    
    def add_document(self, content: str, metadata: Dict[str, Any] = None):
        """Add a new document to the knowledge base"""
        doc = Document(
            page_content=content,
            metadata=metadata or {}
        )
        self.vector_store.add_documents([doc])
        print(f"DEBUG: Added document to knowledge base")
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the knowledge base"""
        try:
            collection = self.chroma_client.get_collection(self.collection_name)
            return {
                "name": self.collection_name,
                "document_count": collection.count(),
                "using_cloud": self.use_cloud
            }
        except Exception as e:
            return {"error": str(e)}


# ============================================================================
# SINGLETON INSTANCE
# ============================================================================

_rag_service: Optional[RAGService] = None


def get_rag_service(use_cloud: bool = None) -> RAGService:
    """
    Get or create the RAG service singleton
    
    Args:
        use_cloud: If None, auto-detect (use cloud if credentials available)
                   If True, force cloud. If False, force local.
    """
    global _rag_service
    
    if _rag_service is None:
        # Auto-detect: use cloud if credentials are set (for Render deployment)
        if use_cloud is None:
            use_cloud = bool(CHROMA_API_KEY and CHROMA_TENANT)
            if use_cloud:
                print("DEBUG: Chroma Cloud credentials found, using cloud storage")
            else:
                print("DEBUG: No Chroma Cloud credentials, using local storage")
        
        _rag_service = RAGService(use_cloud=use_cloud)
    
    return _rag_service


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def rag_search(query: str, k: int = 3) -> List[Dict[str, Any]]:
    """Quick search function"""
    service = get_rag_service()
    return service.search(query, k)


def rag_answer(question: str) -> str:
    """Quick RAG answer function"""
    service = get_rag_service()
    return service.query_with_rag(question)
