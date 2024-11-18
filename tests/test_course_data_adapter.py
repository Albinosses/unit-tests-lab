import pytest
import json
from unittest.mock import patch, mock_open
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from classes import CourseDataAdapter, DBCourseData, CourseDataStream

class TestCourseDataAdapter:
    def test_get_course_statistics_from_stream(self, sample_json_data, sample_course_data):
        with patch("builtins.open", new_callable=mock_open, read_data=sample_json_data):
            adapter = CourseDataAdapter()
            result = adapter.get_course_statistics("dummy_path.json")
            assert result == sample_course_data

    def test_get_course_statistics_file_not_found(self):
        with patch("builtins.open", side_effect=FileNotFoundError):
            adapter = CourseDataAdapter()
            with pytest.raises(FileNotFoundError):
                adapter.get_course_statistics("nonexistent.json")

    def test_get_course_statistics_invalid_json(self):
        with patch("builtins.open", new_callable=mock_open, read_data='invalid json'):
            adapter = CourseDataAdapter()
            with pytest.raises(json.JSONDecodeError):
                adapter.get_course_statistics("dummy_path.json")

    def test_get_course_statistics_inheritance(self):
        adapter = CourseDataAdapter()
        assert isinstance(adapter, DBCourseData)
        assert isinstance(adapter, CourseDataStream)