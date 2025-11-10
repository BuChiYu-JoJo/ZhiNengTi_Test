#!/usr/bin/env python3
"""
API Test Script for ScraperAPI
This script tests the ScraperAPI service with dynamic parameters and logs results to CSV.
"""

import http.client
import csv
import time
import json
import random
import argparse
from urllib.parse import urlencode
from datetime import datetime


class APITester:
    """API测试类，用于测试ScraperAPI并记录结果"""
    
    def __init__(self, api_token):
        """
        初始化API测试器
        
        Args:
            api_token: API认证令牌
        """
        self.api_token = api_token
        self.host = "scraperapi.thordata.com"
        self.used_keywords = set()
        
        # 预定义的关键词池，确保每次请求使用不同的关键词
        self.keyword_pool = [
            "pizza", "burger", "sushi", "pasta", "tacos",
            "coffee", "tea", "juice", "smoothie", "sandwich",
            "salad", "soup", "steak", "chicken", "fish",
            "dessert", "cake", "ice cream", "chocolate", "cookies",
            "bread", "cheese", "wine", "beer", "cocktail",
            "restaurant", "cafe", "bakery", "diner", "bistro",
            "breakfast", "lunch", "dinner", "brunch", "snack",
            "healthy food", "fast food", "street food", "gourmet", "organic",
            "vegan", "vegetarian", "gluten free", "keto", "paleo",
            "chinese food", "italian food", "mexican food", "japanese food", "thai food",
            "indian food", "french food", "greek food", "korean food", "vietnamese food",
            "seafood", "barbecue", "grilled", "fried", "baked",
            "noodles", "rice", "curry", "dumplings", "ramen",
            "burger joint", "pizza place", "taco shop", "noodle bar", "sushi bar",
            "food delivery", "takeout", "dine in", "catering", "meal prep",
            "farm to table", "local food", "authentic cuisine", "fusion food", "comfort food",
            "fine dining", "casual dining", "buffet", "food truck", "pop up restaurant",
            "artisan bread", "craft beer", "specialty coffee", "fresh juice", "homemade food",
            "seasonal menu", "chef special", "signature dish", "house made", "daily special",
            "appetizers", "main course", "side dishes", "combo meal", "family meal",
            "kids menu", "late night food", "weekend brunch", "happy hour", "all day breakfast",
            "food near me", "best restaurant", "top rated", "highly recommended", "must try",
            "new restaurant", "local favorite", "hidden gem", "popular spot", "trending food"
        ]
        
    def get_random_keyword(self):
        """
        获取随机且未使用过的关键词
        
        Returns:
            str: 随机关键词
        """
        available_keywords = [kw for kw in self.keyword_pool if kw not in self.used_keywords]
        
        if not available_keywords:
            # 如果所有关键词都用过了，重置已使用集合
            self.used_keywords.clear()
            available_keywords = self.keyword_pool.copy()
        
        keyword = random.choice(available_keywords)
        self.used_keywords.add(keyword)
        return keyword
    
    def make_request(self, engine, keyword=None):
        """
        发送API请求
        
        Args:
            engine: 搜索引擎类型 (如: google, bing, yahoo等)
            keyword: 搜索关键词，如果为None则随机生成
            
        Returns:
            dict: 包含请求结果的字典
        """
        if keyword is None:
            keyword = self.get_random_keyword()
        
        result = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'engine': engine,
            'keyword': keyword,
            'status_code': None,
            'response_time': None,
            'response_size': None,
            'response_excerpt': '',
            'error': ''
        }
        
        try:
            # 准备请求参数
            params = {
                "engine": engine,
                "q": keyword,
                "json": "1"
            }
            payload = urlencode(params)
            
            headers = {
                'Authorization': f'Bearer {self.api_token}',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            # 记录开始时间
            start_time = time.time()
            
            # 建立连接并发送请求
            conn = http.client.HTTPSConnection(self.host)
            conn.request("POST", "/request", payload, headers)
            
            # 获取响应
            res = conn.getresponse()
            result['status_code'] = res.status
            
            # 读取响应数据
            data = res.read()
            result['response_time'] = round(time.time() - start_time, 3)
            result['response_size'] = len(data)
            
            # 解析响应内容
            try:
                response_text = data.decode("utf-8")
                # 截取前200个字符作为摘要
                result['response_excerpt'] = response_text[:200].replace('\n', ' ').replace('\r', '')
            except Exception as e:
                result['response_excerpt'] = f"Failed to decode response: {str(e)}"
            
            conn.close()
            
        except Exception as e:
            result['error'] = str(e)
            result['response_time'] = round(time.time() - start_time, 3) if 'start_time' in locals() else 0
        
        return result
    
    def save_to_csv(self, results, filename='test_results.csv'):
        """
        将测试结果保存到CSV文件
        
        Args:
            results: 测试结果列表
            filename: CSV文件名
        """
        if not results:
            return
        
        fieldnames = ['timestamp', 'engine', 'keyword', 'status_code', 'response_time', 
                     'response_size', 'response_excerpt', 'error']
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        
        print(f"\n测试结果已保存到: {filename}")
    
    def run_tests(self, engine, num_requests=5, output_file='test_results.csv'):
        """
        运行多次测试
        
        Args:
            engine: 搜索引擎类型
            num_requests: 请求次数
            output_file: 输出CSV文件名
        """
        print(f"开始测试 {engine} 引擎，共 {num_requests} 次请求...")
        print("-" * 80)
        
        results = []
        
        for i in range(num_requests):
            print(f"\n请求 {i+1}/{num_requests}:")
            result = self.make_request(engine)
            results.append(result)
            
            # 打印请求结果
            print(f"  时间戳: {result['timestamp']}")
            print(f"  引擎: {result['engine']}")
            print(f"  关键词: {result['keyword']}")
            print(f"  状态码: {result['status_code']}")
            print(f"  响应时间: {result['response_time']}秒")
            print(f"  响应大小: {result['response_size']}字节")
            if result['error']:
                print(f"  错误: {result['error']}")
            else:
                print(f"  响应摘要: {result['response_excerpt'][:100]}...")
            
            # 短暂延迟避免请求过快
            if i < num_requests - 1:
                time.sleep(1)
        
        # 保存结果到CSV
        self.save_to_csv(results, output_file)
        
        # 打印统计信息
        self._print_statistics(results)
    
    def _print_statistics(self, results):
        """打印测试统计信息"""
        print("\n" + "=" * 80)
        print("测试统计:")
        print("=" * 80)
        
        total_requests = len(results)
        successful_requests = sum(1 for r in results if r['status_code'] and r['status_code'] == 200)
        failed_requests = total_requests - successful_requests
        
        avg_response_time = sum(r['response_time'] for r in results if r['response_time']) / total_requests if total_requests > 0 else 0
        total_data_size = sum(r['response_size'] for r in results if r['response_size'])
        
        print(f"总请求数: {total_requests}")
        print(f"成功请求: {successful_requests}")
        print(f"失败请求: {failed_requests}")
        print(f"平均响应时间: {avg_response_time:.3f}秒")
        print(f"总数据大小: {total_data_size}字节")
        print("=" * 80)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='ScraperAPI测试脚本')
    parser.add_argument('-e', '--engine', type=str, default='google',
                       help='搜索引擎类型 (默认: google)')
    parser.add_argument('-n', '--num-requests', type=int, default=5,
                       help='请求次数 (默认: 5)')
    parser.add_argument('-o', '--output', type=str, default='test_results.csv',
                       help='输出CSV文件名 (默认: test_results.csv)')
    parser.add_argument('-t', '--token', type=str, 
                       default='663fba4eb51f1fb2ec007f1b7bd73f16',
                       help='API认证令牌')
    
    args = parser.parse_args()
    
    # 创建测试器并运行测试
    tester = APITester(args.token)
    tester.run_tests(args.engine, args.num_requests, args.output)


if __name__ == "__main__":
    main()
