import os
import time
import datetime
import traceback
from contextlib import redirect_stdout, redirect_stderr
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.types import ASGIApp

from db.db import client

class MongoConnectionPoolLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            # lazy connection 방지 
            await client.admin.command("ping")

            # 내부 PyMongo 클라이언트 얻기
            pymongo_client = client.delegate

            # Topology 객체 접근
            topology = pymongo_client._topology

            # 단일 MongoDB 서버 주소 지정
            address = ("localhost", 27017)

            # 해당 주소의 서버 커넥션 풀 접근
            pooled_server = topology.get_server_by_address(address)
            pool = pooled_server.pool

            # 커넥션 풀 상태 추적
            in_use = len(pool.conns)
            max_pool_size = pool.opts._PoolOptions__max_pool_size

            print(f"[Mongo Pool] Address: {address}, In Use: {in_use}, Max: {max_pool_size}")
        except Exception as e:
            print(f"[Mongo Pool] Error accessing connection info: {e}")

        return await call_next(request)


class FullOutputCaptureMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, log_dir: str = "/Users/yang-eunseo/Desktop/projects/mongodb_practice/logs"):
        super().__init__(app)
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)

    async def dispatch(self, request: Request, call_next):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"deploy_{timestamp}.log"
        log_path = os.path.join(self.log_dir, log_filename)

        start_time = time.time()

        try:
            with open(log_path, "w") as log_file, redirect_stdout(log_file), redirect_stderr(log_file):
                print(f"=== {timestamp} | {request.method} {request.url.path} ===")
                response = await call_next(request)
                duration = time.time() - start_time
                print(f"=== completed in {duration:.4f}s | status {response.status_code} ===")

            return response

        except Exception as e:
            with open(log_path, "a") as log_file:
                log_file.write(f"\n=== Exception ===\n")
                traceback.print_exc(file=log_file)

            raise e
