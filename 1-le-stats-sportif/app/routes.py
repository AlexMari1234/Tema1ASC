from app import webserver
from flask import request, jsonify

import os
import json


@webserver.route('/api/jobs', methods=['GET'])
def get_status_jobs():
    status_jobs = {}
    status_jobs["status"] = "done"
    status_jobs["data"] = []
    for job_id in webserver.jobs_status:
        status_jobs["data"].append({job_id: webserver.jobs_status[job_id]})
    
    return jsonify(status_jobs)

@webserver.route('/api/graceful/shutdown', methods=['GET'])
def graceful_shutdown():
    webserver.tasks_runner.shutdown()
    return jsonify({"status": "done"})

# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        print(f"got data in post {data}")

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)
    else:
        # Method Not Allowed
        return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    # TODO
    # Check if job_id is valid

    # Check if job_id is done and return the result
    #    res = res_for(job_id)
    #    return jsonify({
    #        'status': 'done',
    #        'data': res
    #    })

    if job_id not in webserver.jobs_status:
        return jsonify({"status": "eror", "reason": "Invalid job_id"}), 404

    # Verifică starea job-ului
    if webserver.jobs_status[job_id] == 'done':
        # Încarcă și returnează rezultatul din fișierul corespunzător job_id
        with open(f"results/{job_id}.json", "r") as f:
            result = json.load(f)
        return jsonify({"status": "done", "data": result}), 200
    else:
        # Dacă job-ul este încă în execuție, returnează starea 'running'
        return jsonify({"status": "running"}), 200

@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():

    # TODO
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    dict = webserver.data_ingestor.dict
    data = request.json
    question = data["question"]

    with webserver.lock:
        job_id = f"job_id_{webserver.job_counter}"
        webserver.job_counter += 1

    webserver.tasks_runner.add_task(webserver.endpoints_requests.calculate_states_mean, data, question, job_id, webserver.data_ingestor.dict, webserver.jobs_status)
    webserver.jobs_status[job_id] = 'running'
    
    return jsonify({"job_id": job_id}), 200

def calculate_states_mean(data, question, job_id, webserver_data_ingestor_dict):
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
    
    webserver.jobs_status[job_id] = 'done'


@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    data = request.json
    question = data["question"]
    state = data["state"]

    # Generează un nou job_id
    with webserver.lock:
        job_id = f"job_id_{webserver.job_counter}"
        webserver.job_counter += 1

    # Adaugă job-ul în ThreadPool pentru a fi executat asincron
    webserver.tasks_runner.add_task(webserver.endpoints_requests.calculate_state_mean, data, question, state, job_id, webserver.data_ingestor.dict, webserver.jobs_status)
    
    webserver.jobs_status[job_id] = 'running'
    # Returnează job_id pentru a verifica starea mai târziu
    return jsonify({"job_id": job_id}), 200

def calculate_state_mean(data, question, state, job_id, data_ingestor_dict):
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
    webserver.jobs_status[job_id] = 'done'


@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id
    dict = webserver.data_ingestor.dict
    data = request.json
    question = data["question"]

    with webserver.lock:
        job_id = f"job_id_{webserver.job_counter}"
        webserver.job_counter += 1

    webserver.tasks_runner.add_task(webserver.endpoints_requests.calculate_best5, data, question, job_id, webserver.data_ingestor.dict, webserver.jobs_status, webserver.data_ingestor.questions_best_is_min)
    webserver.jobs_status[job_id] = 'running'

    return jsonify({"job_id": job_id}), 200

def calculate_best5(data, question, job_id, webserver_data_ingestor_dict):
    state_media = {}

    for i in range(len(webserver_data_ingestor_dict["Question"])):
        if webserver_data_ingestor_dict["Question"][i] == question:
            if webserver_data_ingestor_dict["LocationDesc"][i] not in state_media:
                state_media[webserver_data_ingestor_dict["LocationDesc"][i]] = [0.0, 0.0]
            if webserver_data_ingestor_dict["Data_Value"][i]:
                state_media[webserver_data_ingestor_dict["LocationDesc"][i]][0] += float(webserver_data_ingestor_dict["Data_Value"][i])
                state_media[webserver_data_ingestor_dict["LocationDesc"][i]][1] += 1

    if question in webserver.data_ingestor.questions_best_is_min:
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
    
    webserver.jobs_status[job_id] = 'done'

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    dict = webserver.data_ingestor.dict
    data = request.json
    question = data["question"]

    with webserver.lock:
        job_id = f"job_id_{webserver.job_counter}"
        webserver.job_counter += 1

    webserver.tasks_runner.add_task(webserver.endpoints_requests.calculate_worst5, data, question, job_id, webserver.data_ingestor.dict, webserver.jobs_status, webserver.data_ingestor.questions_best_is_min)
    webserver.jobs_status[job_id] = 'running'

    return jsonify({"job_id": job_id}), 200

