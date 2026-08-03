from fastapi import FastAPI
from database import engine, Base
from routers import user, customer, supplier, category, product, sale, sale_item, payment, receipt

app = FastAPI(title="Coffee Shop POS")


Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(customer.router)
app.include_router(supplier.router)
app.include_router(category.router)
app.include_router(product.router)
app.include_router(sale.router)
app.include_router(sale_item.router)
app.include_router(payment.router)
app.include_router(receipt.router)