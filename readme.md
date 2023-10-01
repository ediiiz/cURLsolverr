# cURLsolverrManager

## Introduction

The `cURLsolverrManager` is a FastAPI application designed to create and manage `SimpleSession` objects, which are essentially HTTP sessions with extended functionalities. The manager allows users to make GET and POST requests using created sessions, which can optionally be configured with a proxy. 

## How to Use

### 1. Starting the FastAPI application:

```bash
uvicorn filename:app --reload
```
Replace `filename` with the name of the python file containing the FastAPI application.

### 2. Creating a new session:

To create a new session, you can make a POST request:

```javascript
const response = await fetch("/v1/sessions/", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    proxy: {  // Optional
      url: "http://your_proxy_url",
      username: "your_username",  // Optional
      password: "your_password"  // Optional
    }
  })
});
const data = await response.json();
console.log(data);  // Expected output: { "session": "generated_session_id" }
```

### 3. Making a GET request:

To make a GET request using a session:

```javascript
const response = await fetch("/v1/request/", {
  method: "GET",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    url: "http://your_target_url",
    session: "your_session_id",  // Optional
    headers: {  // Optional
      "Header-Name": "Header-Value"
    }
    // Other optional parameters: session_ttl_minutes, maxTimeout, cookies, returnOnlyCookies, proxy
  })
});
const data = await response.json();
console.log(data); 
```

**Expected Output:** A JSON object containing the response details such as `url`, `status`, `headers`, `response` (HTML content), and `cookies`.

```json
{
  "url": "https://www.example.com/",
  "status": 200,
  "headers": {...},
  "response": "<!DOCTYPE html><html>...</html>",
  "cookies": [
    {
      "name": "cookie_name",
      "value": "cookie_value",
      ...
    },
    ...
  ],
  ...
}
```

### 4. Making a POST request:

To make a POST request using a session:

```javascript
const response = await fetch("/v1/request/", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    url: "http://your_target_url",
    postData: { key: "value" },  // Optional
    session: "your_session_id",  // Optional
    headers: {  // Optional
      "Header-Name": "Header-Value"
    }
    // Other optional parameters: session_ttl_minutes, maxTimeout, cookies, returnOnlyCookies, proxy
  })
});
const data = await response.json();
console.log(data); 
```

**Expected Output:** A JSON object containing the response details such as `url`, `status`, `headers`, `response` (HTML content), and `cookies`.

```json
{
  "url": "https://www.example.com/",
  "status": 200,
  "headers": {...},
  "response": "<!DOCTYPE html><html>...</html>",
  "cookies": [
    {
      "name": "cookie_name",
      "value": "cookie_value",
      ...
    },
    ...
  ],
  ...
}
```

### 5. Deleting a session:

To delete a session:

```javascript
const response = await fetch("/v1/sessions/your_session_id", {
  method: "DELETE"
});
const data = await response.json();
console.log(data);  // Expected output: { "status": "ok" }
```

### 6. Listing all sessions:

To get a list of all active sessions:

```javascript
const response = await fetch("/v1/sessions/");
const data = await response.json();
console.log(data);  // Expected output: { "sessions": ["session_id_1", "session_id_2", ...] }
```

## Optional Parameters:

For **GET and POST** requests, the following parameters are optional:

- `session`: The session ID to be used.
- `headers`: Custom headers to be added to the request.
- `session_ttl_minutes`: Time-to-live for the session in minutes.
- `maxTimeout`: Maximum timeout for the request in milliseconds. Defaults to `60000` ms.
- `cookies`: List of cookies to be included in the request.
- `returnOnlyCookies`: If set to `true`, only the cookies from the response will be returned.
- `proxy`: Proxy settings for the request. Contains URL, username (optional), and password (optional).

For **session creation** (`/v1/sessions/`), the `proxy` parameter is optional.
