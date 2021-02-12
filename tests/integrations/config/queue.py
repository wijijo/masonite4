DRIVERS = {
    "default": "async",
    "database": {
        "connection": "sqlite",
        "table": "jobs",
        "failed_table": "failed_jobs",
        "attempts": 3,
        "poll": 5,
    },
    "redis": {
        #
    },
    "amqp": {
        "username": "guest",
        "password": "guest",
        "port": "5672",
        "vhost": "",
        "host": "localhost",
        "channel": "default",
        "queue": "masonite4",
    },
    "async": {"blocking": True},
}
