from celery import Celery

import __init__


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['http://127.0.0.1:5000'],
        broker=app.config['http://127.0.0.1:5000']
    )
    celery = make_celery(__init__.app)
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery