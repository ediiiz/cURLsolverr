# cURLsolverr

## Introduction

The `cURLsolverrManager` is a FastAPI application designed to create and manage HTTP sessions based on curl-impersonate (curl_cffi) with extended functionalities. The manager allows users to make GET and POST requests using created sessions, which can optionally be configured with a proxy. The manager also allows users to delete sessions and get a list of all active sessions.

## Installation using Docker

### 1. Pulling the Docker Image:

To get the Docker image of `cURLsolverrManager` from Docker Hub:

```bash
docker pull ed1zx/curlsolverr:latest
```

### 2. Running with Docker Compose:

You can use Docker Compose to manage the application container. Here's a basic `docker-compose.yml` file for the service:

```yaml
version: '3'

services:
  curlsolverr:
    image: ed1zx/curlsolverr:latest
    ports:
      - "8000:8000"
```

With the above `docker-compose.yml` file, you can start the application using:

```bash
docker-compose up
```

This will start the `cURLsolverrManager` application and bind it to port 8000 on your host machine. You can access the application by navigating to `http://localhost:8000` in your browser or using any API client.

### 3. Accessing the Swagger UI:

Once the application is running, you can access the Swagger UI at:

```
http://localhost:8000/docs
```

The Swagger UI provides a user-friendly interface to interact with the API, view its documentation, and test out its endpoints.

## Usage

### 1. Creating a new session:

To create a new session, you can make a POST request to `/v1/session/`:

```javascript
const response = await fetch("/v1/session/", {
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

### 2. Making a GET or POST request:

To make a GET or POST request using a session, you can make a POST request to `/v1/request/`:

```javascript
const requestData = {
  method: "GET", // or "POST"
  url: "http://your_target_url",
  session: "your_session_id",
  headers: {  // Optional
    "Header-Name": "Header-Value"
  },
  postData: { key: "value" },  // Optional for POST
  // Other optional parameters: returnOnlyCookies
};

const response = await fetch("/v1/request/", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(requestData)
});

const data = await response.json();
console.log(data); 

// Expected Output:
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

### 3. Deleting a session:

To delete a session:

```javascript
const response = await fetch("/v1/session/your_session_id", {
  method: "DELETE"
});
const data = await response.json();
console.log(data);  // Expected output: { "status": "ok" }
```

### 4. Listing all sessions:

To get a list of all active sessions:

```javascript
const response = await fetch("/v1/session/");
const data = await response.json();
console.log(data);  // Expected output: { "sessions": ["session_id_1", "session_id_2", ...] }
```

## Optional Parameters:

For requests to `/v1/request/`, the following parameters are optional:

- `headers`: Custom headers to be added to the request.
- `postData`: Data to be sent in a POST request.
- `returnOnlyCookies`: If set to `true`, only the cookies from the response will be returned.
- `proxy`: Proxy settings for the request. Contains URL, username (optional), and password (optional).

For **session creation** (`/v1/session/`), the `proxy` parameter is optional.

--- 

This README reflects the updated code structure and functionality you've shared. Adjustments can be made further based on specific requirements or further changes to the code.
