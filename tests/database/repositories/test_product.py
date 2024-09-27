from typing import Sequence
import pytest

from backend.database.gateway import DBGateway
from backend.database.models.product import ProductModel


class TestProductRepository:
    @pytest.mark.asyncio
    async def test_select_products(self, gateway: DBGateway, products : Sequence[ProductModel]):
        for product in products:
            db_product = await gateway.product().get_one(product.id)
            
            assert db_product.title == product.title
            assert db_product.description == product.description
            assert db_product.price == product.price
    
    @pytest.mark.asyncio
    async def test_select_all(self, gateway: DBGateway, products : Sequence[ProductModel]):
        db_products = await gateway.product().get_all()
        
        assert len(db_products) == len(products)
        
    @pytest.mark.asyncio
    async def test_delete_products(self, gateway: DBGateway, products : Sequence[ProductModel]):
        assert all([await gateway.product().delete(product.id) for product in products]) is True