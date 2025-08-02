# 🚀 HAJIMI Gemini API Proxy

- 这是一个基于 FastAPI 构建的 Gemini API 代理，旨在提供一个简单、安全且可配置的方式来访问 Google 的 Gemini 模型。适用于在 Hugging Face Spaces 上部署，并支持openai api格式的工具集成。

## 项目采用动态更新，随时会有一些小更新同步到主仓库且会自动构建镜像，如果反馈的bug开发者说修了但是版本号没变是正常现象，~~记得勤更新镜像哦~~

# 本项目基于CC BY-NC 4.0许可开源，需遵守以下规则
- 您必须给出适当的署名，提供指向本协议的链接，并指明是否（对原作）作了修改。您可以以任何合理方式进行，但不得以任何方式暗示许可方认可您或您的使用。
- 您不得将本作品用于商业目的，包括但不限于任何形式的商业倒卖、SaaS、API 付费接口、二次销售、打包出售、收费分发或其他直接或间接盈利行为。

### 如需商业授权，请联系原作者获得书面许可。违者将承担相应法律责任。

### 感谢[@warming-afternoon](https://github.com/warming-afternoon)，[@任梓樂](https://github.com/rzline)在技术上的大力支持

###  错误自查

遇到问题请先查看以下的 **错误自查** 文档，确保已尝试按照其上的指示进行了相应的排查与处理。

- [错误自查](./wiki/error.md)
###  使用文档
- [huggingface 部署的使用文档（复活？！）（推荐，免费，手机电脑均可使用）](./wiki/huggingface2.md)

