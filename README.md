# AI 图片生成自动化项目

基于Google AI Studio和豆包生图的图片生成自动化服务，提供REST API接口和多实例浏览器管理。

## 项目结构

```
crawler_py/
├── src/                          # 源代码
│   ├── api/                     # API服务模块
│   │   ├── ai_studio_api.py           # AI Studio API服务
│   │   ├── ai_studio_api_refactored.py # AI Studio API重构版
│   │   ├── doubao_api.py              # 豆包API服务
│   │   ├── ai_studio_management_api.py # AI Studio管理界面
│   │   ├── doubao_management_api.py    # 豆包管理界面
│   │   ├── base_image_api.py          # 基础图片API
│   │   ├── base_management_api.py     # 基础管理API
│   │   ├── base_multi_instance_server.py # 多实例服务器基础
│   │   └── browser_management_api.py  # 浏览器管理API
│   ├── core/                    # 核心功能模块
│   │   ├── browser_manager.py         # 浏览器管理器
│   │   ├── service_browser_manager.py # 服务浏览器管理器
│   │   ├── crawler_framework.py       # 爬虫框架
│   │   ├── interactive_ai_studio.py   # AI Studio交互客户端
│   │   └── interactive_doubao_image.py # 豆包交互客户端
│   └── utils/                   # 工具模块
│       └── filters.py                 # 过滤工具
├── tests/                       # 测试文件
│   ├── test_api_client.py
│   ├── test_doubao_image.py
│   ├── test_interactive_components.py
│   └── simple_test.py
├── examples/                    # 示例代码
│   ├── start_doubao_image_test.py     # 豆包生图测试
│   ├── start_interactive_test.py      # 交互式测试
│   ├── test_ai_studio_navigation.py   # AI Studio导航测试
│   ├── test_api_with_aspect_ratio.py  # 宽高比API测试
│   ├── test_doubao_api.py            # 豆包API测试
│   ├── test_multiple_reference_images.py # 多参考图片测试
│   └── test_new_workflow.py          # 新工作流测试
├── config/                      # 配置文件
│   └── server_config.json            # 服务器配置
├── docs/                        # 文档
│   ├── API_USAGE_GUIDE.md
│   ├── DOUBAO_IMAGE_GUIDE.md
│   ├── MULTI_INSTANCE_GUIDE.md
│   ├── PERSISTENT_BROWSER_GUIDE.md
│   └── WORKFLOW_USAGE.md
├── data/                        # 数据目录（运行时生成）
│   ├── logs/                    # 日志文件
│   ├── screenshots/             # 截图文件
│   ├── cookies/                 # Cookie文件
│   └── *.json                   # 浏览器实例数据
├── main.py                      # AI Studio单实例启动脚本
├── main_refactored.py           # AI Studio多实例启动脚本
├── doubao_main.py               # 豆包多实例启动脚本
├── requirements.txt             # Python依赖
├── environment.yml              # Conda环境配置
└── test.py                      # 快速测试脚本
```

## 快速开始

### 1. 环境准备

```bash
# 方式1：使用Conda（推荐）
conda env create -f environment.yml
conda activate camoufox-crawler

# 方式2：使用pip
pip install -r requirements.txt
```

### 2. 启动服务

#### AI Studio 多实例服务（推荐）
```bash
# 启动AI Studio多实例服务（API + 管理界面）
python main_refactored.py
```
- 图片生成API: `http://localhost:8812`
- 浏览器管理界面: `http://localhost:8813`
- API文档: `http://localhost:8812/docs`

#### 豆包多实例服务
```bash
# 启动豆包多实例服务（API + 管理界面）
python doubao_main.py
```
- 图片生成API: `http://localhost:8814`
- 浏览器管理界面: `http://localhost:8815`
- API文档: `http://localhost:8814/docs`

#### 单实例服务（兼容模式）
```bash
# AI Studio单实例服务
python main.py

# 豆包交互式测试
python examples/start_doubao_image_test.py
```

### 3. 浏览器实例管理

多实例服务启动后，需要通过管理界面创建浏览器实例：

1. 访问管理界面（AI Studio: `http://localhost:8813`，豆包: `http://localhost:8815`）
2. 点击"创建新实例"按钮
3. 等待浏览器启动并完成初始化
4. 手动登录对应的服务（AI Studio或豆包）
5. 实例状态变为"运行中"后即可处理生图任务

**并发能力 = 运行中的浏览器实例数量**

