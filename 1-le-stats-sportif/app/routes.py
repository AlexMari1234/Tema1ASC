import json
from flask import request, jsonify
from app import webserver
from app.logger import AppLogger

logger = AppLogger.get_logger("webserver.log")

@webserver.route('/api/jobs', methods=['GET'])
def get_status_jobs():
    """Returnează starea curentă a tuturor joburilor."""
    logger.info("Am intrat in get_status_jobs")

    status_jobs = {"status": "done", "data": []}
    for job_id, status in webserver.jobs_status.items():
        status_jobs["data"].append({job_id: status})

    logger.info("Am iesit din get_status_jobs")
    return jsonify(status_jobs)

@webserver.route('/api/graceful/shutdown', methods=['GET'])
def graceful_shutdown():
    """Inițiază o oprire ordonată a serverului."""
    logger.info("Am intrat in graceful_shutdown")
    webserver.tasks_runner.shutdown()
    logger.info("Am iesit din graceful_shutdown")
    return jsonify({"status": "done"}), 200

@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    """Procesează și răspunde la cereri POST cu date JSON."""
    if request.method == 'POST':
        data = request.json
        response = {"message": "Received data successfully", "data": data}
        return jsonify(response)
    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    """Returnează rezultatele pentru un job specificat prin ID."""
    logger.info(f"Am intrat în get_results pentru job_id {job_id}")

    if job_id not in webserver.jobs_status:
        logger.error(f"Eroare: job_id invalid {job_id}")
        return jsonify({"status": "error", "reason": "Invalid job_id"}), 404

    if webserver.jobs_status[job_id] == 'done':
        with open(f"results/{job_id}.json", "r", encoding='utf-8') as f:
            result = json.load(f)
        logger.info(f"Am ieșit cu succes din get_results pentru job_id {job_id}")
        return jsonify({"status": "done", "data": result}), 200

    logger.info(f"Job-ul {job_id} este încă în execuție")
    return jsonify({"status": "running"}), 200

@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    """Handles requests to calculate the mean of states based on given criteria."""
    logger.info("Am intrat în states_mean_request pentru job_id %s", webserver.job_counter)

    data_dict = webserver.data_ingestor.dict
    data = request.json
    question = data["question"]

    with webserver.lock:
        job_id = f"job_id_{webserver.job_counter}"
        webserver.job_counter += 1

    webserver.tasks_runner.add_task(webserver.endpoints_requests.calculate_states_mean,
                                    question,job_id, data_dict, webserver.jobs_status)
    webserver.jobs_status[job_id] = 'running'

    logger.info("Am ieșit din states_mean_request pentru job_id %s", job_id)
    return jsonify({"job_id": job_id}), 200

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    """Calculates the mean for a specific state based on given data."""
    logger.info("Am intrat în state_mean_request pentru job_id %s", webserver.job_counter)
    data = request.json
    question = data["question"]
    state = data["state"]

    with webserver.lock:
        job_id = f"job_id_{webserver.job_counter}"
        webserver.job_counter += 1

    webserver.tasks_runner.add_task(webserver.endpoints_requests.calculate_state_mean,
                                    question, state, job_id, webserver.data_ingestor.dict,
                                    webserver.jobs_status)
    webserver.jobs_status[job_id] = 'running'

    logger.info("Am ieșit din state_mean_request pentru job_id %s", job_id)
    return jsonify({"job_id": job_id}), 200

@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    """Requests calculation of the top 5 best results for a given question."""
    logger.info("Am intrat în best5_request pentru job_id %s", webserver.job_counter)
    data_dict = webserver.data_ingestor.dict
    data = request.json
    question = data["question"]

    with webserver.lock:
        job_id = f"job_id_{webserver.job_counter}"
        webserver.job_counter += 1

    webserver.tasks_runner.add_task(webserver.endpoints_requests.calculate_best5,
                                    question, job_id, data_dict, webserver.jobs_status,
                                    webserver.data_ingestor.questions_best_is_min)
    webserver.jobs_status[job_id] = 'running'

    logger.info("Am ieșit din best5_request pentru job_id %s", job_id)
    return jsonify({"job_id": job_id}), 200

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    """Requests calculation of the top 5 worst results for a given question."""
    logger.info("Am intrat în worst5_request pentru job_id %s", webserver.job_counter)
    data_dict = webserver.data_ingestor.dict
    data = request.json
    question = data["question"]

    with webserver.lock:
        job_id = f"job_id_{webserver.job_counter}"
        webserver.job_counter += 1

    webserver.tasks_runner.add_task(webserver.endpoints_requests.calculate_worst5,
                                    question, job_id, data_dict, webserver.jobs_status,
                                    webserver.data_ingestor.questions_best_is_min)
    webserver.jobs_status[job_id] = 'running'

    logger.info("Am ieșit din worst5_request pentru job_id %s", job_id)
    return jsonify({"job_id": job_id}), 200


