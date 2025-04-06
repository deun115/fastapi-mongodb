from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from db import client

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