### 4. 测试服务

```bash
# 快速测试API服务
python test.py

# 测试多参考图片功能
python examples/test_multiple_reference_images.py

# 测试宽高比设置
python examples/test_api_with_aspect_ratio.py
```

## API接口

### 1. 生成图片（JSON格式）

```http
POST /generate
Content-Type: application/json

{
  "prompt": "画一只可爱的小猫咪，卡通风格",
  "reference_images_b64": [
    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
    "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQAB..."
  ],
  "aspect_ratio": "16:9"
}
```

**请求参数：**
- `prompt` (string, 必需): 图片生成提示词
- `reference_images_b64` (array, 可选): 参考图片的base64编码数组，支持多张图片
- `aspect_ratio` (string, 可选): 图片宽高比，支持 "Auto", "1:1", "2:3", "3:2", "4:3", "3:4", "9:16", "16:9"

**响应格式：**
```json
{
  "success": true,
  "task_id": "uuid-string",
  "message": "图片生成成功",
  "generated_images": [
    "iVBORw0KGgoAAAANSUhEUgAA...",
    "iVBORw0KGgoAAAANSUhEUgAA..."
  ],
  "ai_text_response": "我为您生成了一只可爱的卡通小猫咪..."
}
```

### 2. 生成图片（文件上传）

```http
POST /generate-with-file
Content-Type: multipart/form-data

prompt: "画一只可爱的小猫咪，卡通风格"
reference_images: [file1.png, file2.jpg]
aspect_ratio: "16:9"
```

### 3. 健康检查

```http
GET /health
```

**响应格式：**
```json
{
  "status": "healthy",
  "ai_studio_initialized": true,
  "browser_instances": {
    "total": 3,
    "running": 2,
    "available": 1,
    "busy": 1
  },
  "concurrency_capacity": 2,
  "active_tasks": 1,
  "timestamp": "2025-11-10T10:30:00",
  "message": "系统就绪，当前有 2 个浏览器实例运行中"
}
```

### 4. 根路径

```http
GET /
```

返回服务基本信息和状态。

## 功能特性

### 🚀 多实例并发处理
- ✅ **多浏览器实例管理**: 支持同时运行多个浏览器实例
- ✅ **并发图片生成**: 并发能力 = 运行中的浏览器实例数量
- ✅ **实例状态监控**: 实时监控实例运行状态和任务分配
- ✅ **负载均衡**: 自动分配任务到可用实例
- ✅ **故障恢复**: 实例异常时自动重启和恢复

### 🎨 AI Studio 服务
- ✅ **多参考图片**: 支持同时上传多张参考图片
- ✅ **智能解析**: 自动解析AI响应，提取生成的图片和文本
- ✅ **宽高比设置**: 支持多种图片比例（Auto, 1:1, 2:3, 3:2, 4:3, 3:4, 9:16, 16:9）
- ✅ **会话管理**: 自动保存和恢复登录状态
- ✅ **错误处理**: 完整的错误处理和重试机制

### 🤖 豆包生图服务
- ✅ **技能自动选择**: 智能检测和选择图像生成技能
- ✅ **图片下载转换**: 自动下载生成的图片并转换为base64
- ✅ **多重试机制**: 网络异常时自动重试下载
- ✅ **比例设置**: 支持多种图片比例设置
- ✅ **并发安全**: 支持多实例并发生成

### 🛠️ 技术特性
- ✅ **RESTful API**: 标准的REST API接口
- ✅ **FastAPI框架**: 高性能异步API框架
- ✅ **Swagger文档**: 自动生成API文档
- ✅ **多格式支持**: 支持JSON和文件上传两种方式
- ✅ **实时日志**: 详细的操作日志和错误追踪
- ✅ **健康检查**: 完整的系统状态监控

## 多实例浏览器管理

### 管理界面功能

访问管理界面可以进行以下操作：

**AI Studio管理界面** (`http://localhost:8813`)
- 📊 **实例状态监控**: 查看所有浏览器实例的运行状态
- ➕ **创建新实例**: 一键创建新的浏览器实例
- 🔄 **重启实例**: 重启异常的浏览器实例
- 🗑️ **删除实例**: 清理不需要的浏览器实例
- 📈 **性能监控**: 查看任务处理统计和性能指标

**豆包管理界面** (`http://localhost:8815`)
- 功能与AI Studio管理界面相同，专门管理豆包服务实例

