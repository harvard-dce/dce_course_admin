from getenv import env
import dotenv
dotenv.read_dotenv()

workers = env('GUNICORN_WORKERS', 4)
timeout = env('GUNICORN_TIMEOUT', 60)