def calculate_worst5(data, question, job_id, data_ingestor_dict):
    state_media = {}

    for i in range(len(data_ingestor_dict["Question"])):
        if data_ingestor_dict["Question"][i] == question:
            if data_ingestor_dict["LocationDesc"][i] not in state_media:
                state_media[data_ingestor_dict["LocationDesc"][i]] = [0.0, 0.0]
            if data_ingestor_dict["Data_Value"][i]:
                state_media[data_ingestor_dict["LocationDesc"][i]][0] += float(data_ingestor_dict["Data_Value"][i])
                state_media[data_ingestor_dict["LocationDesc"][i]][1] += 1

    if question in webserver.data_ingestor.questions_best_is_min:
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
    
    webserver.jobs_status[job_id] = 'done'

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    dict = webserver.data_ingestor.dict
    data = request.json
    question = data["question"]

    with webserver.lock:
        job_id = f"job_id_{webserver.job_counter}"
        webserver.job_counter += 1

    webserver.tasks_runner.add_task(webserver.endpoints_requests.calculate_global_mean, data, question, job_id, webserver.data_ingestor.dict, webserver.jobs_status)
    webserver.jobs_status[job_id] = 'running'

    return jsonify({"job_id": job_id}), 200

def calculate_global_mean(data, question, job_id, data_ingestor_dict):
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
    
    webserver.jobs_status[job_id] = 'done'

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    dict = webserver.data_ingestor.dict
    data = request.json
    question = data["question"]

    with webserver.lock:
        job_id = f"job_id_{webserver.job_counter}"
        webserver.job_counter += 1

    webserver.tasks_runner.add_task(webserver.endpoints_requests.calculate_diff_from_mean, data, question, job_id, webserver.data_ingestor.dict, webserver.jobs_status)
    webserver.jobs_status[job_id] = 'running'

    return jsonify({"job_id": job_id}), 200

def calculate_diff_from_mean(data, question, job_id, data_ingestor_dict):
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
    
    webserver.jobs_status[job_id] = 'done'    

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id.

    dict = webserver.data_ingestor.dict
    data = request.json
    question = data["question"]
    state = data["state"]

    with webserver.lock:
        job_id = f"job_id_{webserver.job_counter}"
        webserver.job_counter += 1

    webserver.tasks_runner.add_task(webserver.endpoints_requests.calculate_state_diff_from_mean, data, question, state, job_id, webserver.data_ingestor.dict, webserver.jobs_status)
    webserver.jobs_status[job_id] = 'running'

    return jsonify({"job_id": job_id}), 200

def calculate_state_diff_from_mean(data, question, state, job_id, data_ingestor_dict):
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
    
    webserver.jobs_status[job_id] = 'done'

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    data = request.json
    question = data["question"]

    with webserver.lock:
        job_id = f"job_id_{webserver.job_counter}"
        webserver.job_counter += 1

    webserver.tasks_runner.add_task(webserver.endpoints_requests.calculate_mean_by_category, data, question, job_id, webserver.data_ingestor.dict, webserver.jobs_status)
    webserver.jobs_status[job_id] = 'running'

    return jsonify({"job_id": job_id}), 200

def calculate_mean_by_category(data, question, job_id, data_ingestor_dict):
    
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
    
    webserver.jobs_status[job_id] = 'done'

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    data = request.json
    question = data["question"]
    state = data["state"]

    with webserver.lock:
        job_id = f"job_id_{webserver.job_counter}"
        webserver.job_counter += 1

    webserver.tasks_runner.add_task(webserver.endpoints_requests.calculate_state_mean_by_category, data, question, state, job_id, webserver.data_ingestor.dict, webserver.jobs_status)
    webserver.jobs_status[job_id] = 'running'

    return jsonify({"job_id": job_id}), 200


def calculate_state_mean_by_category(data, question, state, job_id, data_ingestor_dict):
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
    
    webserver.jobs_status[job_id] = 'done'

# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    routes = get_defined_routes()
    msg = f"Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg

def get_defined_routes():
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes


