import sys
import os
import traceback
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI()

try:
    from app.main import app as real_app
    app = real_app
except Exception as e:
    err_msg = traceback.format_exc()
    @app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE"])
    def catch_all(path_name: str):
        return PlainTextResponse(err_msg, status_code=500)
