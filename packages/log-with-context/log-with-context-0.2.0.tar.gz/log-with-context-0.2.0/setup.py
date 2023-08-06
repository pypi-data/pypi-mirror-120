# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['log_with_context']
setup_kwargs = {
    'name': 'log-with-context',
    'version': '0.2.0',
    'description': 'a thread-local, context-preserving Python logger',
    'long_description': 'log-with-context--a thread-local, context-preserving Python logger\n==================================================================\n\n``log-with-context`` is a Python logger that saves variables in a\nthread-local context to be passed as `extra` to Python\n`logging <https://docs.python.org/3/library/logging.html>`_ methods.\n\nInstallation\n------------\n\nThis library is available on PyPI and can be installed with\n\n.. code:: bash\n\n    python3 -m pip install log-with-context\n\nUsage\n-----\n\nThis library provides a wrapped Python logging.Logger that\nadds a shared context to each logging message, passed as\nthe `extra` parameter.\n\n**You will need an additional library** (like\n`JSON-log-formatter <https://pypi.org/project/JSON-log-formatter/>`_)\n**to actually output the logging messages**. We avoided putting this\nfunctionality in this library to keep it lightweight and flexible.\nWe assumed that you already have a preferred way to format your\nlogging messages.\n\n.. code:: python\n\n    import logging\n    import logging.config\n\n    from log_with_context import add_logging_context, Logger\n\n    logging.config.dictConfig({\n        "version": 1,\n        "disable_existing_loggers": True,\n        "formatters": {\n            "json": {"()": "json_log_formatter.JSONFormatter"},\n        },\n        "handlers": {\n            "console": {\n                "formatter": "json",\n                "class": "logging.StreamHandler",\n            }\n        },\n        "loggers": {\n            "": {"handlers": ["console"], "level": "INFO"},\n        },\n    })\n\n    LOGGER = Logger(__name__)\n\n    LOGGER.info("First message. No context")\n\n    with add_logging_context(current_request="hi"):\n        LOGGER.info("Level 1")\n\n        with add_logging_context(more_info="this"):\n            LOGGER.warning("Level 2")\n\n        LOGGER.info("Back to level 1")\n\n    LOGGER.error("No context at all...")\n\n\nThe above program logs the following messages to standard error:\n\n.. code:: json\n\n    {"message": "First message. No context", "time": "2021-04-08T16:37:23.126099"}\n    {"current_request": "hi", "message": "Level 1", "time": "2021-04-08T16:37:23.126336"}\n    {"current_request": "hi", "more_info": "this", "message": "Level 2", "time": "2021-04-08T16:37:23.126389"}\n    {"current_request": "hi", "message": "Back to level 1", "time": "2021-04-08T16:37:23.126457"}\n    {"message": "No context at all...", "time": "2021-04-08T16:37:23.126514"}\n\n\nThis example may look trivial, but it is very handy to maintain a\nlogging context up and down a Python call stack without having\nto pass additional variables to the functions and methods\nthat you call.\n\nImplementation details\n----------------------\nLogging contexts are stored as thread-local variables. If you want\nto share information between threads, you must create a Logging\ncontext in each thread with the same information.\n\nSimilarly, logging contexts are *deliberately not copied* when\ncreating subprocesses. This is done to minimize bugs and make sure\nthat log-with-context behaves in the exact same manner across\noperating systems.\n',
    'author': 'Neocrym Records Inc.',
    'author_email': 'engineering@neocrym.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/neocrym/log-with-context',
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
