from enum import Enum
from fastapi import FastAPI
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, HttpUrl
from curl_cffi import requests
import uuid


class SimpleSession:

    def __init__(self):
        self.session = requests.Session()

    def get(self, url: str, headers: Optional[Dict[str, str]] = None, **kwargs):
        return self.session.get(str(url), headers=headers, **kwargs)

    def post(self, url: str, json: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None, **kwargs):
        return self.session.post(str(url), headers=headers, json=json, **kwargs)

    def close(self):
        self.session.close()


class ProxyProtocol(Enum):
    HTTP = "http"
    HTTPS = "https"
    SOCKS4 = "socks4"
    SOCKS5 = "socks5"


class Proxy(BaseModel):
    protocol: ProxyProtocol
    url: str
    username: Optional[str]
    password: Optional[str]


class Impersonate(Enum):
    chrome99 = "chrome99"
    chrome100 = "chrome100"
    chrome101 = "chrome101"
    chrome104 = "chrome104"
    chrome107 = "chrome107"
    chrome110 = "chrome110"
    chrome99_android = "chrome99_android"
    edge99 = "edge99"
    edge101 = "edge101"
    safari15_3 = "safari15_3"
    safari15_5 = "safari15_5"


class SessionCreateRequest(BaseModel):
    impersonate: Impersonate
    session: Optional[str] = None
    proxy: Optional[Proxy] = None


class SessionData:
    session: SimpleSession
    cookies: Optional[Dict[str, Any]]
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


class cURLsolverrManager:
    def __init__(self):
        self.sessions = {}

    def create_session(self, impersonate: Impersonate, session_id: Optional[str] = None, proxy: Optional[Proxy] = None) -> str:
        if not session_id:
            session_id = str(uuid.uuid4())

        simple_session = SimpleSession()
        if proxy:
            simple_session.session.proxies = self.__get_proxies(proxy)

        if impersonate:
            simple_session.session.impersonate = str(impersonate.value)

        self.sessions[session_id] = {
            "session": simple_session,
            "cookies": {},
            "proxy": proxy
        }
        return {"sessionId": session_id, "proxy": proxy}

    def list_sessions(self) -> List[str]:
        return self.sessions

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
            response = simple_session.get(
                url, headers=headers, ** kwargs)
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
            return {"PostError": str(e)}

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

    def __get_proxies(self, proxy: Proxy) -> Optional[Dict[str, str]]:
        if not proxy:
            return None

        proxy_url = str(proxy.url)
        if proxy.username and proxy.password:
            return {"https": f"{proxy.protocol.value}://{proxy.username}:{proxy.password}@{proxy_url}"}
        return {"https": f"{proxy.protocol.value}://{proxy_url}"}


app = FastAPI()

curlManager = cURLsolverrManager()


@app.post("/v1/session/")
def create_session(request: Optional[SessionCreateRequest] = None):
    session_id = None
    proxy = None
    impersonate = None
    if request:
        impersonate = request.impersonate
        session_id = request.session
        proxy = request.proxy
    session_id = curlManager.create_session(
        session_id=session_id, proxy=proxy, impersonate=impersonate)
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
