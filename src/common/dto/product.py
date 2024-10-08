from src.common.dto.base import DTO


class ProductSchema(DTO):
    title: str
    description: str
    price: int


class ProductId(DTO):
    id: int


class Product(ProductSchema, ProductId):
    pass


class CreateProductQuery(ProductSchema):
    pass


class UpdateProductQuery(ProductSchema, ProductId):
    pass


class GetProductQuery(ProductId):
    pass


class GetAllProductsQuery(DTO):
    pass


class DeleteProductQuery(ProductId):
    pass
