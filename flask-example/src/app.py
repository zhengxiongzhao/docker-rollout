import os
import time
import logging
import threading

from flask import Flask, jsonify, request

from pyxxl import ExecutorConfig, PyxxlRunner, JobHandler

from prometheus_client import generate_latest, CollectorRegistry, Gauge
from prometheus_client import Summary

app = Flask(__name__)

xxl_handler = JobHandler()

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Get environment variable
API_KEY = os.environ.get("API_KEY", "default_api_key")


# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

@app.route('/health', methods=['GET'])
def health_check():
    logger.debug("Health check requested")
    return jsonify({'status': 'ok'})

@app.route('/api/example', methods=['GET'])
@REQUEST_TIME.time()
def example_api():
    logger.info("Example API requested")
    return jsonify({'message': f'This is an example API endpoint. API_KEY: {API_KEY}'})

@app.route('/xxl-job-callback', methods=['POST'])
def xxl_job_callback():
    data = request.get_json()
    logger.info(f"XXL-Job callback received: {data}")
    # Process the job execution result here
    return jsonify({'status': 'success', 'message': 'Job executed successfully'})

@app.route('/metrics')
def metrics():
    reg = CollectorRegistry()
    g = Gauge('python_gc_objects_collected', 'Objects collected during gc', registry=reg)
    g.collect()
    data = generate_latest(reg)
    return data, 200, {'Content-Type': 'text/plain; charset=utf-8'}


@xxl_handler.register(name="demo_job_handler")
async def test_task3():
    logging.info("------ [demo_job_handler] executing ------")
    return "Success"
    

def start_xxl_job_executor():
    """
    在一个新的线程中启动XXL-Job执行器
    """
    print("XXL-Job Executor started in a background thread start.")
    from multiprocessing import freeze_support
    freeze_support()

    config = ExecutorConfig(
        xxl_admin_baseurl="http://192.168.204.56:7070/xxl-job-admin/api/",
        executor_app_name="flask-xxl-executor",
        executor_listen_host="0.0.0.0",
        executor_listen_port=9999,
        access_token='default_token',
        debug=True,
    )
    pyxxl_app = PyxxlRunner(config, handler=xxl_handler)
    app.pyxxl_app = pyxxl_app
    pyxxl_app.run_with_daemon()
    print("XXL-Job Executor started in a background thread end.")

if __name__ == '__main__':
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        start_xxl_job_executor()
    app.run(debug=False, host='0.0.0.0', port=5000)
