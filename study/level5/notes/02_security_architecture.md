# 02 安全架构

> **主题**: 设计生产级系统的安全架构
> **时间**: 45 分钟
> **难度**: ⭐⭐⭐⭐

---

## 学习目标

完成本笔记后，你将能够：

1. 理解安全架构的核心原则
2. 掌握纵深防御策略
3. 能够设计安全架构
4. 理解常见安全威胁和防护措施

---

## 核心概念

### 安全架构原则

#### 1. 纵深防御（Defense in Depth）

**定义**: 多层安全控制，即使一层失效，其他层仍能提供保护。

```
┌─────────────────────────────────────────────┐
│           第一层：网络安全                  │
│  - VPC, Security Groups, Firewall, WAF     │
├─────────────────────────────────────────────┤
│           第二层：边界安全                  │
│  - API Gateway, 负载均衡, DDoS 防护        │
├─────────────────────────────────────────────┤
│           第三层：应用安全                  │
│  - 认证授权, 输入验证, 速率限制            │
├─────────────────────────────────────────────┤
│           第四层：数据安全                  │
│  - 加密存储, 传输加密, 密钥管理            │
├─────────────────────────────────────────────┤
│           第五层：运行时安全                │
│  - 容器安全, 进程隔离, 资源限制            │
└─────────────────────────────────────────────┘
```

#### 2. 最小权限原则

**定义**: 用户和组件只拥有完成任务所需的最小权限。

**示例**:
```python
# ❌ 不好的做法
@app.get("/admin/users/{user_id}")
def delete_user(user_id: str):
    # 任何用户都能删除用户
    return delete_user_from_db(user_id)

# ✅ 好的做法
@app.get("/admin/users/{user_id}")
def delete_user(
    user_id: str,
    current_user: User = Depends(require_admin)  # 必须是管理员
):
    # 只有管理员能删除用户
    return delete_user_from_db(user_id)
```

#### 3. 默认拒绝

**定义**: 除非明确允许，否则拒绝所有访问。

**示例**:
```python
# ✅ 默认拒绝所有访问
ALLOWED_ORIGINS = ["https://your-domain.com"]

@app.middleware("cors")
async def cors_middleware(request, call_next):
    origin = request.headers.get("origin")
    if origin in ALLOWED_ORIGINS:
        # 允许特定来源
        response = await call_next(request)
        response.headers["Access-Control-Allow-Origin"] = origin
        return response
    else:
        # 拒绝其他所有来源
        return JSONResponse(
            status_code=403,
            content={"detail": "Origin not allowed"}
        )
```

#### 4. 职责分离

**定义**: 将敏感操作分离到不同的组件中，防止单点妥协。

**示例**:
```
用户认证服务 ────────> 验证身份
                        │
资源授权服务 ──────────┤
                        │
业务逻辑服务 ──────────┘

每个服务独立部署，单独保护
```

---

### 安全威胁模型

#### STRIDE 威胁分类

| 威胁类型 | 描述 | 示例 | 防护措施 |
|---------|------|------|----------|
| **Spoofing（欺骗）** | 伪装成合法用户 | 使用被盗Token | 强认证，多因素认证 |
| **Tampering（篡改）** | 修改数据或代码 | 中间人攻击 | 加密传输，签名验证 |
| **Repudiation（抵赖）** | 否认操作 | 用户否认下单 | 完整审计日志 |
| **Information Disclosure（信息泄露）** | 暴露敏感信息 | API返回密码 | 数据脱敏，加密 |
| **Denial of Service（拒绝服务）** | 耗尽系统资源 | DDoS攻击 | 速率限制，限流 |
| **Elevation of Privilege（权限提升）** | 获得更高权限 | 普通用户变管理员 | 最小权限，定期审计 |

---

### 安全架构层次

#### 1. 网络安全层

**组件**:
- **VPC (Virtual Private Cloud)**: 隔离的网络环境
- **Security Groups**: 虚拟防火墙，控制入站/出站流量
- **Network ACLs**: 子网级别的访问控制
- **WAF (Web Application Firewall)**: 过滤恶意流量
- **DDoS Protection**: 防护分布式拒绝服务攻击

