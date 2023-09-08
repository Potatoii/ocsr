import json
from typing import List

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import Message

from commons.log_utils import logger
from commons.schemas import Result


class BaseRequest(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        done = False
        chunks: List[bytes] = []
        receive = request.receive

        async def wrapped_receive() -> Message:  # 取body
            nonlocal done
            message = await receive()
            if message["type"] == "http.disconnect":
                done = True
                return message
            origin_body = message.get("body", b"")
            more_body = message.get("more_body", False)
            if not more_body:
                done = True
            chunks.append(origin_body)
            return message
        try:
            # 在请求之前打印日志
            logger.info(f"Request received: {request.method} {request.url.path}")
            request._receive = wrapped_receive
            response = await call_next(request)
            if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
                if "auth" not in request.url.path and "user" not in request.url.path:
                    if not done:
                        await wrapped_receive()
                    content_type = request.headers.get("Content-Type")
                    if content_type and "application/json" in content_type:
                        body = b"".join(chunks)
                        logger.info(f"Request body: {body}")
                    else:
                        logger.info(f"Request not json body. Content-Type: {content_type}")
            # 在请求完成后打印日志
            logger.info(f"Response sent: {response.status_code}")
            return response
        except Exception as e:
            if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
                if "auth" not in request.url.path and "user" not in request.url.path:
                    if not done:
                        await wrapped_receive()
                    body = b"".join(chunks)
                    logger.info(f"Request body: {body}")
            # 没有手动抛出异常，返回固定错误消息
            logger.exception(f"Exception occurred during request handling, {e}")
            error_message = Result(code=-1, msg="Exception occurred during request handling")
            response = Response(
                content=json.dumps(error_message.dict()),
                media_type="application/json",
                status_code=500
            )
            return response
