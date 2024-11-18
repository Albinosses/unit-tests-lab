import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from classes import AvgCalculator

@pytest.fixture
def calculator():
    return AvgCalculator()

class TestAvgCalculator:
    def test_get_avg_for_task_with_module_filter(self, calculator, stats_data):
        result = calculator.get_avg_for_task(stats_data, "Module1", "scores")
        assert len(result) == 2
        task_averages = {task["name"]: task["Average progress"] for task in result}
        assert pytest.approx(task_averages["Task1"]) == 77.5
        assert pytest.approx(task_averages["Task2"]) == 92.5

    def test_get_avg_for_task_without_module_filter(self, calculator, stats_data):
        result = calculator.get_avg_for_task(stats_data, None, "scores")
        assert len(result) == 4
        expected_averages = {
            "Task1": 77.5,
            "Task2": 92.5,
            "Task3": 77.5,
            "Task4": 87.5
        }
        task_averages = {task["name"]: task["Average progress"] for task in result}
        for task_name, expected_avg in expected_averages.items():
            assert pytest.approx(task_averages[task_name]) == expected_avg

    @pytest.mark.parametrize("metric_type,expected", [
        ("scores", {"Task1": 77.5, "Task2": 92.5}),
        ("time_spent", {"Task1": 110, "Task2": 100})
    ])
    def test_get_avg_for_task_metrics(self, calculator, stats_data, metric_type, expected):
        result = calculator.get_avg_for_task(stats_data, "Module1", metric_type)
        task_averages = {task["name"]: task["Average progress"] for task in result}
        assert all(pytest.approx(task_averages[name]) == value 
                  for name, value in expected.items())

    @pytest.mark.parametrize("metric_type,expected", [
        ("scores", {"Module1": 85, "Module2": 82.5}),
        ("time_spent", {"Module1": 105, "Module2": 125})
    ])
    def test_get_avg_for_module_metrics(self, calculator, stats_data, metric_type, expected):
        result = calculator.get_avg_for_module(stats_data, metric_type)
        module_averages = {module["name"]: module["Average progress"] for module in result}
        assert all(pytest.approx(module_averages[name]) == value 
                  for name, value in expected.items())

    @pytest.mark.parametrize("method,args", [
        ("get_avg_for_task", (None, "scores")),
        ("get_avg_for_module", ("scores",))
    ])
    def test_empty_data(self, calculator, method, args):
        empty_data = {"results": []}
        result = getattr(calculator, method)(empty_data, *args)
        assert result == []

    def test_missing_module(self, calculator, stats_data):
        result = calculator.get_avg_for_task(stats_data, "NonExistentModule", "scores")
        assert result == []

    def test_invalid_metric_type(self, calculator, stats_data):
        with pytest.raises(KeyError):
            calculator.get_avg_for_task(stats_data, None, "invalid_metric")

    def test_module_with_no_tasks(self, calculator):
        data_with_zero_tasks = {"results": [{"scores": {"EmptyModule": {}}}]}
        result = calculator.get_avg_for_module(data_with_zero_tasks, "scores")
        assert result == []

    @pytest.mark.parametrize("method,args", [
        ("get_avg_for_task", (None, "scores")),
        ("get_avg_for_module", ("scores",))
    ])
    def test_none_input_data(self, calculator, method, args):
        with pytest.raises(TypeError):
            getattr(calculator, method)(None, *args)

    def test_malformed_data_structure(self, calculator):
        malformed_data = {"results": [{"scores": "not_a_dict"}]}
        with pytest.raises(AttributeError):
            calculator.get_avg_for_task(malformed_data, None, "scores")