- [Claw Cloud部署的使用文档（推荐，免费，手机电脑均可使用）](./wiki/claw.md) 感谢[@IDeposit](https://github.com/IDeposit)编写

- [termux部署的使用文档（手机使用）](./wiki/Termux.md) 感谢[@天命不又](https://github.com/tmby)编写

- [windows 本地部署的使用文档](./wiki/windows.md)

- ~~[zeabur部署的使用文档(需付费)](./wiki/zeabur.md) 感谢**墨舞ink**编写~~（已过时且暂时无人更新，欢迎提交pull requests）

- [vertex模式的使用文档](./wiki/vertex.md)

### 🐳 Docker 部署 (Linux)

您可以在任何安装了 Docker 的 Linux 环境中轻松部署此应用。

**第一步：获取项目文件**

首先，您需要将项目文件下载到您的服务器上，例如使用 `git clone`。

```bash
# 示例:
# git clone https://github.com/your-repo/hajimi.git
# cd hajimi
```

**第二步：构建 Docker 镜像**

在项目根目录下（即 `Dockerfile` 所在的目录），执行以下命令来构建镜像：

```bash
docker build -t hajimi-proxy .
```

**第三步：运行 Docker 容器**

使用以下命令启动容器。请务必将 `your_secret_password` 和 `your_gemini_api_key_1,...` 替换为您自己的值。

```bash
docker run -d \
  -p 7860:7860 \
  -e PASSWORD="your_secret_password" \
  -e GEMINI_API_KEYS="your_gemini_api_key_1,your_gemini_api_key_2" \
  --name hajimi-proxy-container \
  --restart always \
  hajimi-proxy
```

*   `-d`: 后台运行容器。
*   `-p 7860:7860`: 将主机的 7860 端口映射到容器的 7860 端口。您可以根据需要更改主机端口（冒号前的数字）。
*   `-e PASSWORD="..."`: **必需**。设置客户端访问代理所需的密码。
*   `-e GEMINI_API_KEYS="..."`: **必需**。设置代理服务内部使用的真实 Gemini API 密钥，多个密钥用英文逗号隔开。
*   `--name ...`: 为您的容器指定一个方便识别的名称。
*   `--restart always`: 使容器在宿主机重启后能够自动启动。

**如何管理容器：**

*   **查看实时日志**: `docker logs -f hajimi-proxy-container`
*   **停止容器**: `docker stop hajimi-proxy-container`
*   **启动容器**: `docker start hajimi-proxy-container`
*   **删除容器**: `docker rm hajimi-proxy-container`


###  更新日志
* v1.0.1
   * 新增`清除失效密钥`功能
   * 新增`输出有效秘钥`功能

## ✨ 主要功能：

### 🔑 API 密钥轮询和管理

### 📑 模型列表接口

### 💬 聊天补全接口：

*   提供 `/v1/chat/completions` 接口，支持流式和非流式响应，支持函数调用，与 OpenAI API 格式兼容。
*   支持的输入内容: 文本、文件、图像
*   自动将 OpenAI 格式的请求转换为 Gemini 格式。

### ♊ 原生 Gemini API 代理接口：

*   提供 `/gemini/v1beta/*` 路径，用于代理原生 Gemini API 请求。
*   **认证方式**：客户端使用代理服务设置的 `PASSWORD` 进行认证，代理服务使用内部管理的真实 Gemini API Key 池请求 Google。
*   **功能**：完整实现了原生 Gemini API 的功能，包括获取模型列表 (`/models`) 和内容生成 (`/models/{model}:generateContent`)。


### 🔒 密码保护（可选）：

*   通过 `PASSWORD` 环境变量设置密码。
*   提供默认密码 `"123"`。

### 🧩 服务兼容

*   提供的接口与 OpenAI API 格式兼容,便于接入各种服务

### ⚙️ 功能配置

* 方式 1 : 通过网页前端进行配置
* 方式 2 : 根据 [配置文档](./app/config/settings.py) 中的注释说明，修改对应的变量

## ⚠️ 注意事项：

*   **强烈建议在生产环境中设置 `PASSWORD` 环境变量，并使用强密码。**
*   根据你的使用情况调整速率限制相关的环境变量。
*   确保你的 Gemini API 密钥具有足够的配额。


## 💡 特色功能：

### 🎭 假流式传输

*   **作用：** 解决部分网络环境下客户端通过非流式请求 Gemini 时可能遇到的断连问题。**默认开启**。

*   **原理简述：** 当客户端请求流式响应时，本代理会每隔一段时间向客户端发出一个空信息以维持连接，同时在后台向 Gemini 发起一个完整的、非流式的请求。等 Gemini 返回完整响应后，再一次性将响应发回给客户端。

*   **注意：** 如果想使用真的流式请求，请**关闭**该功能

### ⚡ 并发与缓存

*   **作用：** 允许您为用户的单次提问同时向 Gemini 发送多个请求，并将额外的成功响应缓存起来，用于后续重新生成回复。

*   **注意：** 此功能**默认关闭** 。只有当您将并发数设置为 2 或以上时，缓存才会生效。缓存匹配要求提问的上下文与被缓存的问题**完全一致**（包括标点符号）。此外，该模式目前仅支持非流式及假流式传输
    
    **Q: 新版本增加的并发缓存功能会增加 gemini 配额的使用量吗？**
   
    **A: 不会**。因为默认情况下该功能是关闭的。只有当你主动将并发数 `CONCURRENT_REQUESTS` 设置为大于 1 的数值时，才会实际发起并发请求，这才会消耗更多配额。
   
    **Q: 如何使用并发缓存功能？**
   
    **A:** 修改并发请求数，使其等于你想在一次用户提问中同时向 Gemini 发送的请求数量（例如设置为 `3`）。
    
    这样设置后，如果一次并发请求中收到了多个成功的响应，除了第一个返回给用户外，其他的就会被缓存起来。

### 🎭 伪装信息

*   **作用：** 在发送给 Gemini 的消息中添加一段随机生成的、无意义的字符串，用于“伪装”请求，可能有助于防止被识别为自动化程序。**默认开启**。

*   **注意：** 如果使用非 SillyTavern 的其余客户端 (例如 cherryStudio )，请**关闭**该功能

### 🌐 联网模式

*   **作用：** 让 Gemini 模型能够利用搜索工具进行联网搜索，以回答需要最新信息或超出其知识库范围的问题。

*   **如何使用：**

    在客户端请求时，选择模型名称带有 `-search` 后缀的模型（例如 `gemini-2.5-pro-search`，具体可用模型请通过 `/v1/models` 接口查询）。


### 🚦 速率限制和防滥用：

*   通过环境变量自定义限制：
    *   `MAX_REQUESTS_PER_MINUTE`：每分钟最大请求数（默认 30）。
    *   `MAX_REQUESTS_PER_DAY_PER_IP`：每天每个 IP 最大请求数（默认 600）。
*   超过速率限制时返回 429 错误。
