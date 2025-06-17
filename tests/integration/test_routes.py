import unittest
from app.core import create_app
from app.core.config import TestingConfig


class TestRoutes(unittest.TestCase):
    """Integration tests for routes"""

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_home_route(self):
        """Test home page route"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.data)

    def test_about_route(self):
        """Test about page route"""
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'About This Project', response.data)

    def test_products_route(self):
        """Test products page route"""
        response = self.client.get('/products')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Product Catalog', response.data)

    def test_products_with_category_filter(self):
        """Test products page with category filter"""
        response = self.client.get('/products?category=Electronics')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Product Catalog', response.data)

    def test_product_detail_route(self):
        """Test product detail page route"""
        response = self.client.get('/products/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Product Details', response.data)

    def test_product_detail_not_found(self):
        """Test product detail page with non-existent product"""
        response = self.client.get('/products/999')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()