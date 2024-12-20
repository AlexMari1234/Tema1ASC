import json
import os
from app.logger import AppLogger

logger = AppLogger.get_logger("webserver.log")

class SolveEndpoint:

    def __init__(self):
        pass

    def calculate_states_mean(self, question, job_id,
                              webserver_data_ingestor_dict, webserver_jobs_status):
        webserver_jobs_status[job_id] = 'running'
        logger.info('Calculating states mean for job %s', job_id)
        state_media = {}
        for i in range(len(webserver_data_ingestor_dict["Question"])):
            if webserver_data_ingestor_dict["Question"][i] == question:
                if webserver_data_ingestor_dict["LocationDesc"][i] not in state_media:
                    state_media[webserver_data_ingestor_dict["LocationDesc"][i]] = [0.0, 0.0]
                if webserver_data_ingestor_dict["Data_Value"][i]:
                    state_media[webserver_data_ingestor_dict["LocationDesc"][i]][0] += float(
                        webserver_data_ingestor_dict["Data_Value"][i])
                    state_media[webserver_data_ingestor_dict["LocationDesc"][i]][1] += 1

        results = {}
        for state in state_media:
            results[state] = state_media[state][0] / state_media[state][1]

        results_dir = 'results'
        file_path = os.path.join(results_dir, f'{job_id}.json')
        with open(file_path, 'w') as f:
            json.dump(results, f)

        webserver_jobs_status[job_id] = 'done'
        logger.info('Finished calculating states mean for job %s', job_id)

    def calculate_state_mean(self, question, state, job_id,
                             data_ingestor_dict, webserver_jobs_status):
        webserver_jobs_status[job_id] = 'running'
        logger.info('Calculating state mean for job %s', job_id)
        sum_Data_Value = 0.0
        count = 0

        for i in range(len(data_ingestor_dict["Question"])):
            if data_ingestor_dict["Question"][i] == question and data_ingestor_dict["LocationDesc"][i] == state:
                if data_ingestor_dict["Data_Value"][i]:
                    sum_Data_Value += float(data_ingestor_dict["Data_Value"][i])
                    count += 1

        mean_value = sum_Data_Value / count if count else 0
        result = {state: mean_value}
        results_dir = 'results'
        file_path = os.path.join(results_dir, f'{job_id}.json')
        with open(file_path, 'w') as f:
            json.dump(result, f)

        webserver_jobs_status[job_id] = 'done'
        logger.info(f'Finished calculating state mean for job %s', job_id)

    def calculate_best5(self, question, job_id, webserver_data_ingestor_dict,
                        webserver_jobs_status, webserver_questions_best_is_min):
        webserver_jobs_status[job_id] = 'running'
        logger.info('Calculating best 5 for job %s', job_id)
        state_media = {}

        for i in range(len(webserver_data_ingestor_dict["Question"])):
            if webserver_data_ingestor_dict["Question"][i] == question:
                if webserver_data_ingestor_dict["LocationDesc"][i] not in state_media:
                    state_media[webserver_data_ingestor_dict["LocationDesc"][i]] = [0.0, 0.0]
                if webserver_data_ingestor_dict["Data_Value"][i]:
                    state_media[webserver_data_ingestor_dict["LocationDesc"][i]][0] += float(
                        webserver_data_ingestor_dict["Data_Value"][i])
                    state_media[webserver_data_ingestor_dict["LocationDesc"][i]][1] += 1

        if question in webserver_questions_best_is_min:
            sorted_states = sorted(state_media.items(), key=lambda x: (x[1][0] / x[1][1]))
        else:
            sorted_states = sorted(state_media.items(), key=lambda x: (x[1][0] / x[1][1]),
                                   reverse=True)
        results = {}
        for i in range(0, 5):
            results[sorted_states[i][0]] = sorted_states[i][1][0] / sorted_states[i][1][1]

        results_dir = 'results'
        file_path = os.path.join(results_dir, f'{job_id}.json')
        with open(file_path, 'w') as f:
            json.dump(results, f)
        webserver_jobs_status[job_id] = 'done'
        logger.info('Finished calculating best 5 for job %s', job_id)

    def calculate_worst5(self, question, job_id, data_ingestor_dict, webserver_jobs_status,
                         webserver_questions_best_is_min):
        webserver_jobs_status[job_id] = 'running'
        logger.info('Calculating worst 5 for job %s', job_id)
        state_media = {}

        for i in range(len(data_ingestor_dict["Question"])):
            if data_ingestor_dict["Question"][i] == question:
                if data_ingestor_dict["LocationDesc"][i] not in state_media:
                    state_media[data_ingestor_dict["LocationDesc"][i]] = [0.0, 0.0]
                if data_ingestor_dict["Data_Value"][i]:
                    state_media[data_ingestor_dict["LocationDesc"][i]][0] += float(
                        data_ingestor_dict["Data_Value"][i])
                    state_media[data_ingestor_dict["LocationDesc"][i]][1] += 1

        if question in webserver_questions_best_is_min:
            sorted_states = sorted(state_media.items(), key=lambda x: (x[1][0] / x[1][1]),
                                   reverse=True)
        else:
            sorted_states = sorted(state_media.items(), key=lambda x: (x[1][0] / x[1][1]))
        results = {}
        for i in range(0, 5):
            results[sorted_states[i][0]] = sorted_states[i][1][0] / sorted_states[i][1][1]

        results_dir = 'results'
        file_path = os.path.join(results_dir, f'{job_id}.json')
        with open(file_path, 'w') as f:
            json.dump(results, f)
        webserver_jobs_status[job_id] = 'done'
        logger.info('Finished calculating worst 5 for job %s', job_id)

    def calculate_global_mean(self, question, job_id, data_ingestor_dict,
                              webserver_jobs_status):
        webserver_jobs_status[job_id] = 'running'
        logger.info('Calculating global mean for job %s', job_id)
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
        file_path = os.path.join(results_dir, f'{job_id}.json')
        with open(file_path, 'w') as f:
            json.dump(result, f)
        webserver_jobs_status[job_id] = 'done'
        logger.info('Finished calculating global mean for job %s', job_id)

    def calculate_diff_from_mean(self, question, job_id, data_ingestor_dict,
                                 webserver_jobs_status):
        webserver_jobs_status[job_id] = 'running'
        logger.info('Calculating diff from mean for job %s', job_id)
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
                    state_media[data_ingestor_dict["LocationDesc"][i]][0] += float(
                        data_ingestor_dict["Data_Value"][i])
                    state_media[data_ingestor_dict["LocationDesc"][i]][1] += 1

        results = {}
        for state in state_media:
            results[state] = global_mean - state_media[state][0] / state_media[state][1]

        results_dir = 'results'
        file_path = os.path.join(results_dir, f'{job_id}.json')
        with open(file_path, 'w') as f:
            json.dump(results, f)
        webserver_jobs_status[job_id] = 'done'
        logger.info('Finished calculating diff from mean for job %s', job_id)

    def calculate_state_diff_from_mean(self, question, state, job_id,
                                       data_ingestor_dict, webserver_jobs_status):
        webserver_jobs_status[job_id] = 'running'
        logger.info('Calculating state diff from mean for job %s', job_id)
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
        file_path = os.path.join(results_dir, f'{job_id}.json')
        with open(file_path, 'w') as f:
            json.dump(result, f)
        webserver_jobs_status[job_id] = 'done'
        logger.info('Finished calculating state diff from mean for job %s', job_id)

    def calculate_mean_by_category(self, question, job_id,
                                   data_ingestor_dict, webserver_jobs_status):
        webserver_jobs_status[job_id] = 'running'
        logger.info('Calculating mean by category for job %s', job_id)
        aggregated_data = {}

        for i in range(len(data_ingestor_dict["Question"])):
            if data_ingestor_dict["Question"][i] == question:
                state = data_ingestor_dict["LocationDesc"][i]
                category = data_ingestor_dict["StratificationCategory1"][i]
                if category:
                    segment = data_ingestor_dict["Stratification1"][i]
                    value = float(data_ingestor_dict["Data_Value"][i]) if data_ingestor_dict["Data_Value"][i] else 0
                    key = (state, category, segment)
                    if key not in aggregated_data:
                        aggregated_data[key] = [0, 0]
                    if value:
                        aggregated_data[key][0] += value
                        aggregated_data[key][1] += 1
        
        results = {}
        for key, (total, count) in aggregated_data.items():
            mean_value = total / count if count else 0
            results[key] = mean_value

        results_dir = 'results'
        file_path = os.path.join(results_dir, f'{job_id}.json')
        with open(file_path, 'w') as f:
            formatted_results = {str(key): value for key, value in results.items()}
            json.dump(formatted_results, f)
        webserver_jobs_status[job_id] = 'done'
        logger.info('Finished calculating mean by category for job %s', job_id)
    

    def calculate_state_mean_by_category(self, question, state, job_id,
                                         data_ingestor_dict, webserver_jobs_status):
        webserver_jobs_status[job_id] = 'running'
        logger.info('Calculating state mean by category for job %s', job_id)
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
        file_path = os.path.join(results_dir, f'{job_id}.json')
        with open(file_path, 'w') as f:
            formatted_results = {str(key): value for key, value in results.items()}
            data_res = {}
            data_res[state] = formatted_results
            json.dump(data_res, f)
        webserver_jobs_status[job_id] = 'done'
        logger.info('Finished calculating state mean by category for job %s', job_id)
    