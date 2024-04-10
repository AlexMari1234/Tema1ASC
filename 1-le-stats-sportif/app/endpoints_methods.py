from flask import request
import json
import os

class SolveEndpoint:

    def __init__(self):
        pass

    def calculate_states_mean(self, data, question, job_id, webserver_data_ingestor_dict, webserver_jobs_status):
        state_media = {}

        for i in range(len(webserver_data_ingestor_dict["Question"])):
            if webserver_data_ingestor_dict["Question"][i] == question:
                if webserver_data_ingestor_dict["LocationDesc"][i] not in state_media:
                    state_media[webserver_data_ingestor_dict["LocationDesc"][i]] = [0.0, 0.0]
                if webserver_data_ingestor_dict["Data_Value"][i]:
                    state_media[webserver_data_ingestor_dict["LocationDesc"][i]][0] += float(webserver_data_ingestor_dict["Data_Value"][i])
                    state_media[webserver_data_ingestor_dict["LocationDesc"][i]][1] += 1

        results = {}
        for state in state_media:
            results[state] = state_media[state][0] / state_media[state][1]

        results_dir = 'results'
        os.makedirs(results_dir, exist_ok=True)

        file_path = os.path.join(results_dir, f'{job_id}.json')
        with open(file_path, 'w') as f:
            json.dump(results, f)
        
        webserver_jobs_status[job_id] = 'done'
    

    def calculate_state_mean(self, data, question, state, job_id, data_ingestor_dict, webserver_jobs_status):
        sum_Data_Value = 0.0
        count = 0

        for i in range(len(data_ingestor_dict["Question"])):
            if data_ingestor_dict["Question"][i] == question and data_ingestor_dict["LocationDesc"][i] == state:
                if data_ingestor_dict["Data_Value"][i]:
                    sum_Data_Value += float(data_ingestor_dict["Data_Value"][i])
                    count += 1

        mean_value = sum_Data_Value / count if count else 0

        # Salvează rezultatul într-un fișier JSON
        result = {state: mean_value}
        results_dir = 'results'
        os.makedirs(results_dir, exist_ok=True)

        file_path = os.path.join(results_dir, f'{job_id}.json')
        with open(file_path, 'w') as f:
            json.dump(result, f)
        
        # Actualizează starea job-ului
        webserver_jobs_status[job_id] = 'done'
    

    def calculate_best5(self, data, question, job_id, webserver_data_ingestor_dict, webserver_jobs_status, webserver_questions_best_is_min):
        state_media = {}

        for i in range(len(webserver_data_ingestor_dict["Question"])):
            if webserver_data_ingestor_dict["Question"][i] == question:
                if webserver_data_ingestor_dict["LocationDesc"][i] not in state_media:
                    state_media[webserver_data_ingestor_dict["LocationDesc"][i]] = [0.0, 0.0]
                if webserver_data_ingestor_dict["Data_Value"][i]:
                    state_media[webserver_data_ingestor_dict["LocationDesc"][i]][0] += float(webserver_data_ingestor_dict["Data_Value"][i])
                    state_media[webserver_data_ingestor_dict["LocationDesc"][i]][1] += 1

        if question in webserver_questions_best_is_min:
            sorted_states = sorted(state_media.items(), key=lambda x: (x[1][0] / x[1][1]))
        else:
            sorted_states = sorted(state_media.items(), key=lambda x: (x[1][0] / x[1][1]), reverse=True)
        results = {}
        for i in range(0, 5):
            results[sorted_states[i][0]] = sorted_states[i][1][0] / sorted_states[i][1][1]

        results_dir = 'results'
        os.makedirs(results_dir, exist_ok=True)

        file_path = os.path.join(results_dir, f'{job_id}.json')
        with open(file_path, 'w') as f:
            json.dump(results, f)
        
        webserver_jobs_status[job_id] = 'done'
    

    def calculate_worst5(self, data, question, job_id, data_ingestor_dict, webserver_jobs_status, webserver_questions_best_is_min):
        state_media = {}
        for i in range(len(data_ingestor_dict["Question"])):
            if data_ingestor_dict["Question"][i] == question:
                if data_ingestor_dict["LocationDesc"][i] not in state_media:
                    state_media[data_ingestor_dict["LocationDesc"][i]] = [0.0, 0.0]
                if data_ingestor_dict["Data_Value"][i]:
                    state_media[data_ingestor_dict["LocationDesc"][i]][0] += float(data_ingestor_dict["Data_Value"][i])
                    state_media[data_ingestor_dict["LocationDesc"][i]][1] += 1

        if question in webserver_questions_best_is_min:
            sorted_states = sorted(state_media.items(), key=lambda x: (x[1][0] / x[1][1]), reverse=True)
        else:
            sorted_states = sorted(state_media.items(), key=lambda x: (x[1][0] / x[1][1]))
        results = {}
        for i in range(0, 5):
            results[sorted_states[i][0]] = sorted_states[i][1][0] / sorted_states[i][1][1]

        results_dir = 'results'
        os.makedirs(results_dir, exist_ok=True)

        file_path = os.path.join(results_dir, f'{job_id}.json')
        with open(file_path, 'w') as f:
            json.dump(results, f)
        
        webserver_jobs_status[job_id] = 'done'
    

    def calculate_global_mean(self, data, question, job_id, data_ingestor_dict, webserver_jobs_status):
        global_mean = 0.0
        count = 0

        for i in range(len(data_ingestor_dict["Question"])):
            if data_ingestor_dict["Question"][i] == question:
                if data_ingestor_dict["Data_Value"][i]:
                    global_mean += float(data_ingestor_dict["Data_Value"][i])
                    count += 1

        global_mean = global_mean / count if count else 0

        result = {"global_mean": global_mean}
        results_dir = 'results'
        os.makedirs(results_dir, exist_ok=True)

        file_path = os.path.join(results_dir, f'{job_id}.json')
        with open(file_path, 'w') as f:
            json.dump(result, f)
        
        webserver_jobs_status[job_id] = 'done'
    

    def calculate_diff_from_mean(self, data, question, job_id, data_ingestor_dict, webserver_jobs_status):
        global_mean = 0.0
        count = 0

        for i in range(len(data_ingestor_dict["Question"])):
            if data_ingestor_dict["Question"][i] == question:
                if data_ingestor_dict["Data_Value"][i]:
                    global_mean += float(data_ingestor_dict["Data_Value"][i])
                    count += 1

        global_mean = global_mean / count if count else 0

        state_media = {}
        for i in range(len(data_ingestor_dict["Question"])):
            if data_ingestor_dict["Question"][i] == question:
                if data_ingestor_dict["Data_Value"][i]:
                    if data_ingestor_dict["LocationDesc"][i] not in state_media:
                        state_media[data_ingestor_dict["LocationDesc"][i]] = [0.0, 0.0]
                    state_media[data_ingestor_dict["LocationDesc"][i]][0] += float(data_ingestor_dict["Data_Value"][i])
                    state_media[data_ingestor_dict["LocationDesc"][i]][1] += 1

        results = {}
        for state in state_media:
            results[state] = global_mean - state_media[state][0] / state_media[state][1]

        results_dir = 'results'
        os.makedirs(results_dir, exist_ok=True)

        file_path = os.path.join(results_dir, f'{job_id}.json')
        with open(file_path, 'w') as f:
            json.dump(results, f)
        
        webserver_jobs_status[job_id] = 'done'
    

    def calculate_state_diff_from_mean(self, data, question, state, job_id, data_ingestor_dict, webserver_jobs_status):
        global_mean = 0.0
        count_global = 0

        state_mean = 0.0
        count_state = 0

        for i in range(len(data_ingestor_dict["Question"])):
            if data_ingestor_dict["Question"][i] == question:
                if data_ingestor_dict["Data_Value"][i]:
                    global_mean += float(data_ingestor_dict["Data_Value"][i])
                    count_global += 1
                    if data_ingestor_dict["LocationDesc"][i] == state:
                        state_mean += float(data_ingestor_dict["Data_Value"][i])
                        count_state += 1

        global_mean = global_mean / count_global if count_global else 0
        state_mean = state_mean / count_state if count_state else 0

        result = {state: global_mean - state_mean}
        results_dir = 'results'
        os.makedirs(results_dir, exist_ok=True)

        file_path = os.path.join(results_dir, f'{job_id}.json')
        with open(file_path, 'w') as f:
            json.dump(result, f)
        
        webserver_jobs_status[job_id] = 'done'
    

    
    def calculate_mean_by_category(self, data, question, job_id, data_ingestor_dict, webserver_jobs_status):
        aggregated_data = {}

        for i in range(len(data_ingestor_dict["Question"])):
            if data_ingestor_dict["Question"][i] == question:
                state = data_ingestor_dict["LocationDesc"][i]
                category = data_ingestor_dict["StratificationCategory1"][i]
                segment = data_ingestor_dict["Stratification1"][i]
                value = float(data_ingestor_dict["Data_Value"][i]) if data_ingestor_dict["Data_Value"][i] else 0

                # Cheia este un tuple ce conține (Stat, Categorie, Segment)
                key = (state, category, segment)

                if key not in aggregated_data:
                    aggregated_data[key] = [0, 0]  # [Suma, Număr]

                # Adaugă valoarea la sumă și incrementez numărul
                aggregated_data[key][0] += value
                aggregated_data[key][1] += 1

        # Calculul mediei
        results = {}
        for key, (total, count) in aggregated_data.items():
            mean_value = total / count if count else 0
            results[key] = mean_value

        results_dir = 'results'
        os.makedirs(results_dir, exist_ok=True)

        file_path = os.path.join(results_dir, f'{job_id}.json')
        with open(file_path, 'w') as f:
            formatted_results = {str(key): value for key, value in results.items()}
            json.dump(formatted_results, f)
        
        webserver_jobs_status[job_id] = 'done'
    

    def calculate_state_mean_by_category(self, data, question, state, job_id, data_ingestor_dict, webserver_jobs_status):
        aggregated_data = {}

        for i in range(len(data_ingestor_dict["Question"])):
            if data_ingestor_dict["Question"][i] == question and data_ingestor_dict["LocationDesc"][i] == state:
                category = data_ingestor_dict["StratificationCategory1"][i]
                segment = data_ingestor_dict["Stratification1"][i]
                value = float(data_ingestor_dict["Data_Value"][i]) if data_ingestor_dict["Data_Value"][i] else 0

                key = (category, segment)

                if key not in aggregated_data:
                    aggregated_data[key] = [0, 0]

                aggregated_data[key][0] += value
                aggregated_data[key][1] += 1

        results = {}
        for key, (total, count) in aggregated_data.items():
            mean_value = total / count if count else 0
            results[key] = mean_value

        results_dir = 'results'
        os.makedirs(results_dir, exist_ok=True)

        file_path = os.path.join(results_dir, f'{job_id}.json')
        with open(file_path, 'w') as f:
            formatted_results = {str(key): value for key, value in results.items()}
            data_res = {}
            data_res[state] = formatted_results
            json.dump(data_res, f)
        
        webserver_jobs_status[job_id] = 'done'
    

