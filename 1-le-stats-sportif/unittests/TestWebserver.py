import unittest
import time
import os
import json
from app.data_ingestor import DataIngestor
from app.endpoints_methods import SolveEndpoint as endpoints_methods
from flask import Flask

class TestWebserver(unittest.TestCase):
    def setUp(self):
        time.sleep(1)
    
    def test_best5(self):
        input_dir = "unittests/tests/best5/input"
        output_dir = "unittests/tests/best5/output"
        file_input = "in-1.json"
        file_output = "out-1.json"
        
        Data_Ingestor = DataIngestor("unittests/data_set.csv")

        with open(f"{input_dir}/{file_input}") as f:
            data = json.load(f)
        
        with open(f"{output_dir}/{file_output}") as f:
            expected = json.load(f)
        
        question = data["question"]
        job_status = {}
        endpoints_methods.calculate_best5(self, question, "job_id_best5", Data_Ingestor.dict, job_status, Data_Ingestor.questions_best_is_min)

        result = {}
        with open("results/job_id_best5.json") as f:
            result = json.load(f)
        
        for key in expected:
            self.assertAlmostEqual(result[key], expected[key], delta=0.001, msg=f"Key {key} failed")
        print("Test best5 passed")
    
    def test_worst5(self):
        input_dir = "unittests/tests/worst5/input"
        output_dir = "unittests/tests/worst5/output"
        file_input = "in-1.json"
        file_output = "out-1.json"
        
        Data_Ingestor = DataIngestor("unittests/data_set.csv")

        with open(f"{input_dir}/{file_input}") as f:
            data = json.load(f)
        
        question = data["question"]
        job_status = {}
        endpoints_methods.calculate_worst5(self, question, "job_id_worst5", Data_Ingestor.dict, job_status, Data_Ingestor.questions_best_is_min)
        with open(f"{output_dir}/{file_output}") as f:
            expected = json.load(f)
        
        result = {}
        with open("results/job_id_worst5.json") as f:
            result = json.load(f)
        
        for key in expected:
            self.assertAlmostEqual(result[key], expected[key], delta=0.001, msg=f"Key {key} failed")
        print("Test worst5 passed")
    
    def test_states_mean(self):
        input_dir = "unittests/tests/states_mean/input"
        output_dir = "unittests/tests/states_mean/output"
        file_input = "in-1.json"
        file_output = "out-1.json"
        
        Data_Ingestor = DataIngestor("unittests/data_set.csv")

        with open(f"{input_dir}/{file_input}") as f:
            data = json.load(f)
        
        question = data["question"]
        job_status = {}
        endpoints_methods.calculate_states_mean(self, question, "job_id_states_mean", Data_Ingestor.dict, job_status)
        with open(f"{output_dir}/{file_output}") as f:
            expected = json.load(f)
        
        result = {}
        with open("results/job_id_states_mean.json") as f:
            result = json.load(f)
        
        for key in expected:
            self.assertAlmostEqual(result[key], expected[key], delta=0.001, msg=f"Key {key} failed")
        print("Test states_mean passed")
    
    def test_diff_from_mean(self):
        input_dir = "unittests/tests/diff_from_mean/input"
        output_dir = "unittests/tests/diff_from_mean/output"
        file_input = "in-1.json"
        file_output = "out-1.json"
        
        Data_Ingestor = DataIngestor("unittests/data_set.csv")

        with open(f"{input_dir}/{file_input}") as f:
            data = json.load(f)
        
        question = data["question"]
        job_status = {}
        endpoints_methods.calculate_diff_from_mean(self, question, "job_id_diff_from_mean", Data_Ingestor.dict, job_status)
        with open(f"{output_dir}/{file_output}") as f:
            expected = json.load(f)
        
        result = {}
        with open("results/job_id_diff_from_mean.json") as f:
            result = json.load(f)
        
        for key in expected:
            self.assertAlmostEqual(result[key], expected[key], delta=0.001, msg=f"Key {key} failed")
        print("Test diff_from_mean passed")
    
    def test_mean_by_category(self):
        input_dir = "unittests/tests/mean_by_category/input"
        output_dir = "unittests/tests/mean_by_category/output"
        file_input = "in-1.json"
        file_output = "out-1.json"
        
        Data_Ingestor = DataIngestor("unittests/data_set.csv")

        with open(f"{input_dir}/{file_input}") as f:
            data = json.load(f)
        
        question = data["question"]
        job_status = {}
        endpoints_methods.calculate_mean_by_category(self, question, "job_id_mean_by_category", Data_Ingestor.dict, job_status)
        with open(f"{output_dir}/{file_output}") as f:
            expected = json.load(f)
        
        result = {}
        with open("results/job_id_mean_by_category.json") as f:
            result = json.load(f)
        
        sorted_result = dict(sorted(result.items()))
        sorted_expected = dict(sorted(expected.items()))
        for key in sorted_expected:
            self.assertAlmostEqual(sorted_result[key], sorted_expected[key], delta=0.001, msg=f"Key {key} failed")

        print("Test mean_by_category passed")
    
    def test_state_diff_from_mean(self):
        input_dir = "unittests/tests/state_diff_from_mean/input"
        output_dir = "unittests/tests/state_diff_from_mean/output"
        file_input = "in-1.json"
        file_output = "out-1.json"
        
        Data_Ingestor = DataIngestor("unittests/data_set.csv")

        with open(f"{input_dir}/{file_input}") as f:
            data = json.load(f)
        
        question = data["question"]
        state = data["state"]
        job_status = {}
        endpoints_methods.calculate_state_diff_from_mean(self, question, state, "job_id_state_diff_from_mean", Data_Ingestor.dict, job_status)
        with open(f"{output_dir}/{file_output}") as f:
            expected = json.load(f)
        
        result = {}
        with open("results/job_id_state_diff_from_mean.json") as f:
            result = json.load(f)
        
        for key in expected:
            self.assertAlmostEqual(result[key], expected[key], delta=0.001, msg=f"Key {key} failed")
        print("Test state_diff_from_mean passed")
    
    def test_state_mean(self):
        input_dir = "unittests/tests/state_mean/input"
        output_dir = "unittests/tests/state_mean/output"
        file_input = "in-1.json"
        file_output = "out-1.json"
        
        Data_Ingestor = DataIngestor("unittests/data_set.csv")

        with open(f"{input_dir}/{file_input}") as f:
            data = json.load(f)
        
        question = data["question"]
        state = data["state"]
        job_status = {}
        endpoints_methods.calculate_state_mean(self, question, state, "job_id_state_mean", Data_Ingestor.dict, job_status)
        with open(f"{output_dir}/{file_output}") as f:
            expected = json.load(f)
        
        result = {}
        with open("results/job_id_state_mean.json") as f:
            result = json.load(f)
        
        for key in expected:
            self.assertAlmostEqual(result[key], expected[key], delta=0.001, msg=f"Key {key} failed")
        print("Test state_mean passed")
    
    def test_state_mean_by_category(self):
        input_dir = "unittests/tests/state_mean_by_category/input"
        output_dir = "unittests/tests/state_mean_by_category/output"
        file_input = "in-1.json"
        file_output = "out-1.json"
        
        Data_Ingestor = DataIngestor("unittests/data_set.csv")

        with open(f"{input_dir}/{file_input}") as f:
            data = json.load(f)
        
        question = data["question"]
        state = data["state"]
        job_status = {}
        endpoints_methods.calculate_state_mean_by_category(self, question, state, "job_id_state_mean_by_category", Data_Ingestor.dict, job_status)
        with open(f"{output_dir}/{file_output}") as f:
            expected = json.load(f)
        
        result = {}
        with open("results/job_id_state_mean_by_category.json") as f:
            result = json.load(f)
        
        for key in expected:
            for key2 in expected[key]:
                self.assertAlmostEqual(result[key][key2], expected[key][key2], delta=0.001, msg=f"Key {key} failed")
        print("Test state_mean_by_category passed")
    
    def test_global_mean(self):
        input_dir = "unittests/tests/global_mean/input"
        output_dir = "unittests/tests/global_mean/output"
        file_input = "in-1.json"
        file_output = "out-1.json"
        
        Data_Ingestor = DataIngestor("unittests/data_set.csv")

        with open(f"{input_dir}/{file_input}") as f:
            data = json.load(f)
        
        question = data["question"]
        job_status = {}
        endpoints_methods.calculate_global_mean(self, question, "job_id_global_mean", Data_Ingestor.dict, job_status)
        with open(f"{output_dir}/{file_output}") as f:
            expected = json.load(f)
        
        result = {}
        with open("results/job_id_global_mean.json") as f:
            result = json.load(f)
        
        for key in expected:
            self.assertAlmostEqual(result[key], expected[key], delta=0.001, msg=f"Key {key} failed")
        print("Test global_mean passed")
            
