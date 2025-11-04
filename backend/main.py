from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from sqlalchemy.orm import Session

from database import session, engine
import database_models

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
)

database_models.Base.metadata.create_all(bind=engine)

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

# def init_db():
#     session = Session(bind=engine)
#     for product in products:
#         db_product = database_models.Product(
#             id=product.id,
#             name=product.name,
#             description=product.description,
#             price=product.price,
#             quantity=product.quantity
#         )
#         session.add(db_product)
#     session.commit()
#     session.close()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = session()

    count = db.query(database_models.Product).count()

    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()

init_db()

@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()

    return(db_products)


@app.get("/products/{id}")
def get_product_by_id(id: int,db: Session = Depends(get_db)):
                                                
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()

    if db_product:
        return db_product
    
    return "Product not found!"

@app.post("/products")
def add_product(new_product: Product, db: Session = Depends(get_db)):
    db_product = database_models.Product(**new_product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.put("/products/{id}")
def update_product(id: int, updated_product: Product, db: Session = Depends(get_db)):
   
        db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
        if db_product:
            db_product.name = updated_product.name
            db_product.description = updated_product.description
            db_product.price = updated_product.price
            db_product.quantity = updated_product.quantity
            db.commit()
            db.refresh(db_product)
            return db_product
        return "Product not found!"

@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()

    if db_product:
        db.delete(db_product)
        db.commit()
        return f"Product with id {id} has been deleted."
    return "Product not found!"
