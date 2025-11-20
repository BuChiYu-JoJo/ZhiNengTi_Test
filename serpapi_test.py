#!/usr/bin/env python3
"""
SerpAPI Performance Test Script
Tests SerpAPI service with configurable engines, concurrency, and detailed performance metrics.
"""

import http.client
import csv
import time
import json
import argparse
import concurrent.futures
from urllib.parse import urlencode, urlparse
from datetime import datetime
from collections import defaultdict
import ssl


class SerpAPITester:
    """SerpAPI性能测试类"""
    
    # SerpAPI支持的所有引擎
    SUPPORTED_ENGINES = [
        'google', 'bing', 'yahoo', 'baidu', 'yandex', 'duckduckgo',
        'google_images', 'google_videos', 'google_news', 'google_shopping',
        'google_scholar', 'google_maps', 'google_jobs', 'google_flights',
        'bing_images', 'bing_videos', 'bing_news',
        'youtube', 'ebay', 'amazon', 'walmart', 'apple_app_store', 
        'google_play', 'naver', 'home_depot', 'google_lens'
    ]
    
    def __init__(self, api_key, save_details=False):
        """
        初始化SerpAPI测试器
        
        Args:
            api_key: SerpAPI认证密钥
            save_details: 是否保存每个请求的详细CSV记录
        """
        self.api_key = api_key
        self.host = "serpapi.com"
        self.save_details = save_details
        self.keyword_pool = [
            "pizza", "coffee", "restaurant", "weather", "news",
            "hotel", "flight", "car", "phone", "laptop",
            "book", "music", "movie", "game", "sport",
            "health", "fitness", "recipe", "travel", "shopping"
        ]
        
    def make_request(self, engine, query):
        """
        发送单个API请求并测量准确的响应时间
        
        Args:
            engine: 搜索引擎名称
            query: 搜索关键词
            
        Returns:
            dict: 包含请求结果的字典
        """
        result = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'product': 'SerpAPI',
            'engine': engine,
            'query': query,
            'status_code': None,
            'response_time': None,
            'response_size': None,
            'success': False,
            'error': '',
            'response_excerpt': ''
        }
        
        conn = None
        try:
            # 准备请求参数 - 禁用缓存以获取真实响应时间
            params = {
                "engine": engine,
                "q": query,
                "api_key": self.api_key,
                "no_cache": "true"  # 禁用缓存
            }
            
            path = f"/search?{urlencode(params)}"
            
            # 创建HTTPS连接
            conn = http.client.HTTPSConnection(self.host, timeout=30)
            
            # 记录请求开始时间（仅测量网络请求时间）
            start_time = time.time()
            
            # 发送GET请求
            conn.request("GET", path)
            
            # 获取响应
            response = conn.getresponse()
            
            # 读取响应数据
            data = response.read()
            
            # 记录响应结束时间（不包括后续处理时间）
            end_time = time.time()
            result['response_time'] = round(end_time - start_time, 3)
            
            result['status_code'] = response.status
            result['response_size'] = round(len(data) / 1024, 3)  # KB
            
            # 解析响应判断是否成功
            try:
                response_json = json.loads(data.decode('utf-8'))
                result['success'] = self._is_response_successful(response_json, response.status)
                
                # 保存响应摘要
                if result['success']:
                    result['response_excerpt'] = self._extract_response_summary(response_json)
                else:
                    # 如果失败，记录错误信息
                    result['error'] = self._extract_error_message(response_json)
                    
            except json.JSONDecodeError as e:
                result['success'] = False
                result['error'] = f"JSON decode error: {str(e)}"
                result['response_excerpt'] = data.decode('utf-8', errors='ignore')[:200]
            except Exception as e:
                result['success'] = False
                result['error'] = f"Response parse error: {str(e)}"
                
        except Exception as e:
            result['error'] = str(e)
            result['success'] = False
            # 如果请求过程中出错，仍然记录耗时
            if 'start_time' in locals():
                result['response_time'] = round(time.time() - start_time, 3)
        finally:
            if conn:
                conn.close()
                
        return result
    
    def _is_response_successful(self, response_json, status_code):
        """
        判断SerpAPI响应是否成功
        
        成功条件:
        1. HTTP状态码为200
        2. 响应JSON不包含error字段
        3. 响应包含搜索结果数据
        
        Args:
            response_json: 解析后的JSON响应
            status_code: HTTP状态码
            
        Returns:
            bool: 是否成功
        """
        # 检查HTTP状态码
        if status_code != 200:
            return False
        
        # 检查是否有错误字段
        if 'error' in response_json:
            return False
        
        # 检查是否包含搜索结果（不同引擎的结果字段可能不同）
        result_fields = [
            'organic_results', 'shopping_results', 'images_results',
            'videos_results', 'news_results', 'local_results',
            'answer_box', 'knowledge_graph', 'flights_results',
            'jobs_results', 'scholar_results', 'search_information'
        ]
        
        # 只要包含任一结果字段就认为成功
        has_results = any(field in response_json for field in result_fields)
        
        return has_results
    
    def _extract_error_message(self, response_json):
        """
        从响应中提取错误信息
        
        Args:
            response_json: 解析后的JSON响应
            
        Returns:
            str: 错误信息
        """
        if 'error' in response_json:
            return response_json['error']
        return "Unknown error - no results found"
    
    def _extract_response_summary(self, response_json):
        """
        提取响应摘要信息
        
        Args:
            response_json: 解析后的JSON响应
            
        Returns:
            str: 响应摘要
        """
        summary_parts = []
        
        # 提取搜索信息
        if 'search_information' in response_json:
            info = response_json['search_information']
            if 'total_results' in info:
                summary_parts.append(f"total_results:{info['total_results']}")
        
        # 统计各类结果数量
        if 'organic_results' in response_json:
            summary_parts.append(f"organic:{len(response_json['organic_results'])}")
        if 'shopping_results' in response_json:
            summary_parts.append(f"shopping:{len(response_json['shopping_results'])}")
        if 'images_results' in response_json:
            summary_parts.append(f"images:{len(response_json['images_results'])}")
        
        return ", ".join(summary_parts) if summary_parts else "Success"
    
    def run_concurrent_test(self, engine, num_requests, concurrency, query=None):
        """
        运行并发性能测试
        
        Args:
            engine: 搜索引擎名称
            num_requests: 总请求数
            concurrency: 并发数
            query: 搜索关键词（可选，默认随机）
            
        Returns:
            list: 所有请求结果
        """
        results = []
        
        # 如果未指定query，使用随机关键词
        queries = []
        if query:
            queries = [query] * num_requests
        else:
            # 循环使用关键词池
            queries = [self.keyword_pool[i % len(self.keyword_pool)] for i in range(num_requests)]
        
        print(f"\n开始测试引擎: {engine}")
        print(f"  总请求数: {num_requests}")
        print(f"  并发数: {concurrency}")
        print(f"  缓存: 禁用 (no_cache=true)")
        print("-" * 80)
        
        # 记录并发测试的总开始时间
        total_start_time = time.time()
        
        # 使用线程池进行并发测试
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
            # 提交所有任务
            future_to_index = {
                executor.submit(self.make_request, engine, queries[i]): i 
                for i in range(num_requests)
            }
            
            # 收集结果
            completed = 0
            for future in concurrent.futures.as_completed(future_to_index):
                index = future_to_index[future]
                try:
                    result = future.result()
                    results.append(result)
                    completed += 1
                    
                    # 显示进度
                    if completed % max(1, num_requests // 10) == 0 or completed == num_requests:
                        print(f"  进度: {completed}/{num_requests} 完成")
                        
                except Exception as e:
                    print(f"  请求 {index+1} 异常: {str(e)}")
        
        # 记录并发测试的总结束时间
        total_end_time = time.time()
        total_duration = round(total_end_time - total_start_time, 3)
        
        print(f"\n并发测试完成，总耗时: {total_duration}秒")
        
        return results, total_duration
    
    def run_all_engines_test(self, engines, num_requests_per_engine, concurrency):
        """
        测试多个引擎的性能
        
        Args:
            engines: 要测试的引擎列表
            num_requests_per_engine: 每个引擎的请求数
            concurrency: 并发数
            
        Returns:
            dict: 所有引擎的测试结果
        """
        all_results = {}
        all_statistics = []
        
        print("=" * 80)
        print("开始批量引擎性能测试")
        print("=" * 80)
        
        for engine in engines:
            try:
                results, total_duration = self.run_concurrent_test(
                    engine, num_requests_per_engine, concurrency
                )
                
                all_results[engine] = results
                
                # 计算统计数据
                stats = self._calculate_statistics(
                    'SerpAPI', engine, results, num_requests_per_engine, 
                    concurrency, total_duration
                )
                all_statistics.append(stats)
                
                # 如果启用详细记录，保存CSV
                if self.save_details:
                    self._save_detailed_csv(engine, results)
                
            except Exception as e:
                print(f"\n引擎 {engine} 测试失败: {str(e)}")
                continue
        
        return all_results, all_statistics
    
    def _calculate_statistics(self, product, engine, results, total_requests, 
                             concurrency, total_duration):
        """
        计算统计数据
        
        Returns:
            dict: 统计数据
        """
        successful_results = [r for r in results if r['success']]
        failed_results = [r for r in results if not r['success']]
        
        success_count = len(successful_results)
        success_rate = round(success_count / total_requests * 100, 2) if total_requests > 0 else 0
        
        # 计算成功请求的平均响应时间
        avg_response_time = 0
        if successful_results:
            total_time = sum(r['response_time'] for r in successful_results if r['response_time'])
            avg_response_time = round(total_time / len(successful_results), 3)
        
        # 计算请求速率 (秒/请求)
        request_rate = round(total_duration / total_requests, 3) if total_requests > 0 else 0
        
        # 计算成功请求的平均响应大小
        avg_response_size = 0
        if successful_results:
            total_size = sum(r['response_size'] for r in successful_results if r['response_size'])
            avg_response_size = round(total_size / len(successful_results), 3)
        
        stats = {
            '产品类别': product,
            '引擎': engine,
            '请求总数': total_requests,
            '并发数': concurrency,
            '请求速率(s/req)': request_rate,
            '成功次数': success_count,
            '成功率(%)': success_rate,
            '成功平均响应时间(s)': avg_response_time,
            '并发完成时间(s)': total_duration,
            '成功平均响应大小(KB)': avg_response_size
        }
        
        return stats
    
    def _save_detailed_csv(self, engine, results):
        """
        保存详细的请求记录到CSV
        
        Args:
            engine: 引擎名称
            results: 请求结果列表
        """
        filename = f"serpapi_{engine}_detailed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        fieldnames = [
            'timestamp', 'product', 'engine', 'query', 'status_code',
            'response_time', 'response_size', 'success', 'error', 'response_excerpt'
        ]
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        
        print(f"  详细记录已保存到: {filename}")
    
    def save_summary_statistics(self, statistics, filename='serpapi_summary_statistics.csv'):
        """
        保存汇总统计表
        
        Args:
            statistics: 统计数据列表
            filename: 输出文件名
        """
        if not statistics:
            print("没有统计数据可保存")
            return
        
        fieldnames = [
            '产品类别', '引擎', '请求总数', '并发数', '请求速率(s/req)',
            '成功次数', '成功率(%)', '成功平均响应时间(s)', 
            '并发完成时间(s)', '成功平均响应大小(KB)'
        ]
        
        with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(statistics)
        
        print(f"\n{'=' * 80}")
        print(f"汇总统计表已保存到: {filename}")
        print(f"{'=' * 80}")
        
        # 打印统计表
        self._print_statistics_table(statistics)
    
    def _print_statistics_table(self, statistics):
        """
        在控制台打印统计表
        
        Args:
            statistics: 统计数据列表
        """
        print("\n汇总统计表:")
        print("-" * 150)
        
        # 打印表头
        header = f"{'引擎':<20} {'请求数':>8} {'并发':>6} {'速率(s/req)':>12} " \
                f"{'成功':>8} {'成功率':>8} {'平均响应(s)':>12} {'完成时间(s)':>12} {'响应大小(KB)':>14}"
        print(header)
        print("-" * 150)
        
        # 打印数据行
        for stat in statistics:
            row = f"{stat['引擎']:<20} {stat['请求总数']:>8} {stat['并发数']:>6} " \
                  f"{stat['请求速率(s/req)']:>12} {stat['成功次数']:>8} " \
                  f"{stat['成功率(%)']:>7}% {stat['成功平均响应时间(s)']:>12} " \
                  f"{stat['并发完成时间(s)']:>12} {stat['成功平均响应大小(KB)']:>14}"
            print(row)
        
        print("-" * 150)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='SerpAPI性能测试脚本',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 测试单个引擎
  python serpapi_test.py -k YOUR_API_KEY -e google -n 10 -c 5
  
  # 测试多个引擎
  python serpapi_test.py -k YOUR_API_KEY -e google bing yahoo -n 20 -c 10
  
  # 测试所有引擎
  python serpapi_test.py -k YOUR_API_KEY --all-engines -n 10 -c 5
  
  # 启用详细CSV记录
  python serpapi_test.py -k YOUR_API_KEY -e google -n 10 -c 5 --save-details
        """
    )
    
    parser.add_argument('-k', '--api-key', type=str,
                       help='SerpAPI认证密钥')
    parser.add_argument('-e', '--engines', type=str, nargs='+',
                       help='要测试的搜索引擎列表')
    parser.add_argument('--all-engines', action='store_true',
                       help='测试所有支持的引擎')
    parser.add_argument('-n', '--num-requests', type=int, default=10,
                       help='每个引擎的请求数 (默认: 10)')
    parser.add_argument('-c', '--concurrency', type=int, default=5,
                       help='并发数 (默认: 5)')
    parser.add_argument('-q', '--query', type=str,
                       help='搜索关键词 (默认: 随机)')
    parser.add_argument('--save-details', action='store_true',
                       help='保存每个请求的详细CSV记录')
    parser.add_argument('-o', '--output', type=str, 
                       default='serpapi_summary_statistics.csv',
                       help='汇总统计表输出文件名')
    parser.add_argument('--list-engines', action='store_true',
                       help='列出所有支持的引擎')
    
    args = parser.parse_args()
    
    # 列出所有支持的引擎
    if args.list_engines:
        print("支持的搜索引擎:")
        for i, engine in enumerate(SerpAPITester.SUPPORTED_ENGINES, 1):
            print(f"  {i:2d}. {engine}")
        return
    
    # 验证API密钥
    if not args.api_key:
        print("错误: 请使用 -k 或 --api-key 指定API密钥")
        return
    
    # 确定要测试的引擎
    if args.all_engines:
        engines = SerpAPITester.SUPPORTED_ENGINES
        print(f"将测试所有 {len(engines)} 个引擎")
    elif args.engines:
        engines = args.engines
        # 验证引擎是否支持
        invalid_engines = [e for e in engines if e not in SerpAPITester.SUPPORTED_ENGINES]
        if invalid_engines:
            print(f"警告: 以下引擎不在支持列表中: {', '.join(invalid_engines)}")
            print("使用 --list-engines 查看支持的引擎列表")
    else:
        print("错误: 请使用 -e 指定引擎或使用 --all-engines 测试所有引擎")
        print("使用 --list-engines 查看支持的引擎列表")
        return
    
    # 创建测试器
    tester = SerpAPITester(args.api_key, save_details=args.save_details)
    
    # 运行测试
    all_results, all_statistics = tester.run_all_engines_test(
        engines, args.num_requests, args.concurrency
    )
    
    # 保存汇总统计
    tester.save_summary_statistics(all_statistics, args.output)
    
    print("\n测试完成!")


if __name__ == "__main__":
    main()
