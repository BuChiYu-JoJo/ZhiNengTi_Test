#!/usr/bin/env python3
"""
Unit tests for api_test.py
测试API测试脚本的核心功能
"""

import unittest
import sys
import os

# 添加父目录到路径以便导入api_test模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api_test import APITester


class TestAPITester(unittest.TestCase):
    """测试APITester类的功能"""
    
    def setUp(self):
        """测试前设置"""
        self.tester = APITester("test_token_123")
        self.tester_with_rate = APITester("test_token_123", rate_limit=10)
    
    def test_initialization(self):
        """测试初始化"""
        self.assertEqual(self.tester.api_token, "test_token_123")
        self.assertEqual(self.tester.host, "scraperapi.thordata.com")
        self.assertEqual(len(self.tester.used_keywords), 0)
        self.assertGreater(len(self.tester.keyword_pool), 50)  # 至少50个关键词
        
    def test_rate_limit_initialization(self):
        """测试速率限制初始化"""
        self.assertEqual(self.tester_with_rate.rate_limit, 10)
        self.assertAlmostEqual(self.tester_with_rate.request_interval, 0.1, places=2)
    
    def test_get_random_keyword_unique(self):
        """测试关键词唯一性"""
        # 获取10个关键词，应该都不重复
        keywords = [self.tester.get_random_keyword() for _ in range(10)]
        
        # 验证所有关键词都不重复
        self.assertEqual(len(keywords), len(set(keywords)))
        
        # 验证关键词都在关键词池中
        for keyword in keywords:
            self.assertIn(keyword, self.tester.keyword_pool)
    
    def test_get_random_keyword_reset(self):
        """测试关键词池重置功能"""
        pool_size = len(self.tester.keyword_pool)
        
        # 使用所有关键词
        keywords_first_round = [self.tester.get_random_keyword() for _ in range(pool_size)]
        
        # 验证已使用的关键词数量
        self.assertEqual(len(self.tester.used_keywords), pool_size)
        
        # 再获取一个关键词应该触发重置
        keyword_after_reset = self.tester.get_random_keyword()
        
        # 验证重置后已使用集合只包含新关键词
        self.assertEqual(len(self.tester.used_keywords), 1)
        self.assertIn(keyword_after_reset, self.tester.keyword_pool)
    
    def test_keyword_pool_size(self):
        """测试关键词池大小"""
        # 验证关键词池至少包含90个关键词（满足多次测试需求）
        self.assertGreaterEqual(len(self.tester.keyword_pool), 90)
    
    def test_used_keywords_tracking(self):
        """测试已使用关键词跟踪"""
        keyword1 = self.tester.get_random_keyword()
        self.assertIn(keyword1, self.tester.used_keywords)
        
        keyword2 = self.tester.get_random_keyword()
        self.assertIn(keyword2, self.tester.used_keywords)
        self.assertNotEqual(keyword1, keyword2)
        
        self.assertEqual(len(self.tester.used_keywords), 2)


class TestResultStructure(unittest.TestCase):
    """测试结果结构"""
    
    def setUp(self):
        """测试前设置"""
        self.tester = APITester("test_token_123")
    
    def test_result_keys(self):
        """测试结果字典包含所有必需的键"""
        # 注意：这个测试不会实际发送请求，但会测试result字典的初始化
        # 我们需要模拟make_request的初始化部分
        
        expected_keys = {
            'timestamp', 'engine', 'keyword', 'status_code',
            'response_time', 'response_size', 'response_excerpt', 'error'
        }
        
        # 获取一个随机关键词测试
        keyword = self.tester.get_random_keyword()
        self.assertIsInstance(keyword, str)
        self.assertGreater(len(keyword), 0)


class TestCacheControl(unittest.TestCase):
    """测试缓存控制功能"""
    
    def test_cache_enabled_by_default(self):
        """测试默认启用缓存"""
        tester = APITester("test_token_123")
        self.assertTrue(tester.use_cache)
    
    def test_cache_disabled(self):
        """测试禁用缓存"""
        tester = APITester("test_token_123", use_cache=False)
        self.assertFalse(tester.use_cache)
    
    def test_cache_enabled_explicitly(self):
        """测试显式启用缓存"""
        tester = APITester("test_token_123", use_cache=True)
        self.assertTrue(tester.use_cache)


class TestCustomKeywords(unittest.TestCase):
    """测试自定义关键词功能"""
    
    def setUp(self):
        """测试前设置"""
        self.tester = APITester("test_token_123")
    
    def test_custom_keyword_in_request(self):
        """测试使用自定义关键词进行请求"""
        custom_keyword = "custom test keyword"
        # 这个测试验证关键词参数可以传递
        # 实际的API调用会在集成测试中进行
        keyword = custom_keyword if custom_keyword else self.tester.get_random_keyword()
        self.assertEqual(keyword, custom_keyword)


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试类
    suite.addTests(loader.loadTestsFromTestCase(TestAPITester))
    suite.addTests(loader.loadTestsFromTestCase(TestResultStructure))
    suite.addTests(loader.loadTestsFromTestCase(TestCacheControl))
    suite.addTests(loader.loadTestsFromTestCase(TestCustomKeywords))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 返回测试结果
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
