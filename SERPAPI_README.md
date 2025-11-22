# SerpAPI性能测试脚本

## 概述

这是一个专为测试SerpAPI (https://serpapi.com/search-api) 性能而设计的Python脚本。支持所有SerpAPI引擎的并发测试，提供详细的性能统计数据。

## 主要特性

✅ **支持所有SerpAPI引擎** - 包含26+个搜索引擎（Google、Bing、Yahoo等）  
✅ **可配置并发测试** - 自定义并发数进行性能测试  
✅ **准确的响应时间测量** - 仅测量网络请求时间，不包括队列等待和处理时间  
✅ **智能响应验证** - 正确判断请求成功/失败，支持各种错误情况  
✅ **禁用缓存** - 所有请求使用 `no_cache=true` 参数获取真实响应时间  
✅ **可选详细记录** - 可选择是否保存每个请求的详细CSV日志  
✅ **汇总统计表** - 自动生成包含所有关键指标的统计表  
✅ **零外部依赖** - 仅使用Python标准库  

## 环境要求

- Python 3.6 或更高版本
- 无需额外依赖包（仅使用Python标准库）

## 支持的引擎

脚本支持以下26个搜索引擎：

### 通用搜索引擎
- google, bing, yahoo, baidu, yandex, duckduckgo

### Google专项引擎
- google_images, google_videos, google_news, google_shopping
- google_scholar, google_maps, google_jobs, google_flights, google_lens

### Bing专项引擎
- bing_images, bing_videos, bing_news

### 电商平台
- amazon, ebay, walmart, apple_app_store, google_play, home_depot

### 其他
- youtube, naver

使用 `--list-engines` 查看完整列表。

## 使用方法

### 基本用法

```bash
# 测试单个引擎
python serpapi_test.py -k YOUR_API_KEY -e google -n 10 -c 5

# 测试多个引擎
python serpapi_test.py -k YOUR_API_KEY -e google bing yahoo -n 20 -c 10

# 测试所有引擎
python serpapi_test.py -k YOUR_API_KEY --all-engines -n 10 -c 5
```

### 高级用法

```bash
# 启用详细CSV记录
python serpapi_test.py -k YOUR_API_KEY -e google -n 10 -c 5 --save-details

# 指定搜索关键词
python serpapi_test.py -k YOUR_API_KEY -e google -n 10 -c 5 -q "machine learning"

# 自定义输出文件名
python serpapi_test.py -k YOUR_API_KEY -e google bing -n 20 -c 10 -o my_stats.csv

# 高并发压力测试
python serpapi_test.py -k YOUR_API_KEY -e google -n 100 -c 50
```

### 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-k, --api-key` | SerpAPI认证密钥（必需） | - |
| `-e, --engines` | 要测试的引擎列表 | - |
| `--all-engines` | 测试所有支持的引擎 | False |
| `-n, --num-requests` | 每个引擎的请求数 | 10 |
| `-c, --concurrency` | 并发数 | 5 |
| `-q, --query` | 搜索关键词 | 随机 |
| `--save-details` | 保存详细CSV记录 | False |
| `-o, --output` | 汇总统计表文件名 | serpapi_summary_statistics.csv |
| `--list-engines` | 列出所有支持的引擎 | - |

## 输出说明

### 汇总统计表

脚本会生成一个包含以下指标的CSV统计表：

| 列名 | 说明 |
|------|------|
| 产品类别 | 固定为"SerpAPI" |
| 引擎 | 搜索引擎名称 |
| 请求总数 | 发送的总请求数 |
| 并发数 | 并发线程数 |
| 请求速率(s/req) | 平均每个请求的耗时（秒） |
| 成功次数 | 成功的请求数 |
| 成功率(%) | 成功请求的百分比 |
| 成功平均响应时间(s) | 成功请求的平均响应时间 |
| P90延迟(s) | 90%的成功请求响应时间低于此值（第90百分位） |
| 并发完成时间(s) | 完成所有请求的总时间 |
| 成功平均响应大小(KB) | 成功响应的平均大小 |

### 详细记录（可选）

当使用 `--save-details` 参数时，每个引擎会生成一个详细的CSV文件，包含每个请求的信息：

- timestamp: 请求时间戳
- product: 产品类别
- engine: 引擎名称
- query: 搜索关键词
- status_code: HTTP状态码
- response_time: 响应时间（秒）
- response_size: 响应大小（KB）
- success: 是否成功
- error: 错误信息（如有）
- response_excerpt: 响应摘要

## 响应验证逻辑

脚本使用智能逻辑判断SerpAPI响应是否成功：

### 成功条件
1. HTTP状态码为200
2. 响应JSON不包含 `error` 字段
3. 响应包含至少一种搜索结果字段：
   - organic_results（有机搜索结果）
   - shopping_results（购物结果）
   - images_results（图片结果）
   - videos_results（视频结果）
   - news_results（新闻结果）
   - local_results（本地结果）
   - jobs_results（职位结果）
   - scholar_results（学术结果）
   - 等其他结果类型

### 失败情况
- HTTP状态码非200（如401、403、429等）
- 响应包含 `error` 字段
- 响应不包含任何结果字段
- JSON解析失败
- 网络连接错误

## 性能测试说明

### 准确的响应时间测量

脚本确保响应时间测量的准确性：

```python
# 记录开始时间（发送请求前）
start_time = time.time()

# 发送请求
conn.request("GET", path)

# 获取响应
response = conn.getresponse()

# 读取数据
data = response.read()

# 记录结束时间（数据接收完成后）
end_time = time.time()
response_time = end_time - start_time
```

**不包括的时间：**
- 线程池排队等待时间
- CSV文件写入时间
- 统计计算时间
- 控制台输出时间

### 缓存控制

所有请求自动添加 `no_cache=true` 参数，确保：
- 获取最新数据
- 测量真实的API响应时间
- 避免缓存影响性能测试结果

## 示例场景

### 场景1：快速性能检查
```bash
# 测试Google引擎，10个请求，5并发
python serpapi_test.py -k YOUR_API_KEY -e google -n 10 -c 5
```

### 场景2：多引擎对比
```bash
# 对比三个主流搜索引擎的性能
python serpapi_test.py -k YOUR_API_KEY -e google bing yahoo -n 20 -c 10
```

### 场景3：全引擎性能测试
```bash
# 测试所有26个引擎
python serpapi_test.py -k YOUR_API_KEY --all-engines -n 10 -c 5
```

### 场景4：压力测试
```bash
# 高并发压力测试，100请求，50并发
python serpapi_test.py -k YOUR_API_KEY -e google -n 100 -c 50 --save-details
```

### 场景5：特定关键词测试
```bash
# 测试特定业务关键词
python serpapi_test.py -k YOUR_API_KEY -e google -n 20 -c 10 -q "Python programming"
```

## 运行单元测试

```bash
python test_serpapi.py
```

测试覆盖：
- 初始化和配置
- 响应成功/失败判断
- 错误信息提取
- 响应摘要生成
- 统计计算
- 各种结果类型识别

## 注意事项

1. **API配额限制**：请注意SerpAPI的API配额限制，避免超出限制
2. **并发数设置**：建议根据API限制合理设置并发数
3. **网络超时**：默认超时30秒，可根据网络情况调整
4. **错误处理**：脚本会捕获所有错误并记录，不会中断测试
5. **存储空间**：使用 `--save-details` 时注意磁盘空间

## 输出示例

### 控制台输出
```
================================================================================
开始批量引擎性能测试
================================================================================

开始测试引擎: google
  总请求数: 10
  并发数: 5
  缓存: 禁用 (no_cache=true)
--------------------------------------------------------------------------------
  进度: 10/10 完成

并发测试完成，总耗时: 3.245秒

================================================================================
汇总统计表已保存到: serpapi_summary_statistics.csv
================================================================================

汇总统计表:
--------------------------------------------------------------------------------------
引擎                   请求数   并发 速率(s/req)     成功   成功率 平均响应(s) 完成时间(s) 响应大小(KB)
--------------------------------------------------------------------------------------
google                     10      5        0.324        10      100%        0.312        3.245         45.678
--------------------------------------------------------------------------------------

测试完成!
```

### CSV统计表示例
```csv
产品类别,引擎,请求总数,并发数,请求速率(s/req),成功次数,成功率(%),成功平均响应时间(s),P90延迟(s),并发完成时间(s),成功平均响应大小(KB)
SerpAPI,google,10,5,0.324,10,100.0,0.312,0.385,3.245,45.678
SerpAPI,bing,10,5,0.287,10,100.0,0.275,0.341,2.874,38.234
SerpAPI,yahoo,10,5,0.356,9,90.0,0.341,0.421,3.562,42.156
```

## 问题排查

### 常见错误

1. **Invalid API key**
   - 检查API密钥是否正确
   - 确认API密钥是否激活

2. **超时错误**
   - 检查网络连接
   - 增加超时时间
   - 降低并发数

3. **速率限制**
   - 减少并发数
   - 增加请求间隔
   - 检查API配额

## 技术特点

- **使用http.client**：标准库HTTP客户端，无需外部依赖
- **线程池并发**：使用concurrent.futures进行高效并发
- **精确计时**：使用time.time()精确测量响应时间
- **结构化数据**：CSV格式便于后续分析
- **错误容错**：完善的错误处理，确保测试稳定运行

## 许可证

本项目使用标准开源许可证。
