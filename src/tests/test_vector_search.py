"""
Test Vector Search - Kiểm tra FAISS index và similarity search
Chạy: python src/tests/test_vector_search.py
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_vector_store_service():
    """Test VectorStoreService"""
    from utils.vector_store_service import VectorStoreService
    
    print("\n" + "="*80)
    print("TEST 1: VectorStoreService - Load FAISS Index")
    print("="*80)
    
    vs = VectorStoreService()
    
    # Test 1: Load index
    print("\n[1] Đang load FAISS index...")
    loaded = vs.load_faiss_index()
    
    if not loaded:
        print("⚠️  FAISS index không tìm thấy. Bạn cần chạy import_regulation script trước.")
        return
    
    print(f"✅ Đã load FAISS index thành công")
    print(f"   - Số chunks: {len(vs.metadata)}")
    print(f"   - Embedding dim: {vs.embedding_dim}")
    
    # Test 2: Một số test queries
    test_queries = [
        "Sinh viên đi trễ bao lâu không được vào thi?",
        "Điều lệ về mang điện thoại vào phòng thi",
        "Quy định khi sinh viên vắng thi",
        "Sinh viên phải tới phòng thi lúc mấy giờ?",
    ]
    
    print("\n[2] Testing Vector Search với các queries...")
    for query in test_queries:
        print(f"\n📝 Query: '{query}'")
        results = vs.search_with_citations(query, k=3)
        
        if not results:
            print("   ❌ Không tìm thấy kết quả")
            continue
        
        for i, result in enumerate(results, 1):
            text = result['text'][:80] + "..." if len(result['text']) > 80 else result['text']
            similarity = result['similarity']
            print(f"   [{i}] Similarity: {similarity:.2f}")
            print(f"       Text: {text}")
            
            citation = result.get('citation', {})
            if citation:
                print(f"       Article: {citation.get('article', 'N/A')}, "
                      f"Clause: {citation.get('clause', 'N/A')}")


def test_regulation_service():
    """Test RegulationService với Vector Search"""
    print("\n" + "="*80)
    print("TEST 2: RegulationService - answer_regulation_question")
    print("="*80)
    
    from services.regulation_service import RegulationService
    
    rs = RegulationService()
    print(f"\n✅ Vector Store Ready: {rs.vector_store_ready}")
    
    test_questions = [
        "Nếu đi trễ 20 phút có được vào thi không?",
        "Điều lệ về điện thoại trong phòng thi",
    ]
    
    print("\n[Testing RAG Response]")
    for question in test_questions:
        print(f"\n❓ Question: '{question}'")
        print("-" * 60)
        
        # Lấy chunks
        context = rs._retrieve_relevant_chunks(question)
        if context:
            print(f"✅ Chunks tìm thấy ({len(context)} chars):")
            print(context[:200] + "..." if len(context) > 200 else context)
        else:
            print("❌ Không tìm thấy chunks liên quan")


if __name__ == "__main__":
    try:
        print("\n🚀 Vector Search Testing\n")
        test_vector_store_service()
        test_regulation_service()
        print("\n" + "="*80)
        print("✅ All tests completed!")
        print("="*80 + "\n")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
