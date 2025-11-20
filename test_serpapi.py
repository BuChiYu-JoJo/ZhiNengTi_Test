#!/usr/bin/env python3
"""
Unit tests for serpapi_test.py
测试SerpAPI性能测试脚本的核心功能
"""

import unittest
import sys
import os

# 添加父目录到路径以便导入serpapi_test模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from serpapi_test import SerpAPITester


class TestSerpAPITester(unittest.TestCase):
    """测试SerpAPITester类的功能"""
    
    def setUp(self):
        """测试前设置"""
        self.tester = SerpAPITester("test_api_key_123")
        self.tester_with_details = SerpAPITester("test_api_key_123", save_details=True)
    
    def test_initialization(self):
        """测试初始化"""
        self.assertEqual(self.tester.api_key, "test_api_key_123")
        self.assertEqual(self.tester.host, "serpapi.com")
        self.assertFalse(self.tester.save_details)
        self.assertGreater(len(self.tester.keyword_pool), 10)
        
    def test_initialization_with_details(self):
        """测试带详细记录的初始化"""
        self.assertTrue(self.tester_with_details.save_details)
    
    def test_supported_engines(self):
        """测试支持的引擎列表"""
        self.assertGreater(len(SerpAPITester.SUPPORTED_ENGINES), 20)
        self.assertIn('google', SerpAPITester.SUPPORTED_ENGINES)
        self.assertIn('bing', SerpAPITester.SUPPORTED_ENGINES)
        self.assertIn('yahoo', SerpAPITester.SUPPORTED_ENGINES)
    
    def test_is_response_successful_with_results(self):
        """测试成功响应判断 - 包含结果"""
        response = {
            'search_information': {'total_results': '1000'},
            'organic_results': [
                {'title': 'Test', 'link': 'http://example.com'}
            ]
        }
        self.assertTrue(self.tester._is_response_successful(response, 200))
    
    def test_is_response_successful_with_error(self):
        """测试失败响应判断 - 包含错误"""
        response = {
            'error': 'Invalid API key'
        }
        self.assertFalse(self.tester._is_response_successful(response, 200))
    
    def test_is_response_successful_bad_status(self):
        """测试失败响应判断 - 错误状态码"""
        response = {
            'organic_results': []
        }
        self.assertFalse(self.tester._is_response_successful(response, 401))
    
    def test_is_response_successful_no_results(self):
        """测试失败响应判断 - 无结果字段"""
        response = {
            'search_parameters': {'q': 'test'}
        }
        self.assertFalse(self.tester._is_response_successful(response, 200))
    
    def test_extract_error_message(self):
        """测试错误信息提取"""
        response = {
            'error': 'API key is invalid'
        }
        error = self.tester._extract_error_message(response)
        self.assertEqual(error, 'API key is invalid')
    
    def test_extract_error_message_no_error(self):
        """测试错误信息提取 - 无错误字段"""
        response = {}
        error = self.tester._extract_error_message(response)
        self.assertIn('Unknown', error)
    
    def test_extract_response_summary(self):
        """测试响应摘要提取"""
        response = {
            'search_information': {'total_results': '1000'},
            'organic_results': [1, 2, 3],
            'shopping_results': [1, 2]
        }
        summary = self.tester._extract_response_summary(response)
        self.assertIn('total_results:1000', summary)
        self.assertIn('organic:3', summary)
        self.assertIn('shopping:2', summary)
    
    def test_extract_response_summary_empty(self):
        """测试响应摘要提取 - 空响应"""
        response = {}
        summary = self.tester._extract_response_summary(response)
        self.assertEqual(summary, 'Success')
    
    def test_calculate_statistics(self):
        """测试统计计算"""
        results = [
            {'success': True, 'response_time': 1.0, 'response_size': 10.0},
            {'success': True, 'response_time': 2.0, 'response_size': 20.0},
            {'success': False, 'response_time': 0.5, 'response_size': 5.0},
        ]
        
        stats = self.tester._calculate_statistics(
            'SerpAPI', 'google', results, 3, 5, 3.0
        )
        
        self.assertEqual(stats['产品类别'], 'SerpAPI')
        self.assertEqual(stats['引擎'], 'google')
        self.assertEqual(stats['请求总数'], 3)
        self.assertEqual(stats['并发数'], 5)
        self.assertEqual(stats['成功次数'], 2)
        self.assertEqual(stats['成功率(%)'], 66.67)
        self.assertEqual(stats['成功平均响应时间(s)'], 1.5)
        self.assertEqual(stats['成功平均响应大小(KB)'], 15.0)


class TestResponseValidation(unittest.TestCase):
    """测试响应验证功能"""
    
    def setUp(self):
        """测试前设置"""
        self.tester = SerpAPITester("test_key")
    
    def test_various_result_types(self):
        """测试各种结果类型的识别"""
        result_types = [
            'organic_results', 'shopping_results', 'images_results',
            'videos_results', 'news_results', 'local_results',
            'jobs_results', 'scholar_results'
        ]
        
        for result_type in result_types:
            response = {result_type: [{'data': 'test'}]}
            self.assertTrue(
                self.tester._is_response_successful(response, 200),
                f"Should recognize {result_type} as success"
            )


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试类
    suite.addTests(loader.loadTestsFromTestCase(TestSerpAPITester))
    suite.addTests(loader.loadTestsFromTestCase(TestResponseValidation))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 返回测试结果
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
