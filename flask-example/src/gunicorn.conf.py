import multiprocessing

from config import config as application_config
app_config = application_config.get('app', {})

bind = [f"{app_config.get('host')}:{app_config.get('port')}"]
backlog = 65534
workers = int(app_config.get('workers', multiprocessing.cpu_count() * 2))
timeout = 300
graceful_timeout = 2
limit_request_field_size = 8192

def when_ready(server):
    from app import app, xxl_handler

    # pylint: disable=import-outside-toplevel,unused-import,no-name-in-module
    xxl_config = application_config.get('xxl', {})

    if xxl_config.get('enabled', False):
        import atexit
        from multiprocessing.util import _exit_function

        from pyxxl import ExecutorConfig, PyxxlRunner

        try:
            atexit.unregister(_exit_function)

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
        except Exception as e:
            print(e)
