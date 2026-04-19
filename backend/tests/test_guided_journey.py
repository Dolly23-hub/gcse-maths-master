"""
Backend tests for GCSE Maths Master - Guided Learning Journey
Tests the 7-step guided learning journey enrichments for all 33 topics
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

class TestSeedIdempotency:
    """Test that POST /api/seed is idempotent and populates all topics"""
    
    def test_seed_endpoint_returns_success(self):
        """POST /api/seed should return success with correct counts"""
        response = requests.post(f"{BASE_URL}/api/seed")
        assert response.status_code == 200
        data = response.json()
        assert data["topics"] == 33, f"Expected 33 topics, got {data['topics']}"
        assert data["quizzes"] == 84, f"Expected 84 quizzes, got {data['quizzes']}"
        assert data["papers"] == 38, f"Expected 38 papers, got {data['papers']}"
        assert data["formulas"] == 30, f"Expected 30 formulas, got {data['formulas']}"
        print(f"PASS: Seed returned {data['topics']} topics, {data['quizzes']} quizzes")
    
    def test_seed_is_idempotent(self):
        """Running seed twice should produce same results"""
        response1 = requests.post(f"{BASE_URL}/api/seed")
        response2 = requests.post(f"{BASE_URL}/api/seed")
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response1.json() == response2.json(), "Seed should be idempotent"
        print("PASS: Seed is idempotent")


class TestTopicEnrichments:
    """Test that all 33 topics have the new guided journey fields"""
    
    # All 33 topic IDs (19 base + 14 additional)
    ALL_TOPIC_IDS = [
        # Base topics (19)
        "num-1", "num-2", "num-3", "num-4",
        "alg-1", "alg-2", "alg-3", "alg-4", "alg-5", "alg-6",
        "rat-1", "rat-2", "rat-3",
        "geo-1", "geo-2", "geo-3", "geo-4",
        "sta-1", "sta-2",
        # Additional topics (14)
        "num-5", "num-6",
        "alg-7", "alg-8", "alg-9",
        "rat-4", "rat-5",
        "geo-5", "geo-6", "geo-7", "geo-8",
        "sta-3", "sta-4", "sta-5"
    ]
    
    def test_all_topics_exist(self):
        """Verify all 33 topics are returned from GET /api/topics"""
        response = requests.get(f"{BASE_URL}/api/topics")
        assert response.status_code == 200
        data = response.json()
        topics = data.get("topics", [])
        assert len(topics) == 33, f"Expected 33 topics, got {len(topics)}"
        
        topic_ids = [t["id"] for t in topics]
        for tid in self.ALL_TOPIC_IDS:
            assert tid in topic_ids, f"Missing topic: {tid}"
        print(f"PASS: All 33 topics exist")
    
    @pytest.mark.parametrize("topic_id", ALL_TOPIC_IDS)
    def test_topic_has_enrichment_fields(self, topic_id):
        """Each topic should have video_id, big_idea, visual_example, step_by_step"""
        response = requests.get(f"{BASE_URL}/api/topics/{topic_id}")
        assert response.status_code == 200, f"Topic {topic_id} not found"
        topic = response.json()
        
        # Check video_id exists and is a valid YouTube ID
        assert "video_id" in topic, f"{topic_id} missing video_id"
        assert topic["video_id"] is not None, f"{topic_id} has null video_id"
        assert len(topic["video_id"]) >= 10, f"{topic_id} video_id too short: {topic['video_id']}"
        
        # Check big_idea exists and is non-empty
        assert "big_idea" in topic, f"{topic_id} missing big_idea"
        assert topic["big_idea"] is not None, f"{topic_id} has null big_idea"
        assert len(topic["big_idea"]) > 20, f"{topic_id} big_idea too short"
        
        # Check visual_example exists and is non-empty
        assert "visual_example" in topic, f"{topic_id} missing visual_example"
        assert topic["visual_example"] is not None, f"{topic_id} has null visual_example"
        assert len(topic["visual_example"]) > 50, f"{topic_id} visual_example too short"
        
        # Check step_by_step exists and has at least 3 steps
        assert "step_by_step" in topic, f"{topic_id} missing step_by_step"
        assert isinstance(topic["step_by_step"], list), f"{topic_id} step_by_step not a list"
        assert len(topic["step_by_step"]) >= 3, f"{topic_id} has fewer than 3 steps"
        
        print(f"PASS: {topic_id} has all enrichment fields")
    
    def test_diverse_topics_have_enrichments(self):
        """Test 3 diverse topics: num-1 (Number), alg-5 (Algebra), geo-5 (Geometry)"""
        diverse_topics = ["num-1", "alg-5", "geo-5"]
        
        for topic_id in diverse_topics:
            response = requests.get(f"{BASE_URL}/api/topics/{topic_id}")
            assert response.status_code == 200
            topic = response.json()
            
            # Verify all enrichment fields
            assert topic.get("video_id"), f"{topic_id} missing video_id"
            assert topic.get("big_idea"), f"{topic_id} missing big_idea"
            assert topic.get("visual_example"), f"{topic_id} missing visual_example"
            assert len(topic.get("step_by_step", [])) >= 3, f"{topic_id} missing steps"
            
            print(f"PASS: {topic_id} ({topic['category']}) has all enrichments")


class TestAITutor:
    """Test AI Tutor endpoint with topic context"""
    
    def test_ai_tutor_with_topic_context(self):
        """POST /api/ai-tutor should work with topic context"""
        payload = {
            "question": "What is the key concept?",
            "topic": "Fractions, Decimals & Percentages",
            "context": "Student is learning about converting between forms"
        }
        response = requests.post(f"{BASE_URL}/api/ai-tutor", json=payload)
        assert response.status_code == 200, f"AI Tutor failed: {response.text}"
        data = response.json()
        
        assert "response" in data, "Missing response field"
        assert len(data["response"]) > 50, "Response too short"
        assert "session_id" in data, "Missing session_id"
        print(f"PASS: AI Tutor returned response with {len(data['response'])} chars")
    
    def test_ai_tutor_without_topic(self):
        """POST /api/ai-tutor should work without topic context"""
        payload = {
            "question": "How do I solve quadratic equations?"
        }
        response = requests.post(f"{BASE_URL}/api/ai-tutor", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert len(data["response"]) > 20
        print("PASS: AI Tutor works without topic context")


class TestQuizzes:
    """Test quiz endpoints for topics"""
    
    def test_quiz_for_num1(self):
        """GET /api/quizzes/num-1 should return questions"""
        response = requests.get(f"{BASE_URL}/api/quizzes/num-1")
        assert response.status_code == 200
        data = response.json()
        questions = data.get("questions", [])
        assert len(questions) >= 2, f"Expected at least 2 questions for num-1, got {len(questions)}"
        
        # Verify question structure
        q = questions[0]
        assert "id" in q
        assert "question" in q
        assert "options" in q
        assert len(q["options"]) == 4
        assert "correct_answer" in q
        assert "explanation" in q
        print(f"PASS: num-1 has {len(questions)} quiz questions")
    
    def test_quiz_check_answer(self):
        """POST /api/quiz/check should return correct/incorrect with explanation"""
        # First get a question
        response = requests.get(f"{BASE_URL}/api/quizzes/num-1")
        questions = response.json().get("questions", [])
        if not questions:
            pytest.skip("No questions available")
        
        q = questions[0]
        
        # Check correct answer
        payload = {"question_id": q["id"], "selected_answer": q["correct_answer"]}
        response = requests.post(f"{BASE_URL}/api/quiz/check", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["correct"] == True
        assert "explanation" in data
        print("PASS: Quiz check returns correct answer with explanation")


class TestRegressionEndpoints:
    """Regression tests for existing endpoints"""
    
    def test_topics_list(self):
        """GET /api/topics should return all topics"""
        response = requests.get(f"{BASE_URL}/api/topics")
        assert response.status_code == 200
        data = response.json()
        assert "topics" in data
        assert len(data["topics"]) == 33
        print("PASS: Topics list returns 33 topics")
    
    def test_formulas(self):
        """GET /api/formulas should return formulas"""
        response = requests.get(f"{BASE_URL}/api/formulas")
        assert response.status_code == 200
        data = response.json()
        assert "formulas" in data
        assert len(data["formulas"]) == 30
        print("PASS: Formulas endpoint returns 30 formulas")
    
    def test_past_papers_edexcel(self):
        """GET /api/past-papers/Edexcel should return papers"""
        response = requests.get(f"{BASE_URL}/api/past-papers/Edexcel")
        assert response.status_code == 200
        data = response.json()
        assert "papers" in data
        assert len(data["papers"]) >= 10
        print(f"PASS: Edexcel has {len(data['papers'])} past papers")
    
    def test_revision_plan(self):
        """POST /api/revision-plan should generate a plan"""
        payload = {
            "exam_board": "Edexcel",
            "exam_date": "2026-06-15",
            "confidence": {
                "Number": 3,
                "Algebra": 2,
                "Ratio & Proportion": 4,
                "Geometry & Measures": 2,
                "Probability & Statistics": 3
            },
            "study_hours_per_day": 1.5,
            "use_ai": False
        }
        response = requests.post(f"{BASE_URL}/api/revision-plan", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "schedule" in data
        assert "days_remaining" in data
        print("PASS: Revision plan endpoint works")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
