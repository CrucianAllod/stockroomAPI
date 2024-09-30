from fastapi import APIRouter, HTTPException, Depends
from schemas.product import Product, ProductCreate
from repositories.product import ProductRepository


router = APIRouter(
    prefix="/products",
    tags=["products"],
)

@router.post("/", response_model=Product)
async def create_product(product: ProductCreate, repository: ProductRepository = Depends()):
    product_id = await repository.add_product(product)
    return await repository.get_product(product_id)

@router.get("/", response_model=list[Product])
async def read_products(repository: ProductRepository = Depends()):
    return await repository.get_products()

@router.get("/{product_id}", response_model= Product)
async def read_product(product_id: int , repository: ProductRepository = Depends()):
    product = await repository.get_product(product_id)
    if not product:
        return HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model= Product)
async def update_product(product_id: int, product: ProductCreate = Depends(), repository: ProductRepository = Depends()):
    update_product = await repository.update_product(product_id, product)
    if not update_product:
        return HTTPException(status_code=404, detail="Product not found")
    return update_product 

@router.delete("/{product_id}", response_model= Product)
async def delete_product(product_id: int, repository: ProductRepository = Depends()):
    success = await repository.delete_product(product_id)
    if not success:
        return HTTPException(status_code=404, detail="Product not found")
    return success
   
    