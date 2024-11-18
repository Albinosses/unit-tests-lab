import pytest
from unittest.mock import patch, mock_open
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from classes import CourseDataStream

class TestCourseDataStream:
    def test_get_course_data_stream_opens_file(self, sample_json_data):
        with patch("builtins.open", new_callable=mock_open, read_data=sample_json_data) as mock_file:
            stream = CourseDataStream()
            result = stream.get_course_data_stream("dummy_path.json")
            assert hasattr(result, "read")
            assert result.read() == sample_json_data

    def test_get_course_data_stream_file_not_found(self):
        with patch("builtins.open", side_effect=FileNotFoundError):
            stream = CourseDataStream()
            with pytest.raises(FileNotFoundError):
                stream.get_course_data_stream("nonexistent.json")