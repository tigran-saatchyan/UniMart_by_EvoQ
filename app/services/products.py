"""Service class for handling product-related operations."""

from app.api.v1.dependencies import UOWDependency
from app.models import User
from app.schemas.products import ProductsCreate, ProductsUpdate


class ProductsService:
    """Service class for handling product-related operations."""

    @staticmethod
    async def add(
        uow: UOWDependency, product: ProductsCreate, user: User
    ) -> int:
        """Add a new product.

        Args:
            uow (UOWDependency): The unit of work dependency.
            product (ProductsCreate): The product creation schema.
            user (User): The user adding the product.

        Returns:
            int: The ID of the added product.

        Raises:
            HTTPException: If the product addition fails.
        """
        product_dict = product.model_dump()
        product_dict["owner_id"] = user.id
        async with uow:
            product_id = await uow.products.add(product_dict)
            await uow.commit()
            return product_id

    @staticmethod
    async def get_all(uow: UOWDependency, user: User):
        """Get all products for a given user.

        Args:
            uow (UOWDependency): The unit of work dependency.
            user (User): The user for whom to retrieve products.

        Returns:
            List[Product]: The list of products.

        Raises:
            HTTPException: If the product retrieval fails.
        """
        async with uow:
            return await uow.products.get_all(user)

    @staticmethod
    async def get(uow: UOWDependency, product_id: int, user: User):
        """Get a specific product by ID for a given user.

        Args:
            uow (UOWDependency): The unit of work dependency.
            product_id (int): The ID of the product to retrieve.
            user (User): The user for whom to retrieve the product.

        Returns:
            Product: The retrieved product.

        Raises:
            HTTPException: If the product retrieval fails or the
                product is not found.
        """
        async with uow:
            return await uow.products.get(product_id, user)

    @staticmethod
    async def update(
        uow: UOWDependency,
        product_id: int,
        product: ProductsUpdate,
        user: User,
    ):
        """Update a specific product by ID for a given user.

        Args:
            uow (UOWDependency): The unit of work dependency.
            product_id (int): The ID of the product to update.
            product (ProductsUpdate): The updated product information.
            user (User): The user performing the update.

        Returns:
            int: The ID of the updated product.

        Raises:
            HTTPException: If the product update fails or the
                product is not found.
        """
        product_dict = product.model_dump()
        async with uow:
            await uow.products.update(product_id, product_dict, user)
            await uow.commit()
            return product_id

    @staticmethod
    async def delete(uow: UOWDependency, product_id: int, user: User):
        """Delete a specific product by ID for a given user.

        Args:
            uow (UOWDependency): The unit of work dependency.
            product_id (int): The ID of the product to delete.
            user (User): The user performing the deletion.

        Returns:
            bool: True if the deletion is successful.

        Raises:
            HTTPException: If the product deletion fails or the
                product is not found.
        """
        async with uow:
            result = await uow.products.delete(product_id, user)
            await uow.commit()
            return result
