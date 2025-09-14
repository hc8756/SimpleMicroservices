from __future__ import annotations

import os
import socket
from datetime import datetime

from typing import Dict, List

from fastapi import FastAPI, HTTPException
from fastapi import Query, Path
from typing import Optional

from models.product import ProductCreate, ProductRead, ProductUpdate
from models.business import BusinessCreate, BusinessRead, BusinessUpdate
from models.health import Health

port = int(os.environ.get("FASTAPIPORT", 8000))

# -----------------------------------------------------------------------------
# Fake in-memory "databases"
# -----------------------------------------------------------------------------
businesses: Dict[str, BusinessRead] = {}
products: Dict[int, ProductRead] = {}

app = FastAPI(
    title="Product/Business API",
    description="Demo FastAPI app using Pydantic v2 models for Product and Business",
    version="0.1.0",
)

# -----------------------------------------------------------------------------
# Business endpoints
# -----------------------------------------------------------------------------

def make_health(echo: Optional[str], path_echo: Optional[str]=None) -> Health:
    return Health(
        status=200,
        status_message="OK",
        timestamp=datetime.utcnow().isoformat() + "Z",
        ip_address=socket.gethostbyname(socket.gethostname()),
        echo=echo,
        path_echo=path_echo
    )

@app.get("/health", response_model=Health)
def get_health_no_path(echo: str | None = Query(None, description="Optional echo string")):
    # Works because path_echo is optional in the model
    return make_health(echo=echo, path_echo=None)

@app.get("/health/{path_echo}", response_model=Health)
def get_health_with_path(
    path_echo: str = Path(..., description="Required echo in the URL path"),
    echo: str | None = Query(None, description="Optional echo string"),
):
    return make_health(echo=echo, path_echo=path_echo)

@app.post("/businesses", response_model=BusinessRead, status_code=201)
def create_business(business: BusinessCreate):
    if business.ein in businesses:
        raise HTTPException(status_code=400, detail="Business with this EIN already exists")
    businesses[business.ein] = BusinessRead(**business.model_dump())
    return businesses[business.ein]

@app.get("/businesses", response_model=List[BusinessRead])
def list_businesses(
    ein: Optional[str] = Query(None, description="Filter by EIN"),
    name: Optional[str] = Query(None, description="Filter by business name"),
    email: Optional[str] = Query(None, description="Filter by email"),
    phone: Optional[str] = Query(None, description="Filter by phone number"),
):
    results = list(businesses.values())

    if ein is not None:
        results = [b for b in results if b.ein == ein]
    if name is not None:
        results = [b for b in results if b.name == name]
    if email is not None:
        results = [b for b in results if b.email == email]
    if phone is not None:
        results = [b for b in results if b.phone == phone]

    return results

@app.get("/businesses/{business_ein}", response_model=BusinessRead)
def get_business(business_ein: str):
    if business_ein not in businesses:
        raise HTTPException(status_code=404, detail="Business not found")
    return businesses[business_ein]

@app.patch("/businesses/{business_ein}", response_model=BusinessRead)
def update_business(business_ein: str, update: BusinessUpdate):
    if business_ein not in businesses:
        raise HTTPException(status_code=404, detail="Business not found")
    stored = businesses[business_ein].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    businesses[business_ein] = BusinessRead(**stored)
    return businesses[business_ein]

@app.delete("/businesses/{ein}", status_code=204)
def delete_business(ein: str):
    if ein not in businesses:
        raise HTTPException(status_code=404, detail="Business not found")
    del businesses[ein]
    return None

# -----------------------------------------------------------------------------
# Product endpoints
# -----------------------------------------------------------------------------
@app.post("/products", response_model=ProductRead, status_code=201)
def create_product(product: ProductCreate):
    if product.product_id in products:
        raise HTTPException(status_code=400, detail="Product with this ID already exists")
    product_read = ProductRead(**product.model_dump())
    products[product_read.product_id] = product_read
    return product_read

@app.get("/products", response_model=List[ProductRead])
def list_products(
        product_id: Optional[int] = Query(None, description="Filter by product ID"),
        name: Optional[str] = Query(None, description="Filter by product name"),
        business_ein: Optional[str] = Query(None, description="Filter by business EIN"),
        business_name: Optional[str] = Query(None, description="Filter by business name"),
):
    results = list(products.values())

    if product_id is not None:
        results = [p for p in results if p.product_id == product_id]
    if name is not None:
        results = [p for p in results if p.name == name]
    if business_ein is not None:
        results = [p for p in results if p.business.ein == business_ein]
    if business_name is not None:
        results = [p for p in results if p.business.name == business_name]

    return results

@app.get("/products/{product_id}", response_model=ProductRead)
def get_product(product_id: int):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    return products[product_id]

@app.patch("/products/{product_id}", response_model=ProductRead)
def update_product(product_id: int, update: ProductUpdate):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    stored = products[product_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    products[product_id] = ProductRead(**stored)
    return products[product_id]

@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    del products[product_id]
    return None

# -----------------------------------------------------------------------------
# Root
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Welcome to the Product/Business API. See /docs for OpenAPI UI."}

# -----------------------------------------------------------------------------
# Entrypoint for `python main.py`
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
