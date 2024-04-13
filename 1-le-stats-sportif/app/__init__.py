import os
from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool
from threading import Lock
from app.endpoints_methods import SolveEndpoint
from app.logger import AppLogger

os.system("rm -rf results/*")
os.system("rm -rf webserver.log")
logger = AppLogger.get_logger("webserver.log")
webserver = Flask(__name__)
webserver.tasks_runner = ThreadPool()

webserver.jobs_status = {}
webserver.endpoints_requests = SolveEndpoint()
webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")

webserver.job_counter = 1
webserver.lock = Lock()

from app import routes