@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    """Calculate the global mean for a given question."""
    logger.info("Am intrat in global_mean_request pentru job_id %s", webserver.job_counter)
    data = request.json
    question = data["question"]
    with webserver.lock:
        job_id = f"job_id_{webserver.job_counter}"
        webserver.job_counter += 1
    webserver.tasks_runner.add_task(webserver.endpoints_requests.calculate_global_mean,
                                    question, job_id, webserver.data_ingestor.dict,
                                    webserver.jobs_status)
    webserver.jobs_status[job_id] = 'running'
    logger.info("Am iesit din global_mean_request pentru job_id %s", job_id)
    return jsonify({"job_id": job_id}), 200

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    """Calculate the difference from the mean for a given question."""
    logger.info("Am intrat in diff_from_mean_request pentru job_id %s", webserver.job_counter)
    data = request.json
    question = data["question"]
    with webserver.lock:
        job_id = f"job_id_{webserver.job_counter}"
        webserver.job_counter += 1
    webserver.tasks_runner.add_task(webserver.endpoints_requests.calculate_diff_from_mean,
                                    question, job_id, webserver.data_ingestor.dict,
                                    webserver.jobs_status)
    webserver.jobs_status[job_id] = 'running'
    logger.info("Am iesit din diff_from_mean_request pentru job_id %s", job_id)
    return jsonify({"job_id": job_id}), 200

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    """Calculate the state-specific difference from the mean for a given question."""
    logger.info("Am intrat in state_diff_from_mean_request pentru job_id %s", webserver.job_counter)
    data = request.json
    question = data["question"]
    state = data["state"]
    with webserver.lock:
        job_id = f"job_id_{webserver.job_counter}"
        webserver.job_counter += 1
    webserver.tasks_runner.add_task(webserver.endpoints_requests.calculate_state_diff_from_mean,
                                    question, state, job_id, webserver.data_ingestor.dict,
                                    webserver.jobs_status)
    webserver.jobs_status[job_id] = 'running'
    logger.info("Am iesit din state_diff_from_mean_request pentru job_id %s", job_id)
    return jsonify({"job_id": job_id}), 200

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    """Calculate the mean by category for a given question."""
    logger.info("Am intrat in mean_by_category_request pentru job_id %s", webserver.job_counter)
    data = request.json
    question = data["question"]
    with webserver.lock:
        job_id = f"job_id_{webserver.job_counter}"
        webserver.job_counter += 1
    webserver.tasks_runner.add_task(webserver.endpoints_requests.calculate_mean_by_category,
                                    question, job_id, webserver.data_ingestor.dict,
                                    webserver.jobs_status)
    webserver.jobs_status[job_id] = 'running'
    logger.info("Am iesit din mean_by_category_request pentru job_id %s", job_id)
    return jsonify({"job_id": job_id}), 200

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    """Calculate the mean for a specific state and category for a given question."""
    logger.info("Am intrat in state_mean_by_category_request pentru job_id %s",
                webserver.job_counter)
    data = request.json
    question = data["question"]
    state = data["state"]
    with webserver.lock:
        job_id = f"job_id_{webserver.job_counter}"
        webserver.job_counter += 1
    webserver.tasks_runner.add_task(webserver.endpoints_requests.calculate_state_mean_by_category,
                                    question, state, job_id, webserver.data_ingestor.dict,
                                    webserver.jobs_status)
    webserver.jobs_status[job_id] = 'running'
    logger.info("Am iesit din state_mean_by_category_request pentru job_id %s", job_id)
    return jsonify({"job_id": job_id}), 200

@webserver.route('/')
@webserver.route('/index')
def index():
    """Display the available routes in a formatted manner on the index page."""
    routes = get_defined_routes()
    msg = "Hello, World!\nInteract with the webserver using one of the defined routes:\n"
    paragraphs = "".join(f"<p>{route}</p>" for route in routes)
    msg += paragraphs
    return msg

def get_defined_routes():
    """Retrieve and format the defined routes for display."""
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")

    return routes