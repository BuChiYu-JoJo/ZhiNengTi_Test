#!/usr/bin/env python3
"""
使用示例：演示如何使用api_test.py脚本

这个脚本展示了如何以编程方式使用APITester类
"""

from api_test import APITester


def example_basic_usage():
    """基本使用示例"""
    print("=" * 80)
    print("示例 1: 基本使用")
    print("=" * 80)
    
    # 创建API测试器实例
    tester = APITester("663fba4eb51f1fb2ec007f1b7bd73f16")
    
    # 测试关键词唯一性
    print("\n获取10个随机且唯一的关键词:")
    for i in range(10):
        keyword = tester.get_random_keyword()
        print(f"  {i+1}. {keyword}")
    
    print(f"\n已使用的关键词数量: {len(tester.used_keywords)}")


def example_programmatic_test():
    """编程方式执行测试示例"""
    print("\n" + "=" * 80)
    print("示例 2: 编程方式执行测试")
    print("=" * 80)
    
    # 创建API测试器（带速率限制）
    tester = APITester("663fba4eb51f1fb2ec007f1b7bd73f16", rate_limit=10)
    
    # 运行3次测试，使用google引擎
    print("\n注意: 这将发送实际的API请求")
    print("如果要真正执行，请取消下面代码的注释:\n")
    
    print("# 串行模式:")
    print("# tester.run_tests(")
    print("#     engine='google',")
    print("#     num_requests=3,")
    print("#     output_file='example_results.csv',")
    print("#     concurrent=False")
    print("# )")
    print("")
    print("# 并发模式 + 速率限制:")
    print("# tester.run_tests(")
    print("#     engine='google',")
    print("#     num_requests=10,")
    print("#     output_file='example_results.csv',")
    print("#     concurrent=True")
    print("# )")


def example_different_engines():
    """测试不同搜索引擎示例"""
    print("\n" + "=" * 80)
    print("示例 3: 测试不同搜索引擎")
    print("=" * 80)
    
    engines = ['google', 'bing', 'yahoo', 'duckduckgo']
    
    print("\n支持的搜索引擎示例:")
    for engine in engines:
        print(f"  - {engine}")
    
    print("\n使用方法:")
    print("  命令行串行: python api_test.py -e bing -n 5")
    print("  命令行并发: python api_test.py -e bing -n 10 -c -r 10")
    print("  或编程串行: tester.run_tests(engine='bing', num_requests=5, concurrent=False)")
    print("  或编程并发: tester.run_tests(engine='bing', num_requests=10, concurrent=True)")


def example_rate_control():
    """速率控制示例"""
    print("\n" + "=" * 80)
    print("示例 4: 速率控制")
    print("=" * 80)
    
    print("\n速率控制选项:")
    print("  -r 10  : 每秒10个请求（每0.1秒发起一个）")
    print("  -r 5   : 每秒5个请求（每0.2秒发起一个）")
    print("  -r 20  : 每秒20个请求（每0.05秒发起一个）")
    
    print("\n使用方法:")
    print("  命令行: python api_test.py -c -r 10 -n 20")
    print("  编程方式:")
    print("    tester = APITester('token', rate_limit=10)")
    print("    tester.run_tests(engine='google', num_requests=20, concurrent=True)")


def example_keyword_pool_info():
    """关键词池信息示例"""
    print("\n" + "=" * 80)
    print("示例 5: 关键词池信息")
    print("=" * 80)
    
    tester = APITester("test_token")
    
    print(f"\n关键词池总数: {len(tester.keyword_pool)}")
    print(f"\n前20个关键词示例:")
    for i, keyword in enumerate(tester.keyword_pool[:20], 1):
        print(f"  {i:2d}. {keyword}")
    
    print(f"\n... 共 {len(tester.keyword_pool)} 个关键词")


def example_custom_keywords():
    """自定义关键词示例"""
    print("\n" + "=" * 80)
    print("示例 6: 自定义关键词")
    print("=" * 80)
    
    print("\n使用自定义关键词列表进行测试:")
    print("\n命令行方式:")
    print("  python api_test.py -k pizza burger sushi")
    print("  python api_test.py -k \"machine learning\" \"data science\" \"AI\" -n 10")
    
    print("\n编程方式:")
    print("  tester = APITester('token')")
    print("  custom_keywords = ['apple', 'orange', 'banana']")
    print("  tester.run_tests(")
    print("      engine='google',")
    print("      num_requests=9,")
    print("      keywords=custom_keywords")
    print("  )")
    
    print("\n当请求数量超过关键词数量时，关键词会循环使用:")
    keywords = ['apple', 'orange', 'banana']
    print(f"  关键词列表: {keywords}")
    print("  请求9次的关键词分配:")
    for i in range(9):
        print(f"    请求 {i+1}: {keywords[i % len(keywords)]}")


def example_cache_control():
    """缓存控制示例"""
    print("\n" + "=" * 80)
    print("示例 7: 缓存控制")
    print("=" * 80)
    
    print("\n缓存设置:")
    print("  默认: 启用缓存（提高性能，使用缓存数据）")
    print("  禁用: 使用 --no-cache 参数（获取最新数据）")
    
    print("\n命令行方式:")
    print("  # 使用缓存（默认）")
    print("  python api_test.py -e google -n 5")
    print("")
    print("  # 禁用缓存")
    print("  python api_test.py -e google -n 5 --no-cache")
    
    print("\n编程方式:")
    print("  # 启用缓存（默认）")
    print("  tester_with_cache = APITester('token', use_cache=True)")
    print("  tester_with_cache.run_tests(engine='google', num_requests=5)")
    print("")
    print("  # 禁用缓存")
    print("  tester_no_cache = APITester('token', use_cache=False)")
    print("  tester_no_cache.run_tests(engine='google', num_requests=5)")
    
    print("\n请求参数差异:")
    print("  启用缓存: engine=google&q=pizza&json=1")
    print("  禁用缓存: engine=google&q=pizza&json=1&no_cache=true")


def example_csv_output():
    """CSV输出格式示例"""
    print("\n" + "=" * 80)
    print("示例 8: CSV输出格式")
    print("=" * 80)
    
    print("\nCSV文件将包含以下列:")
    columns = [
        ('timestamp', '请求时间戳', '2025-01-10 14:30:25'),
        ('engine', '搜索引擎类型', 'google'),
        ('keyword', '搜索关键词', 'pizza'),
        ('status_code', 'HTTP状态码', '200'),
        ('response_time', '响应时间(秒)', '1.234'),
        ('response_size', '响应大小(KB)', '15.31'),
        ('response_excerpt', '响应内容摘要', '{"status":"success"...'),
        ('error', '错误信息', '(如有错误)')
    ]
    
    print(f"\n{'列名':<20} {'说明':<15} {'示例':<25}")
    print("-" * 60)
    for col, desc, example in columns:
        print(f"{col:<20} {desc:<15} {example:<25}")


def main():
    """运行所有示例"""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "API测试脚本使用示例" + " " * 38 + "║")
    print("╚" + "═" * 78 + "╝")
    
    example_basic_usage()
    example_programmatic_test()
    example_different_engines()
    example_rate_control()
    example_keyword_pool_info()
    example_custom_keywords()
    example_cache_control()
    example_csv_output()
    
    print("\n" + "=" * 80)
    print("更多使用方法请查看README.md或运行: python api_test.py -h")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
