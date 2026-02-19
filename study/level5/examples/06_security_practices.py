"""
生产级安全实践示例
包含：认证授权、速率限制、输入验证、安全响应头
"""

from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import jwt
from datetime import datetime, timedelta
from typing import Optional
import redis
import hashlib
import secrets
from functools import wraps
import time

# ============================================
# 初始化
# ============================================

app = FastAPI(title="Secure Agent API")

# JWT 配置
SECRET_KEY = secrets.token_urlsafe(32)  # 生产环境从环境变量读取
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 小时

# Redis 连接（用于速率限制）
redis_client = redis.Redis(
    host='localhost',
    port=6379,
    password='your-password',
    db=0,
    decode_responses=True
)

# 安全中间件
security = HTTPBearer()

# ============================================
# CORS 配置
# ============================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],  # 生产环境指定具体域名
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# 受信任的主机
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["your-domain.com", "*.your-domain.com"]
)

# ============================================
# 安全响应头
# ============================================

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """添加安全响应头"""
    response = await call_next(request)

    # 防止点击劫持
    response.headers["X-Frame-Options"] = "DENY"

    # 防止 MIME 类型嗅探
    response.headers["X-Content-Type-Options"] = "nosniff"

    # 启用 XSS 保护
    response.headers["X-XSS-Protection"] = "1; mode=block"

    # 严格传输安全（仅 HTTPS）
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

    # 内容安全策略
    response.headers["Content-Security-Policy"] = "default-src 'self'"

    # 推荐人策略
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    # 权限策略
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

    return response

# ============================================
# JWT 认证
# ============================================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """创建访问令牌"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow()
    })

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """验证令牌"""
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user_id

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ============================================
# 速率限制
# ============================================

class RateLimiter:
    """速率限制器"""

    def __init__(
        self,
        redis_client: redis.Redis,
        max_requests: int = 20,
        window: int = 60
    ):
        self.redis = redis_client
        self.max_requests = max_requests
        self.window = window

    def _get_key(self, identifier: str) -> str:
        """生成 Redis 键"""
        return f"rate_limit:{hashlib.sha256(identifier.encode()).hexdigest()}"

    def check(self, identifier: str) -> bool:
        """检查是否超过限制"""
        key = self._get_key(identifier)

        # 使用 Redis 的 INCR 和 EXPIRE 实现滑动窗口
        current = self.redis.incr(key)

        if current == 1:
            self.redis.expire(key, self.window)

        return current <= self.max_requests

    def get_remaining(self, identifier: str) -> int:
        """获取剩余请求次数"""
        key = self._get_key(identifier)
        current = int(self.redis.get(key) or 0)
        return max(0, self.max_requests - current)


# 创建速率限制器实例
user_rate_limiter = RateLimiter(redis_client, max_requests=20, window=60)
ip_rate_limiter = RateLimiter(redis_client, max_requests=100, window=60)


def check_rate_limit(
    user_id: Optional[str] = None,
    ip_address: Optional[str] = None
):
    """检查速率限制（装饰器）"""

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 检查用户级别限制
            if user_id and not user_rate_limiter.check(user_id):
                raise HTTPException(
                    status_code=429,
                    detail="Rate limit exceeded for user",
                    headers={
                        "Retry-After": str(user_rate_limiter.window),
                        "X-RateLimit-Limit": str(user_rate_limiter.max_requests),
                        "X-RateLimit-Remaining": "0",
                        "X-RateLimit-Reset": str(int(time.time()) + user_rate_limiter.window)
                    }
                )

            # 检查 IP 级别限制
            if ip_address and not ip_rate_limiter.check(ip_address):
                raise HTTPException(
                    status_code=429,
                    detail="Rate limit exceeded for IP",
                    headers={
                        "Retry-After": str(ip_rate_limiter.window),
                        "X-RateLimit-Limit": str(ip_rate_limiter.max_requests),
                        "X-RateLimit-Remaining": "0",
                        "X-RateLimit-Reset": str(int(time.time()) + ip_rate_limiter.window)
                    }
                )

            # 添加速率限制响应头
            response = await func(*args, **kwargs)

            if hasattr(response, 'headers'):
                if user_id:
                    response.headers["X-RateLimit-Limit"] = str(user_rate_limiter.max_requests)
                    response.headers["X-RateLimit-Remaining"] = str(user_rate_limiter.get_remaining(user_id))

            return response

        return wrapper

    return decorator


# ============================================
# 输入验证
# ============================================

from pydantic import BaseModel, Field, validator
import re

class ChatRequest(BaseModel):
    """聊天请求模型"""

    message: str = Field(..., min_length=1, max_length=2000)
    session_id: Optional[str] = Field(None, max_length=100)

    @validator('message')
    def validate_message(cls, v):
        """验证消息内容"""
        # 检查是否包含恶意字符
        dangerous_patterns = [
            r'<script[^>]*>.*?</script>',  # XSS
            r'javascript:',  # JavaScript 伪协议
            r'on\w+\s*=',  # 事件处理器
        ]

        for pattern in dangerous_patterns:
            if re.search(pattern, v, re.IGNORECASE):
                raise ValueError("Message contains dangerous content")

        return v.strip()

    @validator('session_id')
    def validate_session_id(cls, v):
        """验证会话 ID"""
        if v and not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError("Invalid session ID format")

        return v


class OrderRequest(BaseModel):
    """订单请求模型"""

    order_id: str = Field(..., regex=r'^[A-Z0-9]{10,20}$')

# ============================================
# API 路由
# ============================================

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "Secure Agent API",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/auth/login")
async def login(username: str, password: str):
    """登录接口"""
    # 验证用户名和密码（示例）
    if username == "demo" and password == "demo123":
        access_token = create_access_token(
            data={"sub": username},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
    else:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )


@app.post("/chat")
async def chat(
    request: ChatRequest,
    user_id: str = Depends(verify_token),
    http_request: Request = None
):
    """聊天接口"""

    # 获取客户端 IP
    ip_address = http_request.client.host if http_request else None

    # 应用速率限制
    if not user_rate_limiter.check(user_id):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded",
            headers={"Retry-After": str(user_rate_limiter.window)}
        )

    if ip_address and not ip_rate_limiter.check(ip_address):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded",
            headers={"Retry-After": str(ip_rate_limiter.window)}
        )

    # 处理聊天请求
    response = {
        "response": f"Processed: {request.message}",
        "session_id": request.session_id or secrets.token_urlsafe(16)
    }

    return response


@app.post("/orders/{order_id}")
async def get_order(
    order_id: str,
    user_id: str = Depends(verify_token)
):
    """获取订单信息"""

    # 验证订单 ID 格式
    if not re.match(r'^[A-Z0-9]{10,20}$', order_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid order ID format"
        )

    # 返回订单信息
    return {
        "order_id": order_id,
        "status": "shipped",
        "user_id": user_id
    }


# ============================================
# 运行
# ============================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        ssl_keyfile="key.pem",  # SSL 证书
        ssl_certfile="cert.pem"
    )
