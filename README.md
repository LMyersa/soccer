# Soccer

## Adding Celery
To schedule tasks, you need celery to create tasks,
and Celery Beat to schedule these tasks.\
Follow these steps

1. Install Celery with whatever backend of your choice,
I am using Redis, so I installed with `pip install "celery[redis]"`
2. Add a `celery.py` file in your project directory as I've done
3. Add an import from `celery.py` in your `__init__.py` for discovery
4. Add configurations in `settings.py`
5. Create a `tasks.py` file in any directory and decorate every task with 
`@app.task` and it will get discovered
6. Add tasks you want to schedule in `settings.py`
7. Run your Celery worker with `celery -A Soccer worker -l info`, but in your
case, you have threads in your tasks so you will need some extra args and end up
using this `celery -A Soccer worker --concurrency=1 --pool=threads -l info`
8. Run Celery Beat to turn on task scheduling with 
`celery -A Soccer beat -l info`
