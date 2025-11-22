# ZhiNengTi_Test

AI API 测试脚本项目

## 项目简介

本项目提供了两个专业的API性能测试脚本：

1. **api_test.py** - ScraperAPI测试脚本
   - 用于测试 ScraperAPI (thordata.com) 服务
   - 支持动态参数配置、随机关键词生成
   - 可控制缓存行为和请求速率
   
2. **serpapi_test.py** - SerpAPI性能测试脚本 (新增)
   - 用于测试 SerpAPI (serpapi.com) 服务
   - 支持26个搜索引擎的批量性能测试
   - 提供完整的性能统计和分析
   - **详细文档**: [SERPAPI_README.md](SERPAPI_README.md)

---

## ScraperAPI 测试脚本 (api_test.py)

### 功能特点

1. **动态引擎参数**: 支持通过命令行参数指定不同的搜索引擎（google, bing, yahoo等）
2. **灵活关键词选择**: 支持随机关键词生成或自定义关键词列表
   - 随机模式：内置100+关键词池，确保每次请求使用不同的搜索关键词
   - 自定义模式：可指定自己的关键词列表，适合特定场景测试
3. **缓存控制**: 可选择启用或禁用API请求缓存
   - 默认启用缓存以提高性能
   - 使用 `--no-cache` 参数禁用缓存以获取最新数据
4. **并发请求支持**: 支持异步并发请求，可显著提高测试效率
5. **速率控制**: 可精确控制请求速率（如每秒10个请求）
6. **详细日志记录**: 将以下信息保存到 CSV 文件：
   - 请求时间戳
   - 搜索引擎类型
   - 搜索关键词
   - HTTP状态码
   - 响应时间（秒）
   - 响应内容大小（KB）
   - 响应内容摘要（前200字符）
   - 错误信息（如有）
6. **统计分析**: 自动计算并显示测试统计信息

## 环境要求

- Python 3.6 或更高版本
- 无需额外依赖包（仅使用Python标准库）

## 使用方法

### 基本用法

```bash
python api_test.py
```

这将使用默认参数运行测试：
- 搜索引擎：google
- 请求次数：5次
- 输出文件：test_results.csv

### 高级用法

```bash
# 指定搜索引擎
python api_test.py -e bing

# 指定请求次数
python api_test.py -n 10

# 指定输出文件
python api_test.py -o my_results.csv

# 指定API令牌
python api_test.py -t YOUR_API_TOKEN

# 使用自定义关键词
python api_test.py -k pizza burger sushi

# 禁用缓存
python api_test.py --no-cache

# 使用自定义关键词并禁用缓存
python api_test.py -k "machine learning" "data science" "AI" --no-cache

# 启用并发模式
python api_test.py -c

# 设置请求速率（每秒10个请求，即每0.1秒一个）
python api_test.py -r 10

# 并发模式 + 速率限制
python api_test.py -c -r 10 -n 20

# 组合使用多个参数
python api_test.py -e google -n 20 -o google_test.csv -c -r 5

# 完整示例：使用自定义关键词、禁用缓存、并发模式
python api_test.py -e google -k apple orange banana -n 6 --no-cache -c -r 5 -o results.csv
```

### 命令行参数说明

- `-e, --engine`: 搜索引擎类型（默认：google）
- `-n, --num-requests`: 请求次数（默认：5）
- `-o, --output`: 输出CSV文件名（默认：test_results.csv）
- `-t, --token`: API认证令牌（默认使用示例令牌）
- `-k, --keywords`: 自定义关键词列表（默认：使用随机关键词）
  - 可以指定一个或多个关键词
  - 当请求数量超过关键词数量时，会循环使用关键词
- `-nc, --no-cache`: 禁用缓存（默认：启用缓存）
  - 使用此参数时，请求中会添加 `no_cache=true` 参数
  - 不使用此参数时，启用缓存以提高性能
- `-c, --concurrent`: 启用并发模式（默认：串行模式）
- `-r, --rate`: 请求速率限制，每秒请求数（如10表示每秒10个请求，即每0.1秒发起一个）

### 查看帮助

```bash
python api_test.py -h
```

## 输出示例

### 控制台输出

```
开始测试 google 引擎，共 5 次请求...
并发模式: 速率限制为每秒 10 个请求 (间隔 0.100秒)
--------------------------------------------------------------------------------

请求 1/5:
  时间戳: 2025-01-10 14:30:25
  引擎: google
  关键词: pizza
  状态码: 200
  响应时间: 1.234秒
  响应大小: 15.31KB
  响应摘要: {"status":"success","data":...

...

================================================================================
测试统计:
================================================================================
总请求数: 5
成功请求: 5
失败请求: 0
平均响应时间: 1.150秒
总数据大小: 77.11KB
================================================================================

测试结果已保存到: test_results.csv
```

### CSV输出格式

