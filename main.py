from fastapi import FastAPI
from models import Product

app = FastAPI()

@app.get("/")
def greet():
    return("Welcome to Telusko Trac!")

products = [
    Product(id=1, name="Laptop", description="A high-performance laptop", price=999.99, quantity=10),
    Product(id=2, name="Smartphone", description="A latest model smartphone", price=699.99, quantity=25),
    Product(id=3, name="Headphones", description="Noise-cancelling headphones", price=199.99, quantity=15),
    Product(id=4, name="Smartwatch", description="A smartwatch with various features", price=299.99, quantity=30),
    Product(id=5, name="Tablet", description="A lightweight tablet", price=399.99, quantity=20)
]

@app.get("/products")
def get_all_products():
    return(products)


@app.get("/products/{id}")
def get_product_by_id(id: int):
    for product in products:
        if product.id == id:
            return product
    return "Product not found!"

@app.post("/products")
def add_product(new_product: Product):
    products.append(new_product)
    return new_product

@app.put("/products/{id}")
def update_product(id: int, updated_product: Product):
    for index, product in enumerate(products):
        if product.id == id:
            products[index] = updated_product
            return "Product updated successfully!"
    return "Product not found!"

@app.delete("/products/{id}")
def delete_product(id: int):
    for index, product in enumerate(products):
        if product.id == id:
            del products[index]
            return "Product deleted successfully!"
    return "Product not found!"
