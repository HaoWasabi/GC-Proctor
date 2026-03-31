"""
Test keyword matching - simulate regulation question
"""
import sys
sys.path.insert(0, "src")

from services.regulation_service import RegulationService

print("Testing Regulation Search with Keyword Matching\n")

rs = RegulationService()

test_questions = [
    "Sinh viên đi trễ bao lâu không được vào thi?",
    "Điều lệ về mang điện thoại",
    "Khi nào phải có mặt trước giờ thi?",
    "Quy định về điện thoại trong phòng thi",
]

for question in test_questions:
    print(f"❓ {question}")
    print("-" * 70)
    
    # Get chunks
    context = rs._retrieve_relevant_chunks(question)
    print(f"Context length: {len(context)} chars")
    
    if context:
        print(f"Context: {context}\n")
        
        # Try to answer
        answer = rs.answer_regulation_question(question)
        print(f"Answer: {answer[:200]}...\n")
    else:
        print("❌ No context found\n")
    
    print()
