from typing import Union
from fastapi import FastAPI, HTTPException
from expertApi.expertApiWrapper import ExpertAPIWrapper
from pydantic import BaseModel

app = FastAPI()

@app.get("/getAllExpertStores")
def get_expert_stores():
    wrapper = ExpertAPIWrapper()
    try:
        return wrapper.expert_stores()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/getArticleByWebcode")
class ArticleNumberRequest(BaseModel):
    article_nr: int
def get_article(request: ArticleNumberRequest):
    wrapper = ExpertAPIWrapper()
    try:
        return wrapper.get_article_by_number(request.article_nr)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/getArticleData")
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

    
