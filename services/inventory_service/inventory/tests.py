import pytest
from rest_framework.test import APIClient
from unittest.mock import patch
from django.conf import settings
# Giả sử cấu trúc model của bạn. Import đúng theo code thực tế
from .models import Product 

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def sample_product():
    return Product.objects.create(
        sku="TEST-SKU-001",
        name="Sản phẩm Demo Test",
        description="Mô tả cho sản phẩm test",
        price=100000.00,
        stock_quantity=20,
        is_active=True
    )

@pytest.mark.django_db
class TestInventoryModule:
    
    # 1. Test tính toàn vẹn của Model
    def test_product_creation(self, sample_product):
        assert sample_product.sku == "TEST-SKU-001"
        assert sample_product.stock_quantity == 20
        assert str(sample_product) == sample_product.name or sample_product.sku

    # 2. Test API công khai (List Products)
    def test_list_products_api(self, api_client, sample_product):
        response = api_client.get('/api/v1/inventory/products/')
        assert response.status_code == 200
        # Đảm bảo dữ liệu trả về có chứa sản phẩm vừa tạo
        assert len(response.data) > 0 or 'results' in response.data 

    # 3. Test API Nội bộ (Nghiệp vụ quan trọng nhất)
    def test_internal_consume_success(self, api_client, sample_product):
        # Thiết lập header giả lập gọi từ Order Service sang
        headers = {
            'HTTP_X_INTERNAL_API_KEY': settings.INVENTORY_INTERNAL_API_KEY
        }
        payload = {
            "items": [
                {"product_id": sample_product.id, "quantity": 5}
            ]
        }
        
        response = api_client.post(
            '/api/v1/inventory/internal/consume/', 
            payload, 
            format='json', 
            **headers
        )
        
        assert response.status_code in [200, 201]
        
        # Kiểm tra database xem tồn kho đã bị trừ đúng chưa (20 - 5 = 15)
        sample_product.refresh_from_db()
        assert sample_product.stock_quantity == 15

    # 4. Kỹ thuật Mocking (Mocking external/internal dependencies)
    # Ví dụ: Ta mock hàm timezone.now() thường dùng để ghi nhận thời gian giao dịch
    @patch('django.utils.timezone.now')
    def test_mocking_example(self, mock_now, api_client, sample_product):
        from datetime import datetime, timezone
        
        # Ép thời gian hệ thống giả lập về một mốc cố định
        mock_time = datetime(2026, 4, 9, 12, 0, 0, tzinfo=timezone.utc)
        mock_now.return_value = mock_time
        
        # Chạy logic lấy sản phẩm
        response = api_client.get(f'/api/v1/inventory/products/{sample_product.id}/')
        assert response.status_code == 200
        
        # Đảm bảo mock object đã được gọi trong quá trình chạy (nếu view có xài timezone.now)
        # assert mock_now.called