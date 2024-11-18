import json
from typing import TextIO


class DBCourseData:
    def get_course_statistics(self, source) -> dict:
        # in most cases we'll have some data base connector (Postgres or Snowflake), in this case we know how to transform data
        return source


class CourseDataStream:
    # but in our case we have json data stream, and we don't know how to transform data
    def get_course_data_stream(self, path) -> TextIO:
        return open(path)

class CourseDataAdapter(DBCourseData, CourseDataStream):
    # we use CourseDataAdapter to smoothly integrate stream to CourseData

    def get_course_statistics(self, path) -> dict:
        return json.load(self.get_course_data_stream(path))

class AvgCalculator():
    def get_avg_for_task(self, data, module_name, metric_type):
        task_metric = {}
        task_counts = {}

        for course in data["results"]:
            metrics = course[metric_type]
            for module, tasks in metrics.items():
                if module_name and module != module_name:
                    continue
                for task, metric in tasks.items():
                    if task not in task_metric:
                        task_metric[task] = 0
                        task_counts[task] = 0
                    task_metric[task] += metric
                    task_counts[task] += 1

        average_scores = [
            {"name": task, "Average progress": total_score / task_counts[task]}
            for task, total_score in task_metric.items()
        ]
        return average_scores

    def get_avg_for_module(self, data, metric_type):
        module_metric = {}
        module_task_counts = {}

        for course in data["results"]:
            metrics = course[metric_type]
            for module, tasks in metrics.items():
                if module not in module_metric:
                    module_metric[module] = 0
                    module_task_counts[module] = 0
                for task, metric in tasks.items():
                    module_metric[module] += metric
                    module_task_counts[module] += 1

        average_module_scores = [
            {"name": module, "Average progress": total_score / module_task_counts[module]}
            for module, total_score in module_metric.items()
        ]
        return average_module_scores