**配置示例**:
```yaml
# Security Group 配置
Inbound Rules:
  - Type: HTTP
    Source: 0.0.0.0/0
    Port: 80

  - Type: HTTPS
    Source: 0.0.0.0/0
    Port: 443

  - Type: Custom (Agent API)
    Source: VPC CIDR (仅内部)
    Port: 8000

Outbound Rules:
  - Type: All Traffic
    Destination: 0.0.0.0/0
```

#### 2. 边界安全层

**组件**:
- **API Gateway**: 统一入口，认证授权
- **Load Balancer**: 分发流量，隔离故障
- **CDN**: 内容分发，防护 DDoS
- **Reverse Proxy**: 隐藏后端架构

**安全配置**:
```yaml
# Nginx 反向代理安全配置
server {
    listen 443 ssl http2;
    server_name api.example.com;

    # SSL 配置
    ssl_certificate /etc/ssl/certs/cert.pem;
    ssl_certificate_key /etc/ssl/private/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # 安全头
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000" always;

    # 速率限制
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req zone=api burst=20;

    location / {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### 3. 应用安全层

**认证机制**:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from datetime import datetime, timedelta

security = HTTPBearer()
SECRET_KEY = "your-secret-key"  # 从环境变量读取
ALGORITHM = "HS256"

def create_access_token(user_id: str, scopes: list[str]) -> str:
    """创建访问令牌"""
    payload = {
        "sub": user_id,
        "scopes": scopes,
        "exp": datetime.utcnow() + timedelta(minutes=30),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    required_scopes: list[str] = None
) -> dict:
    """验证令牌和权限"""
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        token_scopes = payload.get("scopes", [])

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        # 检查权限范围
        if required_scopes:
            for scope in required_scopes:
                if scope not in token_scopes:
                    raise HTTPException(
                        status_code=403,
                        detail=f"Missing required scope: {scope}"
                    )

        return {"user_id": user_id, "scopes": token_scopes}

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# 使用
@app.post("/admin/users")
async def create_user(
    user_data: UserCreate,
    auth: dict = Depends(verify_token)
):
    # 需要admin权限
    if "admin" not in auth["scopes"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    ...
```

**授权模型**:

```python
from enum import Enum
from pydantic import BaseModel

class Permission(str, Enum):
    """权限枚举"""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"

class Role(BaseModel):
    """角色定义"""
    name: str
    permissions: list[Permission]

# 预定义角色
ROLES = {
    "user": Role(name="user", permissions=[Permission.READ]),
    "editor": Role(name="editor", permissions=[Permission.READ, Permission.WRITE]),
    "admin": Role(name="admin", permissions=[Permission.READ, Permission.WRITE, Permission.DELETE, Permission.ADMIN]),
}

class AuthorizationChecker:
    """权限检查器"""

    def __init__(self, required_permission: Permission):
        self.required_permission = required_permission

    def __call__(self, current_user: User = Depends(get_current_user)):
        user_role = ROLES.get(current_user.role)

        if not user_role:
            raise HTTPException(status_code=403, detail="Invalid role")

        if self.required_permission not in user_role.permissions:
            raise HTTPException(
                status_code=403,
                detail=f"Permission required: {self.required_permission}"
            )

        return current_user

# 使用
@app.get("/resources/{resource_id}")
async def get_resource(
    resource_id: str,
    user: User = Depends(AuthorizationChecker(Permission.READ))
):
    # 只有有 READ 权限的用户才能访问
    ...

@app.delete("/resources/{resource_id}")
async def delete_resource(
    resource_id: str,
    user: User = Depends(AuthorizationChecker(Permission.DELETE))
):
    # 只有有 DELETE 权限的用户才能访问
    ...
```

**输入验证**:

