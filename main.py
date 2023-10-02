from enum import Enum
from fastapi import FastAPI
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, HttpUrl
from curl_cffi import requests
import uuid


class SimpleSession:

    def __init__(self):
        self.session = requests.Session()

    def get(self, url: str, headers: Optional[Dict[str, str]] = None, impersonate: Optional[str] = "chrome110", **kwargs):
        return self.session.get(str(url), headers=headers, impersonate=impersonate, **kwargs)

    def post(self, url: str, json: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None, impersonate: Optional[str] = "chrome110", **kwargs):
        return self.session.post(str(url), headers=headers, json=json, impersonate=impersonate, **kwargs)

    def close(self):
        self.session.close()


class SessionData:
    session: SimpleSession
    cookies: Dict[str, Any]
    proxy: Optional[Dict[str, Any]]


class cURLsolverrManager:
    def __init__(self):
        self.sessions = {}

    def create_session(self, session_id: Optional[str] = None, proxy: Optional[Dict] = None) -> str:
        if not session_id:
            session_id = str(uuid.uuid4())

        simple_session = SimpleSession()
        if proxy:
            simple_session.session.proxies = proxy

        self.sessions[session_id] = {
            "session": simple_session,
            "cookies": {},
            "proxy": proxy
        }
        return session_id

    def list_sessions(self) -> List[str]:
        return list(self.sessions.keys())

    def destroy_session(self, session_id: str) -> None:
        if session_id in self.sessions:
            self.sessions[session_id]["session"].close()
            del self.sessions[session_id]

    def get_request(self, url: str, session_id: Optional[str] = None, headers: Optional[Dict[str, str]] = None, **kwargs) -> Dict:
        if session_id not in self.sessions:
            return {"error": "Invalid session ID"}

        session_data: SessionData = self.sessions[session_id]
        simple_session: SimpleSession = session_data["session"]

        try:
            response = simple_session.get(url, headers=headers, ** kwargs)
        except Exception as e:  # Adjusted error handling
            return {"error": str(e)}

        # Store the cookies from the response
        if session_id:
            self.sessions[session_id]["cookies"] = response.cookies

        return {
            "url": response.url,
            "status": response.status_code,
            "headers": dict(response.headers),
            "cookies": dict(response.cookies),
            "response": response.content
        }

    def post_request(self, url: str, data: Dict[str, Any], session_id: Optional[str] = None, headers: Optional[Dict[str, str]] = None, **kwargs) -> Dict:
        if session_id not in self.sessions:
            return {"error": "Invalid session ID"}

        session_data: SessionData = self.sessions[session_id]
        simple_session: SimpleSession = session_data["session"]

        try:
            response = simple_session.post(
                url, json=data, headers=headers, **kwargs)
        except Exception as e:  # Adjusted error handling
            return {"error": str(e)}

        # Store the cookies from the response
        if session_id:
            self.sessions[session_id]["cookies"] = response.cookies

        return {
            "url": response.url,
            "status": response.status_code,
            "headers": dict(response.headers),
            "cookies": dict(response.cookies),
            "response": response.content
        }


app = FastAPI()

curlManager = cURLsolverrManager()


class Proxy(BaseModel):
    url: HttpUrl
    username: Optional[str]
    password: Optional[str]


class SessionCreateRequest(BaseModel):
    session: Optional[str]
    proxy: Optional[Proxy]


class SessionDestroyRequest(BaseModel):
    session: str


class HttpMethod(str, Enum):
    GET = "GET"
    POST = "POST"


class Request(BaseModel):
    method: HttpMethod
    url: HttpUrl
    session: str
    headers: Optional[Dict[str, Any]] = None
    postData: Optional[Dict[str, Any]] = None
    returnOnlyCookies: Optional[bool] = False


@app.post("/v1/session/")
def create_session(request: Optional[SessionCreateRequest] = None):
    session_id = None
    proxy = None
    if request:
        session_id = request.session
        proxy = request.proxy
    session_id = curlManager.create_session(
        session_id=session_id, proxy=proxy)
    return {"session": session_id}


@app.get("/v1/session/")
def list_sessions():
    return {"sessions": curlManager.list_sessions()}


@app.delete("/v1/session/{session_id}")
def destroy_session(session_id: str):
    curlManager.destroy_session(session_id)
    return {"status": "ok"}


@app.post("/v1/request/")
def make_get_or_post_request(request: Request):
    method = request.method
    response = None

    switcher = {
        HttpMethod.GET: lambda: curlManager.get_request(request.url, headers=request.headers, session_id=request.session),
        HttpMethod.POST: lambda: curlManager.post_request(
            request.url, data=request.postData, headers=request.headers, session_id=request.session)
    }

    func = switcher.get(method, lambda: {"error": "Invalid method"})
    response = func()

    if request.returnOnlyCookies:
        return {"cookies": response["cookies"]}
    return response
