"""
Test keyword matching với diacritics normalization
"""
import unicodedata

def normalize_text(text):
    """Normalize Vietnamese text by removing diacritics"""
    nfd = unicodedata.normalize('NFD', text)
    return ''.join(c for c in nfd if unicodedata.category(c) != 'Mn')

# Mock chunks data (no diacritics)
chunks_data = [
    "Dieu 12 Khoan 3: Sinh vien khong duoc mang dien thoai vao phong thi duoi moi hinh thuc.",
    "Dieu 8 Khoan 1: Sinh vien phai co mat truoc gio thi 15 phut va xuat trinh the sinh vien.",
]

def test_keyword_matching(query, chunks):
    """Simulate keyword matching retrieval with diacritics normalization"""
    print(f"\n❓ Query: '{query}'")
    print("-" * 70)
    
    relevant_text = []
    query_words = [normalize_text(w.lower().strip()) for w in query.split() if w.strip()]
    
    print(f"Normalized query words: {query_words}")
    
    for chunk in chunks:
        content_lower = normalize_text(chunk.lower())
        match_count = sum(1 for word in query_words if word in content_lower)
        
        print(f"\n  Chunk: {chunk[:60]}...")
        print(f"  Normalized: {content_lower[:60]}...")
        print(f"  Matches: {match_count}/{len(query_words)}")
        
        # Nếu match >= 1 từ query, thêm vào kết quả
        if match_count >= 1:
            relevant_text.append((chunk, match_count))
            print(f"  ✅ MATCHED")
        else:
            print(f"  ❌ NO MATCH")
    
    # Sort by match count
    relevant_text.sort(key=lambda x: x[1], reverse=True)
    results = [text for text, _ in relevant_text[:5]]
    
    if results:
        print(f"\n✅ Found {len(results)} relevant chunk(s):")
        for i, text in enumerate(results, 1):
            print(f"   [{i}] {text}")
        return "\n\n".join(results)
    else:
        print("\n❌ No relevant chunks found")
        return ""


# Test queries with Vietnamese diacritics
test_queries = [
    "Sinh viên đi trễ bao lâu không được vào thi?",
    "Điều lệ về mang điện thoại vào phòng thi",
    "Khi nào phải có mặt trước giờ thi?",
    "Quy định về bài kiểm tra",
]

print("="*70)
print("KEYWORD MATCHING TEST WITH DIACRITICS NORMALIZATION")
print("="*70)

for query in test_queries:
    context = test_keyword_matching(query, chunks_data)
    print()

print("="*70)