CSV文件包含以下列：
- timestamp: 请求时间戳
- engine: 搜索引擎类型
- keyword: 搜索关键词
- status_code: HTTP状态码
- response_time: 响应时间（秒）
- response_size: 响应大小（KB）
- response_excerpt: 响应内容摘要
- error: 错误信息

## 设计特点

### 关键词唯一性保证

脚本内置了100+个预定义关键词，并使用集合（set）跟踪已使用的关键词。每次请求都会从未使用的关键词中随机选择，确保在关键词池范围内不会重复。当所有关键词都被使用后，会自动重置已使用集合。

### 并发请求与速率控制

- **串行模式**（默认）: 顺序执行请求，支持自定义请求间隔
- **并发模式**（`-c`）: 使用线程池并发执行请求，显著提高测试效率
- **速率限制**（`-r`）: 精确控制请求速率，如 `-r 10` 表示每秒10个请求（每0.1秒发起一个）

### 错误处理

脚本包含完善的错误处理机制：
- 网络连接错误
- 响应解析错误
- 文件写入错误

所有错误都会被记录到CSV文件的error列中。

### 性能优化

- 支持并发请求，可根据需求调整并发数
- 灵活的速率控制，避免过于频繁的API调用
- 使用HTTP连接复用减少开销
- 响应内容仅截取前200字符作为摘要，减少存储空间

## 代码结构

```
api_test.py
├── APITester 类
│   ├── __init__: 初始化API测试器（支持速率限制）
│   ├── get_random_keyword: 获取随机未使用的关键词
│   ├── make_request: 发送API请求
│   ├── save_to_csv: 保存结果到CSV
│   ├── run_tests: 运行多次测试（支持串行/并发模式）
│   ├── _run_sequential_tests: 串行执行测试
│   ├── _run_concurrent_tests: 并发执行测试
│   ├── _print_result: 打印单个请求结果
│   └── _print_statistics: 打印统计信息
└── main: 主函数，处理命令行参数
```

---

## SerpAPI 性能测试脚本 (serpapi_test.py)

### 概述

专为SerpAPI性能测试设计的脚本，支持批量测试26个搜索引擎，提供完整的性能指标分析。

### 核心特性

- ✅ **26个搜索引擎支持**: Google、Bing、Yahoo及各专项引擎
- ✅ **批量测试**: 支持 `--all-engines` 测试所有引擎
- ✅ **精确响应时间**: 仅测量网络请求时间（不含排队、处理等）
- ✅ **智能响应验证**: 正确识别成功/失败，覆盖所有错误场景
- ✅ **可选详细记录**: 使用 `--save-details` 启用详细CSV日志
- ✅ **汇总统计表**: 11项完整性能指标（产品、引擎、请求数、并发数、速率、成功率、平均响应时间、P90延迟等）
- ✅ **禁用缓存**: 自动添加 `no_cache=true` 获取真实响应时间

### 快速开始

```bash
# 列出所有支持的引擎
python serpapi_test.py --list-engines

# 测试单个引擎
python serpapi_test.py -k YOUR_API_KEY -e google -n 10 -c 5

# 测试多个引擎
python serpapi_test.py -k YOUR_API_KEY -e google bing yahoo -n 20 -c 10

# 测试所有引擎
python serpapi_test.py -k YOUR_API_KEY --all-engines -n 10 -c 5

# 启用详细CSV记录
python serpapi_test.py -k YOUR_API_KEY -e google -n 10 -c 5 --save-details
```

### 输出示例

**汇总统计表** (serpapi_summary_statistics.csv):
```
产品类别,引擎,请求总数,并发数,请求速率(s/req),成功次数,成功率(%),成功平均响应时间(s),P90延迟(s),并发完成时间(s),成功平均响应大小(KB)
SerpAPI,google,10,5,0.324,10,100.0,0.312,0.385,3.245,45.678
SerpAPI,bing,10,5,0.287,10,100.0,0.275,0.341,2.874,38.234
```

### 响应验证逻辑

脚本智能判断SerpAPI响应成功/失败：

**成功条件**:
1. HTTP状态码为200
2. 无 `error` 字段
3. 包含结果字段（organic_results、shopping_results等）

**失败情况**:
- 错误状态码（401、403、429等）
- 包含 `error` 字段
- 无结果字段
- JSON解析失败
- 网络错误

### 完整文档

详细使用说明、参数配置、场景示例请参考: **[SERPAPI_README.md](SERPAPI_README.md)**

---

## 脚本对比

| 功能 | api_test.py | serpapi_test.py |
|------|------------|-----------------|
| 目标API | ScraperAPI | SerpAPI |
| 请求方法 | POST | GET |
| 引擎支持 | 动态配置 | 26个预定义 |
| 批量测试 | 单引擎 | 多引擎/全引擎 |
| 详细CSV | 始终生成 | 可选 |
| 统计指标 | 基础 | 11项完整指标(含P90) |
| 响应验证 | 状态码 | 智能验证 |

## 许可证

MIT License

## 作者

BuChiYu-JoJo