### 实例状态说明

- 🟢 **运行中**: 实例正常运行，可以处理任务
- 🟡 **忙碌中**: 实例正在处理任务
- 🔴 **已停止**: 实例已停止运行
- ⚠️ **异常**: 实例出现异常，需要重启

### 并发处理机制

1. **任务分发**: API收到请求后自动分配给可用实例
2. **负载均衡**: 优先使用空闲实例，避免单个实例过载
3. **故障转移**: 实例异常时自动重试其他可用实例
4. **资源隔离**: 每个实例独立运行，互不影响

## 开发说明

### 目录说明

- `src/api/`: FastAPI服务和多实例管理相关代码
- `src/core/`: 核心浏览器管理和AI交互逻辑
- `tests/`: 测试代码和测试客户端
- `examples/`: 使用示例和测试脚本
- `config/`: 服务器配置文件
- `docs/`: 详细的项目文档
- `data/`: 运行时数据（日志、截图、cookies、实例数据等）

### 开发模式

```bash
# AI Studio开发模式（单实例）
uvicorn src.api.ai_studio_api:app --reload --host 0.0.0.0 --port 8812

# 豆包开发模式（单实例）
uvicorn src.api.doubao_api:app --reload --host 0.0.0.0 --port 8814

# 多实例服务开发模式
python main_refactored.py  # AI Studio多实例
python doubao_main.py      # 豆包多实例
```

### 配置文件

编辑 `config/server_config.json` 来修改服务配置：

```json
{
  "ai_studio": {
    "api_port": 8812,
    "management_port": 8813,
    "service_name": "AI Studio"
  },
  "doubao": {
    "api_port": 8814,
    "management_port": 8815,
    "service_name": "豆包"
  }
}
```

## 使用注意事项

### 🔐 首次使用设置

**AI Studio服务**
1. 启动多实例服务后，通过管理界面创建浏览器实例
2. 在弹出的浏览器中手动登录Google AI Studio
3. 登录状态会自动保存在 `data/cookies/` 目录
4. 实例状态变为"运行中"后即可开始使用API

**豆包服务**
1. 启动多实例服务后，通过管理界面创建浏览器实例
2. 在弹出的浏览器中手动登录豆包账户
3. 程序会自动检测和选择图像生成技能
4. 登录状态会自动保存，下次启动时自动恢复

### ⚡ 性能优化建议

1. **实例数量**: 建议根据机器性能创建2-4个浏览器实例
2. **内存使用**: 每个实例大约占用200-300MB内存
3. **并发限制**: 避免创建过多实例导致系统资源不足
4. **网络稳定**: 确保网络连接稳定，避免图片下载失败

### 🛠️ 常见问题

**❌ manifest.json is missing 错误**

这是camoufox浏览器安装不完整导致的，使用以下方法修复：

```bash
# 方法1：运行自动修复脚本
python fix_camoufox.py

# 方法2：使用一键修复脚本
# macOS/Linux:
./install_fix.sh

# Windows:
install_fix.bat

# 方法3：手动修复
pip uninstall camoufox -y
pip cache purge
pip install camoufox>=0.2.0 --force-reinstall --no-cache-dir
python -m playwright install
```

**实例启动失败**
- 检查是否已安装camoufox浏览器
- 确认端口未被占用
- 查看日志文件排查具体错误
- 运行 `python fix_camoufox.py` 诊断问题

**图片生成失败**
- 确认已正确登录对应服务
- 检查提示词是否符合平台规范
- 查看实例状态是否正常

**API调用超时**
- 图片生成通常需要30-120秒
- 可以通过健康检查接口监控系统状态
- 必要时重启异常实例

**依赖安装问题**
- 确保Python版本 >= 3.8
- 使用虚拟环境避免依赖冲突
- 如果网络不稳定，使用国内镜像源：
  ```bash
  pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
  ```

## 📚 详细文档

- [API使用指南](docs/API_USAGE_GUIDE.md) - 详细的API使用说明
- [多实例管理指南](docs/MULTI_INSTANCE_GUIDE.md) - 浏览器实例管理
- [豆包生图指南](docs/DOUBAO_IMAGE_GUIDE.md) - 豆包服务使用说明
- [持久化浏览器指南](docs/PERSISTENT_BROWSER_GUIDE.md) - 浏览器状态管理
- [工作流使用指南](docs/WORKFLOW_USAGE.md) - 完整工作流程

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源许可证。
