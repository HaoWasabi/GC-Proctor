"""
Debug script - Kiểm tra tại sao regulation search không hoạt động
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

def debug_vector_store():
    print("\n" + "="*80)
    print("DEBUG: Vector Store Status")
    print("="*80 + "\n")
    
    from utils.vector_store_service import VectorStoreService
    
    vs = VectorStoreService()
    print(f"[1] VectorStoreService available: {vs.available}")
    print(f"[2] Model initialized: {vs.model is not None}")
    print(f"[3] FAISS path exists: {vs.faiss_path.exists()}")
    print(f"[4] Metadata path exists: {vs.metadata_path.exists()}")
    
    if vs.faiss_path.exists():
        faiss_size = vs.faiss_path.stat().st_size / (1024*1024)  # MB
        print(f"[5] FAISS file size: {faiss_size:.2f} MB")
    
    # Try to load index
    print(f"\n[6] Attempting to load FAISS index...")
    loaded = vs.load_faiss_index()
    print(f"    Loaded: {loaded}")
    print(f"    Index: {vs.index}")
    print(f"    Metadata entries: {len(vs.metadata)}")
    
    if loaded:
        print(f"\n[7] Testing search...")
        results = vs.search("Sinh vien di tre", k=2)
        print(f"    Results count: {len(results)}")
        for i, (text, score) in enumerate(results, 1):
            print(f"    [{i}] Score: {score:.3f} - {text[:60]}...")


def debug_regulation_service():
    print("\n" + "="*80)
    print("DEBUG: Regulation Service")
    print("="*80 + "\n")
    
    from services.regulation_service import RegulationService
    
    rs = RegulationService()
    print(f"[1] Regulation Service ready")
    print(f"[2] Vector store ready: {rs.vector_store_ready}")
    print(f"[3] Vector store available: {rs.vector_store.available}")
    
    # Test retrieve
    query = "Sinh vien di tre bao lau"
    print(f"\n[4] Testing _retrieve_relevant_chunks()")
    print(f"    Query: '{query}'")
    
    context = rs._retrieve_relevant_chunks(query)
    print(f"    Context length: {len(context)}")
    print(f"    Context: {context[:200] if context else '(empty)'}")
    
    # Test answer
    print(f"\n[5] Testing answer_regulation_question()")
    answer = rs.answer_regulation_question(query)
    print(f"    Answer: {answer[:200]}...")


def debug_firestore():
    print("\n" + "="*80)
    print("DEBUG: Firestore Data")
    print("="*80 + "\n")
    
    try:
        from repositories.document_chunk_repository import DocumentChunkRepository
        
        repo = DocumentChunkRepository()
        chunks = repo.get_all_document_chunks()
        print(f"[1] Document chunks in Firestore: {len(chunks)}")
        
        if chunks:
            for i, chunk in enumerate(chunks[:3], 1):
                print(f"    [{i}] {chunk.get_content()[:80]}...")
        else:
            print("    ⚠️  No chunks in Firestore!")
            
    except Exception as e:
        print(f"❌ Error connecting to Firestore: {e}")


if __name__ == "__main__":
    try:
        print("\n🔍 REGULATION SEARCH DEBUG\n")
        
        debug_vector_store()
        debug_regulation_service()
        debug_firestore()
        
        print("\n" + "="*80)
        print("✅ Debug completed")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
