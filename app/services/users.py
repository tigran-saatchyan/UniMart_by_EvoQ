from app.api.v1.dependencies import UOWDependency
from app.schemas.users import UsersSchemaAdd
from app.utils.utils import hash_password


class UsersService:
    @staticmethod
    async def add(uow: UOWDependency, user: UsersSchemaAdd) -> int:
        user.validate_data()
        user_dict = user.model_dump()
        user_dict.pop("confirm_password")
        user_dict.update(hash_password(user_dict.pop("password")))
        async with uow:
            await uow.users.is_exists(user_dict)

            user_id = await uow.users.add(user_dict)
            await uow.commit()
            return user_id

    # @staticmethod
    # async def get_all(uow: UOWDependency):
    #     async with uow:
    #         return await uow.products.get_all()
    #
    # @staticmethod
    # async def get(uow: UOWDependency, product_id: int):
    #     async with uow:
    #         return await uow.products.get(product_id)

    # @staticmethod
    # async def update(
    #     uow: UOWDependency, product_id: int, product: ProductsSchemaEdit
    # ):
    #     product_dict = product.model_dump()
    #     async with uow:
    #         await uow.products.update(product_id, product_dict)
    #         await uow.commit()
    #         return product_id
    #
    # @staticmethod
    # async def delete(uow: UOWDependency, product_id: int):
    #     async with uow:
    #         await uow.products.delete(product_id)
    #         await uow.commit()


#
# def is_valid_password(password: str, confirm_password: str) -> bool:
#     if password != confirm_password:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Passwords do not match",
#         )
#     validator = PasswordValidator()
#     validator(password)
#     return True
