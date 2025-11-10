# API测试脚本快速开始指南

## 快速测试

### 1. 基本测试（默认参数）
```bash
python api_test.py
```

这将：
- 使用google搜索引擎
- 执行5次请求
- 使用不同的随机关键词
- 串行模式，默认间隔1秒
- 将结果保存到test_results.csv

### 2. 指定搜索引擎
```bash
# 测试Bing搜索引擎
python api_test.py -e bing

# 测试Yahoo搜索引擎
python api_test.py -e yahoo
```

### 3. 指定请求次数
```bash
# 执行10次测试
python api_test.py -n 10

# 执行20次测试，使用bing引擎
python api_test.py -e bing -n 20
```

### 4. 并发模式
```bash
# 启用并发模式
python api_test.py -c

# 并发模式 + 20次请求
python api_test.py -c -n 20
```

### 5. 速率控制
```bash
# 每秒10个请求（每0.1秒发起一个）
python api_test.py -r 10

# 每秒5个请求（每0.2秒发起一个）
python api_test.py -r 5

# 并发模式 + 速率限制
python api_test.py -c -r 10 -n 20
```

### 6. 指定输出文件
```bash
# 保存到自定义文件
python api_test.py -o my_test_results.csv

# 完整示例：并发测试google引擎20次，速率10/s，保存到google_test.csv
python api_test.py -c -e google -n 20 -r 10 -o google_test.csv
```

### 7. 查看帮助
```bash
python api_test.py -h
```

## 查看测试结果

测试完成后，CSV文件将包含以下信息：

| 列名 | 说明 |
|------|------|
| timestamp | 请求时间 |
| engine | 搜索引擎 |
| keyword | 搜索关键词 |
| status_code | HTTP状态码 |
| response_time | 响应时间(秒) |
| response_size | 响应大小(KB) |
| response_excerpt | 响应内容摘要 |
| error | 错误信息 |

## 运行单元测试

```bash
python test_api_test.py
```

## 查看使用示例

```bash
python example_usage.py
```

## 关键特性

✅ **动态引擎参数** - 通过命令行轻松切换搜索引擎  
✅ **关键词唯一性** - 115+关键词池，保证每次请求使用不同关键词  
✅ **并发请求支持** - 可并发执行测试，显著提高效率  
✅ **精确速率控制** - 可设置每秒请求数（如10表示每0.1秒一个）  
✅ **详细日志** - 记录所有请求细节到CSV文件  
✅ **响应大小KB单位** - 更直观的文件大小显示  
✅ **错误处理** - 捕获并记录所有错误  
✅ **统计信息** - 自动计算成功率、平均响应时间等  
✅ **零依赖** - 仅使用Python标准库  

## 使用场景

### 场景1：快速测试
```bash
# 串行模式，5次请求
python api_test.py
```

### 场景2：压力测试
```bash
# 并发模式，100次请求，每秒20个
python api_test.py -c -n 100 -r 20
```

### 场景3：不同引擎对比测试
```bash
# 测试多个引擎
python api_test.py -e google -n 10 -o google.csv
python api_test.py -e bing -n 10 -o bing.csv
python api_test.py -e yahoo -n 10 -o yahoo.csv
```

## 注意事项

1. 使用并发模式时建议设置合理的速率限制，避免过载
2. 每次请求之间的时间间隔 = 1 / 速率（如速率10表示0.1秒间隔）
3. 响应内容仅保存前200字符作为摘要
4. 响应大小单位为KB（千字节），保留3位小数
5. 当关键词池用完后会自动重置，继续使用不重复的关键词
