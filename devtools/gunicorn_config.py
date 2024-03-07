import json
import multiprocessing
import os

workers_per_core_str = os.getenv("APP_WORKERS_PER_CORE", "1")
max_workers_str = os.getenv("APP_MAX_WORKERS")
use_max_workers = None
if max_workers_str:
    use_max_workers = int(max_workers_str)
web_concurrency_str = os.getenv("APP_WEB_CONCURRENCY", None)

host = os.getenv("APP_HOST", "0.0.0.0")
port = os.getenv("PORT", "8000")
bind_env = os.getenv("APP_BIND", None)
use_loglevel = os.getenv("APP_LOG_LEVEL", "INFO")
if bind_env:
    use_bind = bind_env
else:
    use_bind = f"{host}:{port}"

cores = multiprocessing.cpu_count()
workers_per_core = float(workers_per_core_str)
default_web_concurrency = workers_per_core * cores
if web_concurrency_str:
    web_concurrency = int(web_concurrency_str)
    assert web_concurrency > 0
else:
    web_concurrency = max(int(default_web_concurrency), 2)
    if use_max_workers:
        web_concurrency = min(web_concurrency, use_max_workers)
accesslog_var = os.getenv("APP_ACCESS_LOG", "-")
use_accesslog = accesslog_var or None
errorlog_var = os.getenv("APP_ERROR_LOG", "-")
use_errorlog = errorlog_var or None
graceful_timeout_str = os.getenv("APP_GRACEFUL_TIMEOUT", "120")
timeout_str = os.getenv("APP_TIMEOUT", "120")
keepalive_str = os.getenv("APP_KEEP_ALIVE", "5")

# Gunicorn config variables
loglevel = use_loglevel
workers = web_concurrency
bind = use_bind
errorlog = use_errorlog
accesslog = use_accesslog
graceful_timeout = int(graceful_timeout_str)
timeout = int(timeout_str)
keepalive = int(keepalive_str)


# For debugging and testing
log_data = {
    "loglevel": loglevel,
    "workers": workers,
    "bind": bind,
    "graceful_timeout": graceful_timeout,
    "timeout": timeout,
    "keepalive": keepalive,
    "errorlog": errorlog,
    "accesslog": accesslog,
    # Additional, non-gunicorn variables
    "workers_per_core": workers_per_core,
    "use_max_workers": use_max_workers,
    "host": host,
    "port": port,
}
print("Gunicorn Vars: %s" % json.dumps(log_data))