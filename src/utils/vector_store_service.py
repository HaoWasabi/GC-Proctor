"""
Vector Store Service - Quản lý FAISS index và embedding generation
Sử dụng sentence-transformers để tạo embeddings và FAISS cho similarity search
"""
import json
import numpy as np
import os
from pathlib import Path
from typing import List, Tuple, Dict, Optional

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    print("⚠️  FAISS không khả dụng - sẽ dùng keyword matching fallback")

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    print("⚠️  sentence-transformers không khả dụng - sẽ dùng keyword matching fallback")

class VectorStoreService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Khởi tạo Vector Store Service
        
        Args:
            model_name: Tên embedding model từ sentence-transformers
                       - 'all-MiniLM-L6-v2': 33M, nhanh (khuyến nghị)
                       - 'all-mpnet-base-v2': 110M, chính xác hơn
        """
        self.model = None
        self.embedding_dim = None
        self.index = None
        self.metadata = []  # Lưu thông tin chunk liên kết
        self.vector_db_path = Path(__file__).parent.parent.parent / "tmp" / "vector_db"
        self.faiss_path = self.vector_db_path / "all_regulations.faiss"
        self.metadata_path = self.vector_db_path / "all_regulations.json"
        self.available = SENTENCE_TRANSFORMERS_AVAILABLE and FAISS_AVAILABLE
        
        # Lazy load model only if needed
        if self.available:
            try:
                self.model = SentenceTransformer(model_name)
                self.embedding_dim = self.model.get_sentence_embedding_dimension()
                print(f"✅ VectorStoreService initialized with model: {model_name}")
            except Exception as e:
                print(f"❌ Error loading SentenceTransformer model: {e}")
                self.available = False
        
    def encode_text(self, text: str) -> np.ndarray:
        """
        Tạo embedding cho một đoạn text
        
        Args:
            text: Đoạn text cần embedding
            
        Returns:
            Vector embedding (1D numpy array)
        """
        if not self.available or self.model is None:
            raise RuntimeError("VectorStoreService không khả dụng - sentence-transformers chưa cài")
            
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.astype(np.float32)
    
    def encode_batch(self, texts: List[str]) -> np.ndarray:
        """
        Tạo embeddings cho danh sách texts
        
        Args:
            texts: Danh sách texts
            
        Returns:
            Ma trận embeddings (N x D)
        """
        if not self.available or self.model is None:
            raise RuntimeError("VectorStoreService không khả dụng - sentence-transformers chưa cài")
            
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.astype(np.float32)
    
    def load_faiss_index(self) -> bool:
        """
        Load FAISS index từ file
        
        Returns:
            True nếu load thành công, False nếu file không tồn tại
        """
        if not self.available:
            print("⚠️  Vector Store không khả dụng (sentence-transformers hoặc faiss chưa cài)")
            return False
            
        if not self.faiss_path.exists():
            print(f"⚠️  FAISS index không tìm thấy tại: {self.faiss_path}")
            return False
            
        try:
            # Load FAISS index
            self.index = faiss.read_index(str(self.faiss_path))
            
            # Load metadata từ JSON
            with open(self.metadata_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.metadata = data.get('entries', [])
            
            print(f"✅ Đã load FAISS index ({len(self.metadata)} chunks)")
            return True
        except Exception as e:
            print(f"❌ Lỗi khi load FAISS: {e}")
            return False
    
    def search(self, query: str, k: int = 5) -> List[Tuple[str, float]]:
        """
        Tìm kiếm k chunks tương tự nhất với query
        
        Args:
            query: Câu hỏi cần tìm kiếm
            k: Số lượng kết quả trả về
            
        Returns:
            Danh sách tuples (chunk_text, similarity_score)
        """
        if not self.available:
            print("⚠️  Vector Store không khả dụng")
            return []
            
        if self.index is None:
            print("❌ FAISS index chưa được load")
            return []
        
        if len(self.metadata) == 0:
            print("❌ Metadata rỗng")
            return []
        
        try:
            # Encode query
            query_embedding = self.encode_text(query)
            query_embedding = np.array([query_embedding])  # (1, D)
            
            # Tìm k nearest neighbors
            distances, indices = self.index.search(query_embedding, k)
            
            results = []
            for idx, distance in zip(indices[0], distances[0]):
                if 0 <= idx < len(self.metadata):
                    chunk = self.metadata[idx]
                    # Normalize distance (FAISS trả về L2 distance)
                    # Chuyển đổi thành similarity score: 1 / (1 + distance)
                    similarity = 1.0 / (1.0 + distance)
                    text = chunk.get('text', '')
                    results.append((text, float(similarity)))
            
            return results
        except Exception as e:
            print(f"❌ Lỗi khi search: {e}")
            return []
    
    def search_with_citations(self, query: str, k: int = 5) -> List[Dict]:
        """
        Tìm kiếm kèm thông tin citation
        
        Args:
            query: Câu hỏi cần tìm kiếm
            k: Số lượng kết quả trả về
            
        Returns:
            Danh sách dicts chứa {text, similarity, citation}
        """
        if not self.available:
            print("⚠️  Vector Store không khả dụng")
            return []
            
        if self.index is None:
            print("❌ FAISS index chưa được load")
            return []
        
        try:
            # Encode query
            query_embedding = self.encode_text(query)
            query_embedding = np.array([query_embedding])  # (1, D)
            
            # Tìm k nearest neighbors
            distances, indices = self.index.search(query_embedding, k)
            
            results = []
            for idx, distance in zip(indices[0], distances[0]):
                if 0 <= idx < len(self.metadata):
                    chunk = self.metadata[idx]
                    similarity = 1.0 / (1.0 + distance)
                    
                    result = {
                        'text': chunk.get('text', ''),
                        'similarity': float(similarity),
                        'citation': chunk.get('citation', {})
                    }
                    results.append(result)
            
            return results
        except Exception as e:
            print(f"❌ Lỗi khi search: {e}")
            return []
    
    def create_index_from_chunks(self, chunks_data: List[Dict]):
        """
        Tạo FAISS index từ danh sách chunks
        
        Args:
            chunks_data: Danh sách dicts với field 'text' và 'citation'
        """
        if not self.available:
            print("❌ VectorStoreService không khả dụng - không thể tạo index")
            return False
            
        if not chunks_data:
            print("❌ Không có chunks để tạo index")
            return False
        
        try:
            # Extract texts
            texts = [chunk.get('text', '') for chunk in chunks_data]
            
            # Generate embeddings
            print(f"Đang tạo embeddings cho {len(texts)} chunks...")
            embeddings = self.encode_batch(texts)
            
            # Create FAISS index
            self.index = faiss.IndexFlatL2(self.embedding_dim)
            self.index.add(embeddings)
            
            # Save index and metadata
            self.vector_db_path.mkdir(parents=True, exist_ok=True)
            faiss.write_index(self.index, str(self.faiss_path))
            
            # Save metadata
            metadata_to_save = {
                'fingerprint': 'manual_build',
                'entries': chunks_data
            }
            with open(self.metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata_to_save, f, ensure_ascii=False, indent=2)
            
            self.metadata = chunks_data
            print(f"✅ Đã tạo FAISS index với {len(texts)} chunks")
            return True
        except Exception as e:
            print(f"❌ Lỗi khi tạo index: {e}")
            return False
