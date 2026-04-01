"""
Index Builder - Rebuild FAISS index từ Firestore document chunks
Chạy khi: 
  - Chunks trong Firestore thay đổi
  - Cần tạo lại index nguồn
  
Sử dụng: python src/utils/index_builder.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from repositories.document_chunk_repository import DocumentChunkRepository
from utils.vector_store_service import VectorStoreService


def rebuild_faiss_from_firestore():
    """
    Rebuild FAISS index từ document chunks trong Firestore
    """
    print("\n" + "="*80)
    print("REBUILDING FAISS INDEX FROM FIRESTORE")
    print("="*80)
    
    try:
        # Lấy chunks quy chế từ Firestore (ownerType=regulation)
        print("\n[1] Lấy regulation chunks từ Firestore...")
        chunk_repo = DocumentChunkRepository()
        chunks = chunk_repo.get_document_chunks_by_owner_type("regulation")
        
        if not chunks:
            print("❌ Không tìm thấy regulation chunks trong Firestore")
            return False
        
        print(f"✅ Tìm thấy {len(chunks)} chunks")
        
        # Chuẩn bị dữ liệu cho index
        print("\n[2] Chuẩn bị dữ liệu...")
        chunks_data = []
        for i, chunk in enumerate(chunks, 1):
            chunk_dict = {
                'id': chunk.get_id(),
                'text': chunk.get_content(),
                'citation': {
                    'chunkId': chunk.get_id(),
                    'documentId': chunk.get_documentId(),
                    'chunkIndex': chunk.get_chunkIndex(),
                    'quote': chunk.get_content()[:100]  # First 100 chars as quote
                }
            }
            chunks_data.append(chunk_dict)
            
            if i % 10 == 0:
                print(f"   Processed {i}/{len(chunks)} chunks...")
        
        # Tạo FAISS index
        print("\n[3] Tạo FAISS index...")
        vs = VectorStoreService()
        success = vs.create_index_from_chunks(chunks_data)
        
        if success:
            print("\n" + "="*80)
            print("✅ FAISS index rebuilt successfully!")
            print("="*80 + "\n")
            return True
        else:
            print("\n❌ Failed to rebuild FAISS index")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    rebuild_faiss_from_firestore()