```python
from pydantic import BaseModel, Field, validator
import re
import html

class SafeString(str):
    """安全字符串，自动转义"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')

        # HTML 转义
        v = html.escape(v)

        # 检查危险模式
        dangerous_patterns = [
            r'<script[^>]*>.*?</script>',  # XSS
            r'javascript:',                  # JavaScript 伪协议
            r'on\w+\s*=',                   # 事件处理器
            r'<\?php',                      # PHP 标签
        ]

        for pattern in dangerous_patterns:
            if re.search(pattern, v, re.IGNORECASE):
                raise ValueError('Input contains dangerous content')

        return cls(v)

class AgentRequest(BaseModel):
    """Agent 请求验证"""
    message: SafeString = Field(..., min_length=1, max_length=5000)
    user_id: str = Field(..., regex=r'^[a-zA-Z0-9_-]{1,50}$')

    @validator('message')
    def validate_message(cls, v):
        """验证消息内容"""
        # 检查是否包含 SQL 注入模式
        sql_injection_patterns = [
            r"(\bunion\b.*\bselect\b)",
            r"(\bor\b.*=)",
            r"(\band\b.*=)",
            r"(\bdrop\b.*\btable\b)",
        ]

        for pattern in sql_injection_patterns:
            if re.search(pattern, v, re.IGNORECASE):
                raise ValueError('Invalid input detected')

        return v
```

#### 4. 数据安全层

**加密存储**:

```python
from cryptography.fernet import Fernet
import os

# 生成密钥（只生成一次）
# key = Fernet.generate_key()
# 保存到环境变量或密钥管理服务

class EncryptionService:
    """加密服务"""

    def __init__(self):
        key = os.environ.get("ENCRYPTION_KEY")
        if not key:
            raise ValueError("ENCRYPTION_KEY not set")
        self.cipher = Fernet(key.encode())

    def encrypt(self, data: str) -> str:
        """加密数据"""
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data: str) -> str:
        """解密数据"""
        return self.cipher.decrypt(encrypted_data.encode()).decode()

# 使用
encryption = EncryptionService()

# 存储敏感数据
encrypted_api_key = encryption.encrypt("sk-xxxxx")
# 保存到数据库
db.execute("INSERT INTO api_keys (key) VALUES (?)", (encrypted_api_key,))

# 读取敏感数据
row = db.execute("SELECT key FROM api_keys WHERE id = ?", (key_id,)).fetchone()
api_key = encryption.decrypt(row['key'])
```

**传输加密**:

```python
# FastAPI 配置 HTTPS
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=443,
        ssl_keyfile="/path/to/key.pem",
        ssl_certfile="/path/to/cert.pem"
    )
```

#### 5. 运行时安全

**容器安全**:

```dockerfile
# 使用非 root 用户
FROM python:3.11-slim

# 创建专用用户
RUN groupadd -r appuser && useradd -r -g appuser appuser

# 设置工作目录
WORKDIR /app

# 复制代码并设置权限
COPY --chown=appuser:appuser . .

# 切换到非 root 用户
USER appuser

# 限制资源
HEALTHCHECK --interval=30s CMD curl -f http://localhost:8000/health || exit 1

# 只暴露必要端口
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Kubernetes 安全上下文**:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-agent
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 1000
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: agent
    image: agent:latest
    securityContext:
      allowPrivilegeEscalation: false
      capabilities:
        drop:
        - ALL
      readOnlyRootFilesystem: true
    volumeMounts:
    - name: tmp
      mountPath: /tmp
    - name: cache
      mountPath: /app/cache
  volumes:
  - name: tmp
    emptyDir: {}
  - name: cache
    emptyDir: {}
```

---

## 费曼解释

### 用简单的语言解释

**问题**: 什么是纵深防御？

**类比**: 想象保护一个金库：

**第一道防线（网络安全）**: 金库大门
- 厚重的铁门，只有授权人员有钥匙
- 类似：防火墙只允许合法流量进入

**第二道防线（边界安全）**: 安保人员
- 检查进入人员的工作证
- 类似：API Gateway 验证 Token

**第三道防线（应用安全）**: 金库内部规定
- 不同级别人员只能进入对应区域
- 类似：用户只能访问自己的数据

**第四道防线（数据安全）**: 保险箱
- 即使进入金库，还有保险箱保护
- 类似：敏感数据加密存储

**核心**: 纵深防御就像多层锁，即使坏人突破了一层，还有其他层保护。不要只依赖单一的安全措施。

---

## 最小验证

### 任务 1: 安全威胁分析

分析一个 Agent 系统的安全威胁，填写下表：

| 威胁类型 | 可能的攻击 | 防护措施 |
|---------|-----------|----------|
| Spoofing |  |  |
| Tampering |  |  |
| Repudiation |  |  |
| Information Disclosure |  |  |
| Denial of Service |  |  |
| Elevation of Privilege |  |  |

