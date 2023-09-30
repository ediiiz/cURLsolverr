from typing import Union
from fastapi import FastAPI, HTTPException
from expertApi.expertApiWrapper import ExpertAPIWrapper
from pydantic import BaseModel


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/expertStores")
def get_expert_stores():
    wrapper = ExpertAPIWrapper()
    try:
        return wrapper.expert_stores()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/getArticle")
class ArticleNumberRequest(BaseModel):
    article_nr: int
def get_article(request: ArticleNumberRequest):
    wrapper = ExpertAPIWrapper()
    try:
        return wrapper.get_article_by_number(request.article_nr)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/productInfo")
class ProductInfoRequest(BaseModel):
    store_id: str
    store_name: str
    article_id: str
def get_product_info(request: ProductInfoRequest):
    wrapper = ExpertAPIWrapper()
    try:
        return wrapper.fetch_product_information(request.store_id, request.store_name, request.article_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    
