import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from classes import DBCourseData

class TestDBCourseData:
    def test_get_course_statistics_returns_source(self, sample_course_data):
        db_data = DBCourseData()
        result = db_data.get_course_statistics(sample_course_data)
        assert result == sample_course_data
