# colobridge-test-task
Test task for Python engeneer position in Colobridge

## How to run
1. Create venv with python (3.13 in my case)
2. Install requirements
3. Setup broker for celery, setup aws, setup postgres and make migration
4. Fill env with `.env.example` example
5. `celery -A celery_app worker --loglevel=INFO`
6. `uvicorn app:app`