**预期产出**: 威胁分析文档

### 任务 2: 实现认证授权

实现一个简单的 JWT 认证系统：

```python
# requirements
# - fastapi
# - python-jose[cryptography]
# - passlib[bcrypt]

# 任务：
# 1. 创建登录接口，生成 JWT Token
# 2. 创建需要认证的接口
# 3. 实现基于角色的权限控制
```

**验证**: 测试认证流程

### 任务 3: 添加安全头

为 FastAPI 应用添加所有安全响应头：

```python
# 添加这些安全头：
# - X-Frame-Options
# - X-Content-Type-Options
# - X-XSS-Protection
# - Strict-Transport-Security
# - Content-Security-Policy
# - Referrer-Policy
```

**验证**: 使用 curl 或浏览器检查响应头

---

## 常见问题

### Q1: 如何存储密钥？

**A**:
- **开发环境**: 使用 .env 文件（不提交到 Git）
- **生产环境**: 使用密钥管理服务（AWS Secrets Manager、HashiCorp Vault）
- **绝不要**: 硬编码在代码中

### Q2: HTTPS 必须的吗？

**A**:
- **生产环境**: 必须使用 HTTPS
- **开发环境**: 可以使用 HTTP，但建议配置自签名证书
- **工具**: Let's Encrypt 提供免费证书

### Q3: 如何防止 API 滥用？

**A**:
1. **速率限制**: 每用户/IP 的请求次数限制
2. **配额**: 总资源使用限制
3. **认证**: 要求 API Key 或 Token
4. **监控**: 检测异常流量模式

---

## Agent/Skill/Tool 沙盒隔离架构（生产必备）

对于会执行脚本、命令、文件操作的 Agent，沙盒不是可选项，而是安全基线。

### 最小落地要求

1. **执行环境隔离**
- 使用容器或独立运行时承载 Tool/Skill 执行
- 业务服务与执行环境分离部署

2. **最小权限**
- 容器默认非 root 用户运行
- 文件系统默认只读，必要目录单独挂载可写卷
- 只开放必须系统调用和网络出口

3. **资源限制**
- 限制 CPU、内存、磁盘、进程数
- 所有命令执行设置超时

4. **路径与网络边界**
- 文件访问白名单（workspace 内）
- 禁止访问敏感路径（密钥目录、系统目录）
- 网络访问按域名/IP 白名单策略控制

5. **审计与追踪**
- 记录每次执行：调用者、参数、命令、退出码、耗时、资源用量
- 高风险命令触发告警

### 参考配置（Kubernetes 安全上下文）

```yaml
securityContext:
  runAsNonRoot: true
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  capabilities:
    drop: ["ALL"]
  seccompProfile:
    type: RuntimeDefault
resources:
  limits:
    cpu: "1"
    memory: "1Gi"
  requests:
    cpu: "200m"
    memory: "256Mi"
```

### 验收标准

- [ ] 任意 Skill/Tool 执行都在隔离环境完成  
- [ ] 执行超时、资源上限、路径白名单已启用  
- [ ] 审计日志可追溯到单次调用  
- [ ] 故障/越权演练可证明隔离有效  

---

## 总结

### 关键要点

1. **纵深防御**: 多层安全控制
2. **最小权限**: 只给必要的权限
3. **默认拒绝**: 除非明确允许
4. **职责分离**: 分离敏感操作

### OWASP Top 10 防护

1. **注入攻击**: 输入验证，参数化查询
2. **认证失效**: 强密码，多因素认证
3. **数据泄露**: 加密，脱敏
4. **XXE**: 禁用 XML 外部实体
5. **访问控制**: 权限检查
6. **配置错误**: 安全配置，移除默认账户
7. **XSS**: 输出转义，CSP
8. **不安全反序列化**: 避免反序列化不可信数据
9. **使用有漏洞的组件**: 定期更新
10. **日志不足**: 完整的审计日志

### 下一步

- 学习 API 密钥管理
- 学习速率限制
- 学习安全测试

---

## 参考资源

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [Google Cloud Security Best Practices](https://cloud.google.com/security)
- [AWS Security Best Practices](https://docs.aws.amazon.com/whitepapers/latest/security-best-practices/)

---

**完成时间**: ____
**验证状态**: ⏳ 待完成
