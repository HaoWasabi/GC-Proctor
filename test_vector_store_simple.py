"""Quick test - Check if FAISS can be loaded"""
import sys
from pathlib import Path

sys.path.insert(0, "src")

print("Step 1: Testing imports...")
try:
    import faiss
    print("✅ FAISS imported")
except:
    print("❌ FAISS import failed")

try:
    from sentence_transformers import SentenceTransformer
    print("✅ SentenceTransformer imported")
except:
    print("❌ SentenceTransformer import failed")

print("\nStep 2: Testing VectorStoreService...")
try:
    from utils.vector_store_service import VectorStoreService
    print("✅ VectorStoreService imported")
    
    vs = VectorStoreService()
    print(f"✅ VectorStoreService created")
    print(f"   - available: {vs.available}")
    print(f"   - faiss_path: {vs.faiss_path}")
    print(f"   - exists: {vs.faiss_path.exists()}")
    
    if vs.available:
        print("\nStep 3: Loading FAISS index...")
        loaded = vs.load_faiss_index()
        print(f"✅ Load result: {loaded}")
        print(f"   - index: {vs.index is not None}")
        print(f"   - metadata entries: {len(vs.metadata)}")
        
        if loaded and vs.index:
            print("\nStep 4: Testing search...")
            results = vs.search("Mang dien thoai")
            print(f"✅ Search results: {len(results)}")
            for text, score in results:
                print(f"   Score {score:.3f}: {text[:60]}")
    else:
        print("⚠️  VectorStoreService not available")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
