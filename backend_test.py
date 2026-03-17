import requests
import sys
import json
from datetime import datetime

class GCSEMathsAPITester:
    def __init__(self):
        self.base_url = "https://gcse-maths-master.preview.emergentagent.com/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []

    def run_test(self, name, method, endpoint, expected_status=200, data=None, params=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}" if endpoint else self.base_url
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=30)

            print(f"   Status: {response.status_code}")
            
            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    return response.json()
                except:
                    return {"message": "Success (no JSON response)"}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                self.failed_tests.append({
                    "test": name,
                    "expected": expected_status,
                    "actual": response.status_code,
                    "endpoint": endpoint,
                    "response": response.text[:500]
                })
                return None

        except requests.exceptions.Timeout:
            print(f"❌ Failed - Request timeout after 30 seconds")
            self.failed_tests.append({
                "test": name,
                "error": "Timeout",
                "endpoint": endpoint
            })
            return None
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            self.failed_tests.append({
                "test": name,
                "error": str(e),
                "endpoint": endpoint
            })
            return None

    def test_api_root(self):
        """Test API root endpoint"""
        response = self.run_test("API Root", "GET", "")
        return response is not None

    def test_get_topics(self):
        """Test getting all topics"""
        response = self.run_test("Get All Topics", "GET", "topics")
        if response and 'topics' in response:
            print(f"   Found {len(response['topics'])} topics")
            return len(response['topics']) >= 19  # Should have 19+ topics
        return False

    def test_get_topics_by_category(self):
        """Test getting topics by category"""
        categories = ["Number", "Algebra", "Ratio & Proportion", "Geometry & Measures", "Probability & Statistics"]
        success_count = 0
        
        for category in categories:
            response = self.run_test(f"Get Topics - {category}", "GET", f"topics/category/{category}")
            if response and 'topics' in response:
                print(f"   Found {len(response['topics'])} topics in {category}")
                success_count += 1
            
        return success_count == len(categories)

    def test_get_single_topic(self):
        """Test getting a single topic by ID"""
        # First get all topics to find a valid ID
        topics_response = self.run_test("Get Topics for Single Test", "GET", "topics")
        if topics_response and 'topics' in topics_response and len(topics_response['topics']) > 0:
            topic_id = topics_response['topics'][0]['id']
            response = self.run_test(f"Get Single Topic ({topic_id})", "GET", f"topics/{topic_id}")
            return response is not None and 'title' in response
        return False

    def test_past_papers(self):
        """Test getting past papers for all boards"""
        boards = ["Edexcel", "AQA", "OCR"]
        success_count = 0
        
        for board in boards:
            response = self.run_test(f"Get Past Papers - {board}", "GET", f"past-papers/{board}")
            if response and 'papers' in response:
                print(f"   Found {len(response['papers'])} papers for {board}")
                success_count += 1
                
        return success_count == len(boards)

    def test_quizzes(self):
        """Test quiz endpoints"""
        # Test all quizzes
        response = self.run_test("Get All Quizzes", "GET", "quizzes")
        all_quiz_success = response is not None and 'questions' in response
        
        if all_quiz_success:
            print(f"   Found {len(response['questions'])} quiz questions")
            
            # Test specific topic quiz if we have topics
            topics_response = self.run_test("Get Topics for Quiz Test", "GET", "topics")
            if topics_response and 'topics' in topics_response and len(topics_response['topics']) > 0:
                topic_id = topics_response['topics'][0]['id']
                quiz_response = self.run_test(f"Get Quiz for Topic ({topic_id})", "GET", f"quizzes/{topic_id}")
                return quiz_response is not None
                
        return all_quiz_success

    def test_quiz_check(self):
        """Test quiz answer checking"""
        # First get a quiz question
        response = self.run_test("Get Quiz for Check Test", "GET", "quizzes")
        if response and 'questions' in response and len(response['questions']) > 0:
            question = response['questions'][0]
            question_id = question['id']
            
            # Test checking an answer (try answer 0)
            check_response = self.run_test(
                "Check Quiz Answer", 
                "POST", 
                "quiz/check",
                200,
                {"question_id": question_id, "selected_answer": 0}
            )
            return check_response is not None and 'correct' in check_response
            
        return False

    def test_formulas(self):
        """Test formula endpoints"""
        response = self.run_test("Get All Formulas", "GET", "formulas")
        if response and 'formulas' in response:
            print(f"   Found {len(response['formulas'])} formulas")
            
            # Should have 20+ formulas
            formula_count_ok = len(response['formulas']) >= 20
            
            # Test category endpoint
            category_response = self.run_test("Get Formulas by Category", "GET", "formulas/category/Number")
            category_ok = category_response is not None and 'formulas' in category_response
            
            return formula_count_ok and category_ok
        return False

    def test_ai_tutor(self):
        """Test AI Tutor endpoint"""
        test_question = {
            "question": "What is 2 + 2?",
            "topic": "Number",
            "context": "Basic arithmetic"
        }
        
        response = self.run_test("AI Tutor", "POST", "ai-tutor", 200, test_question)
        if response and 'response' in response:
            print(f"   AI Response length: {len(response['response'])} characters")
            return len(response['response']) > 10  # Should get a meaningful response
        return False

    def test_database_seeding(self):
        """Test database seeding endpoint"""
        response = self.run_test("Database Seed", "POST", "seed", 200)
        return response is not None and 'message' in response

def main():
    print("🚀 Starting GCSE Maths API Tests")
    print("=" * 50)
    
    tester = GCSEMathsAPITester()
    
    # Run all tests
    test_results = {
        "API Root": tester.test_api_root(),
        "Topics": tester.test_get_topics(),
        "Topics by Category": tester.test_get_topics_by_category(),
        "Single Topic": tester.test_get_single_topic(),
        "Past Papers": tester.test_past_papers(),
        "Quizzes": tester.test_quizzes(),
        "Quiz Answer Check": tester.test_quiz_check(),
        "Formulas": tester.test_formulas(),
        "AI Tutor": tester.test_ai_tutor(),
        # Skip seeding for now as it might interfere with existing data
        # "Database Seed": tester.test_database_seeding(),
    }
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    for test_name, passed in test_results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:<25} {status}")
    
    print(f"\nTotal Tests: {tester.tests_run}")
    print(f"Passed: {tester.tests_passed}")
    print(f"Failed: {len(tester.failed_tests)}")
    print(f"Success Rate: {(tester.tests_passed/tester.tests_run*100):.1f}%")
    
    if tester.failed_tests:
        print("\n❌ FAILED TESTS DETAILS:")
        for i, failure in enumerate(tester.failed_tests, 1):
            print(f"\n{i}. {failure['test']}")
            print(f"   Endpoint: {failure.get('endpoint', 'N/A')}")
            if 'expected' in failure:
                print(f"   Expected: {failure['expected']}, Got: {failure['actual']}")
            if 'error' in failure:
                print(f"   Error: {failure['error']}")
            if 'response' in failure:
                print(f"   Response: {failure['response'][:200]}...")
    
    return 0 if tester.tests_passed == tester.tests_run else 1

if __name__ == "__main__":
    sys.exit(main())