import pytest

@pytest.fixture
def sample_course_data():
    return {"course": "Python", "students": 50}

@pytest.fixture
def sample_json_data():
    return '{"course": "Python", "students": 50}'

@pytest.fixture
def stats_data():
    return {
        "results": [
            {
                "scores": {
                    "Module1": {
                        "Task1": 80,
                        "Task2": 90
                    },
                    "Module2": {
                        "Task3": 70,
                        "Task4": 85
                    }
                },
                "time_spent": {
                    "Module1": {
                        "Task1": 120,
                        "Task2": 90
                    },
                    "Module2": {
                        "Task3": 150,
                        "Task4": 100
                    }
                }
            },
            {
                "scores": {
                    "Module1": {
                        "Task1": 75,
                        "Task2": 95
                    },
                    "Module2": {
                        "Task3": 85,
                        "Task4": 90
                    }
                },
                "time_spent": {
                    "Module1": {
                        "Task1": 100,
                        "Task2": 110
                    },
                    "Module2": {
                        "Task3": 130,
                        "Task4": 120
                    }
                }
            }
        ]
    }