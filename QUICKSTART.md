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

### 4. 指定输出文件
```bash
# 保存到自定义文件
python api_test.py -o my_test_results.csv

# 完整示例：测试google引擎15次，保存到google_test.csv
python api_test.py -e google -n 15 -o google_test.csv
```

### 5. 查看帮助
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
| response_size | 响应大小(字节) |
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
✅ **详细日志** - 记录所有请求细节到CSV文件  
✅ **错误处理** - 捕获并记录所有错误  
✅ **统计信息** - 自动计算成功率、平均响应时间等  
✅ **零依赖** - 仅使用Python标准库  

## 注意事项

1. 每次请求之间自动延迟1秒，避免请求过快
2. 响应内容仅保存前200字符作为摘要
3. 当关键词池用完后会自动重置，继续使用不重复的关键词
4. 所有时间以秒为单位，保留3位小数
