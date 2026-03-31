"""
Rebuild FAISS index from JSON metadata
"""
import sys
from pathlib import Path
import json
import numpy as np

sys.path.insert(0, "src")

def rebuild_faiss_from_json():
    print("\n" + "="*80)
    print("Rebuilding FAISS Index from JSON")
    print("="*80 + "\n")
    
    # Load metadata from JSON
    json_path = Path("tmp/vector_db/all_regulations.json")
    print(f"[1] Loading metadata from {json_path}")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    entries = data.get('entries', [])
    print(f"✅ Found {len(entries)} entries")
    
    for i, entry in enumerate(entries, 1):
        print(f"   [{i}] {entry['text'][:60]}...")
    
    # Prepare chunks_data format
    chunks_data = [
        {
            'id': entry['id'],
            'text': entry['text'],
            'citation': entry.get('citation', {})
        }
        for entry in entries
    ]
    
    # Rebuild using VectorStoreService
    print(f"\n[2] Rebuilding FAISS index...")
    from utils.vector_store_service import VectorStoreService
    
    vs = VectorStoreService()
    success = vs.create_index_from_chunks(chunks_data)
    
    if success:
        print(f"\n[3] Verifying new index...")
        vs_verify = VectorStoreService()
        loaded = vs_verify.load_faiss_index()
        print(f"✅ Index loaded: {loaded}")
        print(f"✅ Entries: {len(vs_verify.metadata)}")
        
        # Test search
        test_queries = [
            "Mang dien thoại vào phòng thi",
            "Đi trễ",
            "Sinh viên",
        ]
        
        print(f"\n[4] Testing search...")
        for query in test_queries:
            results = vs_verify.search(query, k=2)
            print(f"\n   Query: '{query}'")
            for text, score in results:
                print(f"   - Score {score:.3f}: {text[:70]}")
        
        print("\n" + "="*80)
        print("✅ FAISS index rebuilt successfully!")
        print("="*80 + "\n")
        return True
    else:
        print("❌ Failed to rebuild index")
        return False

if __name__ == "__main__":
    try:
        rebuild_faiss_from_json()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
