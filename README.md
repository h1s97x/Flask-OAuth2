# Flask App with OAuth

这是一个集成了 OAuth 2.0 (Google, GitHub) 认证的 Flask Web 应用程序。

## 功能

*   用户注册、登录、登出 (基于 Email/密码)
*   通过 Google OAuth 2.0 登录
*   通过 GitHub OAuth 2.0 登录
*   用户个人资料管理 (假设)
*   其他 Flask 扩展集成 (Bootstrap, SQLAlchemy, LoginManager, Moment, Mail, Whooshee, CSRF)

## 安装与设置

1.  **克隆仓库**:

    ```bash
    git clone <your-repository-url>
    cd flask_app
    ```

2.  **创建虚拟环境** (推荐):

    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **安装依赖**:

    假设您有一个 `requirements.txt` 文件 (如果缺少，请根据 `app/extensions.py` 和导入生成):

    ```bash
    pip install -r requirements.txt
    ```

4.  **配置环境变量**: 

    创建 `.env` 文件 (或直接设置系统环境变量)，并填入必要的配置。

    ```dotenv
    # Flask
    FLASK_APP=wsgi.py # 假设入口文件是 wsgi.py
    FLASK_ENV=development
    SECRET_KEY='your-very-secret-key' # 必须设置一个强密钥

    # 数据库 (如果使用 SQLite, 则无需配置 MySQL)
    # USE_SQLITE=True # 取消注释以强制使用 SQLite
    # MYSQL_HOST=127.0.0.1
    # MYSQL_PORT=3306
    # MYSQL_USER=root
    # MYSQL_PASS=your_mysql_password
    # MYSQL_DB=database_learn

    # 邮件配置 (可选, 如果需要邮件功能)
    # MAIL_SERVER='smtp.example.com'
    # MAIL_PORT=465
    # MAIL_USERNAME='your-email@example.com'
    # MAIL_PASSWORD='your-email-password'

    # Google OAuth 2.0
    GOOGLE_CLIENT_ID='your-google-client-id.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET='your-google-client-secret'

    # GitHub OAuth 2.0
    GITHUB_CLIENT_ID='your-github-client-id'
    GITHUB_CLIENT_SECRET='your-github-client-secret'
    ```

    **重要**: 请确保从 Google Cloud Console 和 GitHub Developer Settings 获取您的 OAuth 客户端 ID 和密钥，并配置正确的授权重定向 URI (例如，对于 Google，可能是 `http://localhost:5000/auth/callback/google`；对于 GitHub，可能是 `http://localhost:5000/auth/callback/github`)。

5.  **初始化数据库**:

    ```bash
    flask initdb
    flask init # 初始化角色等
    ```

## 运行应用

```bash
flask run
```

访问 `http://localhost:5000`。

## API 与认证流程

### 标准认证 (Email/密码)

*   `GET /auth/login`: 显示登录页面。
*   `POST /auth/login`: 处理登录表单提交。
*   `GET /auth/register`: 显示注册页面。
*   `POST /auth/register`: 处理注册表单提交。
*   `GET /auth/logout`: 登出用户。

### OAuth 2.0 认证

OAuth 流程允许用户使用第三方服务（如 Google 或 GitHub）登录您的应用。

1.  **发起登录**: 用户点击您网站上的 "Login with Google" 或 "Login with GitHub" 按钮。这些按钮应链接到以下端点：
    *   `GET /auth/login/google`: 重定向用户到 Google 进行授权。
    *   `GET /auth/login/github`: 重定向用户到 GitHub 进行授权。

2.  **用户授权**: 用户在第三方服务提供商的网站上授权您的应用访问其基本信息（如邮箱、用户名）。

3.  **回调处理**: 授权成功后，第三方服务会将用户重定向回您的应用，并附带一个授权码。重定向的目标 URL 是您在服务提供商处配置的回调 URL，对应的 Flask 端点是：
    *   `GET /auth/callback/google`: 处理来自 Google 的回调。应用会使用授权码换取访问令牌 (access token)，然后使用令牌获取用户信息。
    *   `GET /auth/callback/github`: 处理来自 GitHub 的回调。逻辑同上。

4.  **用户关联与登录**: 回调处理端点会：
    *   检查获取到的用户邮箱是否已在您的数据库中存在。
    *   如果存在，则将该用户登录 (使用 `flask_login.login_user`)。
    *   如果不存在，则使用获取到的信息（邮箱、用户名等）在您的数据库中创建一个新用户，然后将该新用户登录。
    *   用户最终会被重定向到应用的主页或其他适当页面。

## 命令行工具

*   `flask initdb [--drop]`: 初始化数据库。`--drop` 选项会在创建前删除现有表。
*   `flask init`: 初始化数据库和角色。
*   `flask forge [--user <n>] [--message <n>]`: 生成虚拟数据用于测试（会先清空数据库）。

## 注意事项

*   请务必妥善保管您的 `SECRET_KEY` 和 OAuth 密钥。
*   确保您的 `User` 模型 (`app/Model/User.py`) 包含处理 OAuth 登录所需的字段（至少 `email`，可能还有 `nickname`, `website`, `github`, `bio` 等）。
*   在生产环境中，`FLASK_ENV` 应设置为 `production`，并禁用 DEBUG 模式。
