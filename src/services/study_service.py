from fastapi import HTTPException
from services.kb_service import KBService
from services.nlp_service import NLPService
from repositories.study_repository import StudyRepository
from pydantic import BaseModel
class StudyService:
    def __init__(self):
        self.kb_service = KBService()
        self.nlp_service = NLPService()
        self.repository = StudyRepository()

    def query(self, payload: dict) -> dict:
        """
        Real implementation: Query knowledge base and generate answer
        """
        question = payload.get("question")
        if not question:
            raise HTTPException(status_code=400, detail="INVALID_INPUT: question")

        # 1. Retrieve relevant documents from KB
        course_id = payload.get("course_id")
        relevant_chunks = self.kb_service.retrieve_relevant_chunks(
            question,
            course_id=course_id
        )

        # 2. Generate answer using NLP/LLM
        answer = self.nlp_service.generate_answer(
            question,
            context=relevant_chunks
        )

        # 3. Extract citations
        citations = [
            {
                "chunk_id": chunk.id,
                "source": chunk.document.name,
                "text": chunk.content[:100]
            }
            for chunk in relevant_chunks
        ]

        # 4. Store query log
        self.repository.log_study_query(
            user_id=payload.get("user_id"),
            question=question,
            answer=answer,
            citations=citations
        )

        return {
            "answer": answer,
            "citations": citations,
        }

    def summarize(self, payload: dict) -> dict:
        """
        Real implementation: Summarize documents/content
        """
        source = payload.get("source")
        source_type = payload.get("source_type")  # "document", "course", "topic"
        if not source:
            raise HTTPException(status_code=400, detail="INVALID_INPUT: source")

        length = payload.get("length", "short")  # short, medium, long

        # 1. Fetch source content
        content = self._fetch_source_content(source, source_type)

        # 2. Generate summary using NLP
        summary = self.nlp_service.summarize(content, length_preference=length)

        # 3. Store summary log
        self.repository.log_study_summary(
            user_id=payload.get("user_id"),
            source=source,
            summary=summary,
            length=length
        )

        return {
            "summary": summary,
            "length": length,
            "source": source,
        }

    def generate_flashcards(self, payload: dict) -> dict:
        """
        Real implementation: Generate flashcards from content
        """
        topic = payload.get("topic")
        if not topic:
            raise HTTPException(status_code=400, detail="INVALID_INPUT: topic")

        num_cards = payload.get("num_cards", 10)
        difficulty = payload.get("difficulty", "medium")  # easy, medium, hard

        # 1. Retrieve relevant content for topic
        relevant_content = self.kb_service.retrieve_by_topic(
            topic,
            course_id=payload.get("course_id")
        )

        # 2. Generate flashcards using NLP
        flashcards = self.nlp_service.generate_flashcards(
            content=relevant_content,
            num_cards=num_cards,
            difficulty=difficulty
        )

        # 3. Save flashcards
        saved_cards = self.repository.save_flashcards(
            user_id=payload.get("user_id"),
            topic=topic,
            flashcards=flashcards
        )

        return {
            "topic": topic,
            "flashcards": saved_cards,
            "total": len(saved_cards),
        }

    def explain(self, payload: dict) -> dict:
        """
        Real implementation: Explain a concept with different difficulty levels
        """
        concept = payload.get("concept")
        if not concept:
            raise HTTPException(status_code=400, detail="INVALID_INPUT: concept")

        level = payload.get("level", "basic")  # basic, intermediate, advanced

        # 1. Retrieve relevant materials
        materials = self.kb_service.search_concept(concept)

        # 2. Generate explanation at appropriate level
        explanation = self.nlp_service.explain_concept(
            concept=concept,
            context=materials,
            difficulty_level=level
        )

        # 3. Add examples
        examples = self.nlp_service.generate_examples(concept, num=3)

        # 4. Log
        self.repository.log_concept_explanation(
            user_id=payload.get("user_id"),
            concept=concept,
            level=level
        )

        return {
            "concept": concept,
            "level": level,
            "explanation": explanation,
            "examples": examples,
        }

    def _fetch_source_content(self, source: str, source_type: str) -> str:
        """Helper: Fetch content based on source type"""
        if source_type == "document":
            return self.kb_service.get_document_content(source)
        elif source_type == "course":
            return self.kb_service.get_course_content(source)
        elif source_type == "topic":
            return self.kb_service.get_topic_content(source)
        return ""