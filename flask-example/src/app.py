import os
import time
import logging
import threading

from flask import Flask, jsonify, request
from pyxxl import ExecutorConfig, PyxxlRunner, JobHandler

from config import config
from log import logger_style_handler

is_debug = config.get('app', {}).get('debug', False)
logging.basicConfig(level=logging.DEBUG if is_debug else logging.INFO, handlers=[logger_style_handler])
logger = logging.getLogger('app')

app = Flask(__name__)

xxl_handler = JobHandler()

@app.before_request
def logBeforeRequest():
    app.logger.info(
        "%s [%s] %s %s %s %s",
        request.remote_addr,
        # datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
        request.method,
        request.path,
        request.scheme,
        # response.status,
        # response.content_length,
        request.referrer,
        request.user_agent,
    )

# Get environment variable
API_KEY = os.environ.get("API_KEY", config.get('app', {}).get('api_key', 'default_api_key'))

# Create a metric to track time spent and requests made.
# REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

@app.route('/health', methods=['GET'])
def health_check():
    logger.debug("Health check requested")
    return jsonify({'status': 'ok'})

@app.route('/api/example', methods=['GET'])
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


@xxl_handler.register(name="demoJobHandler")
async def test_task3():
    logging.info("------ [demoJobHandler] executing ------")
    return "Success"
    
def start_xxl_job_executor():
    """
    在一个新的线程中启动XXL-Job执行器
    """
    print("################### XXL-Job Executor started in a background thread start.")
    from multiprocessing import freeze_support
    freeze_support()

    xxl_config = config.get('xxl', {})
    executor_config = ExecutorConfig(
        xxl_admin_baseurl=xxl_config.get('admin', {}).get('baseurl'),
        executor_app_name=xxl_config.get('executor', {}).get('app_name'),
        executor_listen_host=xxl_config.get('executor', {}).get('host'),
        executor_listen_port=xxl_config.get('executor', {}).get('port'),
        access_token=xxl_config.get('access_token'),
        debug=bool(xxl_config.get('debug', False)),
    )
    pyxxl_app = PyxxlRunner(executor_config, handler=xxl_handler)
    app.pyxxl_app = pyxxl_app
    pyxxl_app.run_with_daemon()
    print("################### XXL-Job Executor started in a background thread end.")

if __name__ == '__main__':
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        if config.get('xxl', {}).get('enabled', False):
            start_xxl_job_executor()
    
    app_config = config.get('app', {})
    app.run(
        host=app_config.get('host', '0.0.0.0'),
        port=app_config.get('port', 5000),
        debug=app_config.get('debug', False)
    )
