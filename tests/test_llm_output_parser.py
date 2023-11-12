import sys
import os
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
if __name__ == '__main__':
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0, parentdir)
    data_dir = os.path.join(parentdir, 'data')
else:
    data_dir = os.path.join(currentdir, 'data')

import unittest
import pandas as pd
from llm_output_parser import extract_tasks_content
from response_components import project_plan_components, task_outline_components
import re

from unittestlogging import TestCaseLogging

class TestProjectPlan(TestCaseLogging):

    def setUp(self):
        self.setup_logging(log_failures=True, log_successes=False, filename='test_llm_output_parser.log')

    def run_on_all_project_plan_data(func):
        def wrapper(self):
            print(os.path.join(data_dir, 'project_plan.parquet'))
            df = pd.read_parquet(os.path.join(data_dir, 'project_plan.parquet'))
            for index, row in df.iterrows():
                    func(self, row.iloc[0])
        return wrapper

    @run_on_all_project_plan_data
    def test_extract_tasks(self, data):
        extracted_data = extract_tasks_content(data, project_plan_components)
        self.assertIn('tasks', extracted_data.keys(),
                      data={'data': data, 'keys': extracted_data.keys()})
        if 'tasks' in extracted_data.keys():
            tasks_data = extracted_data['tasks']
            self.assertEqual(type(tasks_data), list,
                             data={'data': data, 'tasks_data': tasks_data})
            for li in tasks_data:
                self.assertEqual(type(li), str)
                if isinstance(li, str):
                    li_no_number = re.search(r'^\d+(?:\.\d+)*\.\s*(.*)', li).group(1)
                    self.assertIn(li_no_number, data)
                    


if __name__ == '__main__':
    unittest.main()