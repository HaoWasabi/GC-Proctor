"""
Quick Start - Vector Search Demo
Chạy script này để thấy vector search hoạt động

Usage: python vector_search_demo.py
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def demo():
    print("\n" + "="*80)
    print("🚀 VECTOR SEARCH DEMO")
    print("="*80)
    
    # Import after adding to path
    from utils.vector_store_service import VectorStoreService
    from services.regulation_service import RegulationService
    
    # Initialize
    print("\n[1] Initializing Vector Store...")
    vs = VectorStoreService()
    loaded = vs.load_faiss_index()
    
    if not loaded:
        print("❌ FAISS index not found!")
        print("📝 Next step: Run 'python src/utils/index_builder.py' to rebuild from Firestore")
        return
    
    print(f"✅ Vector Store loaded ({len(vs.metadata)} chunks)")
    
    # Demo queries
    print("\n" + "-"*80)
    print("[2] Vector Search Demo - Similarity Search")
    print("-"*80)
    
    demo_queries = [
        "Sinh viên đi trễ bao lâu không được vào thi?",
        "Điện thoại trong phòng thi",
        "Giờ sinh viên phải đến phòng thi",
    ]
    
    for query in demo_queries:
        print(f"\n❓ Query: {query}")
        print("   Results:")
        
        results = vs.search_with_citations(query, k=3)
        
        if not results:
            print("   ❌ No results")
            continue
        
        for i, result in enumerate(results, 1):
            text = result['text']
            score = result['similarity']
            print(f"\n   [{i}] Similarity: {score:.2f}")
            print(f"       {text[:100]}...")
    
    # Test RAG
    print("\n" + "-"*80)
    print("[3] RAG Demo - Regulation Service")
    print("-"*80)
    
    rs = RegulationService()
    print(f"✅ Regulation Service initialized")
    print(f"   Vector Store Ready: {rs.vector_store_ready}")
    
    test_question = "Nếu đi trễ 20 phút có được vào thi không?"
    print(f"\n❓ Question: {test_question}")
    
    context = rs._retrieve_relevant_chunks(test_question)
    if context:
        print("✅ Relevant chunks found:")
        print(f"   {context[:200]}...\n")
    else:
        print("❌ No relevant chunks found\n")
    
    print("="*80)
    print("✅ Demo completed!")
    print("="*80 + "\n")
    
    print("📚 Next: Read VECTOR_SEARCH_GUIDE.md for configuration and troubleshooting\n")


if __name__ == "__main__":
    try:
        demo()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
