# CPAN226 Lab 1: HTTP Protocol Investigation

**Student:** Gusta
**Course:** CPAN226 - Networking & Telecommunications
**Date:** January 30, 2026

---

## Lab Overview

This lab explores HTTP protocol through manual requests (ncat), packet analysis (Wireshark), and Python socket programming.

**Tools Used:**
- ncat 7.98
- Wireshark
- Python 3.12.9

---

## Question 1: HTTP Status Code (Port 80)

**Answer:** **301 Moved Permanently**

**Method:**
```bash
ncat -C gaia.cs.umass.edu 80
GET /kurose_ross/interactive/index.php HTTP/1.1
Host: gaia.cs.umass.edu

```

**Evidence:**

![Command Output](Question%201%20-%20CMD.png)

![Wireshark Capture](Question%201%20-%20Wireshark.png)

**Explanation:** The server redirects HTTP to HTTPS for security. The 301 status code with `Location: https://...` header instructs clients to use encrypted connections.

---

## Question 2: HTTPS Status Code (Port 443)

**Answer:** **200 OK**

**Method:**
```bash
ncat --ssl -C gaia.cs.umass.edu 443
GET /kurose_ross/interactive/index.php HTTP/1.1
Host: gaia.cs.umass.edu

```

**Evidence:**

![Command Output](Question%202%20-%20CMD.png)

**Server Response:**
```http
HTTP/1.1 200 OK
Server: Apache/2.4.62 (AlmaLinux) OpenSSL/3.5.1 mod_fcgid/2.3.9 mod_perl/2.0.12 Perl/v5.32.1
Content-Type: text/html; charset=UTF-8
```

**Explanation:** HTTPS connection successfully delivers content. The 200 status indicates the server processed the request and returned the requested resource.

---

## Question 3: User-Agent Header

**Answer:** **None** (not sent)

**Method:** Examined HTTP request in Wireshark by filtering for HTTP requests and inspecting headers.

**Headers Sent:**
- Request line: `GET /kurose_ross/interactive/index.php HTTP/1.1`
- Host header: `Host: gaia.cs.umass.edu`
- Blank line

**Explanation:** User-Agent is optional in HTTP/1.1 (only Host is required). Manual ncat requests included only minimal headers.

**Browser Comparison:**
Chrome would send:
```http
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...
```

---

## Question 4: Server Software

**Answer:** **Apache/2.4.62** on AlmaLinux

**Complete Server Header:**
```
Server: Apache/2.4.62 (AlmaLinux) OpenSSL/3.5.1 mod_fcgid/2.3.9 mod_perl/2.0.12 Perl/v5.32.1
```

**Components:**
- **Web Server:** Apache 2.4.62
- **OS:** AlmaLinux (Linux distribution)
- **SSL/TLS:** OpenSSL 3.5.1
- **Modules:** mod_fcgid, mod_perl
- **Languages:** PHP 8.0.30, Perl 5.32.1

---

## Question 5: Getting 200 Status Code

**Part A:** No, initial Python program received **301 Moved Permanently**

**Part B: Changes Required**

**1. Change port from 80 to 443:**
```python
server_port = 443  # Changed from 80
```

**2. Add SSL/TLS encryption:**
```python
import ssl

client_socket = socket(AF_INET, SOCK_STREAM)
ssl_socket = ssl.wrap_socket(client_socket, server_hostname=server_name)

ssl_socket.connect((server_name, server_port))
ssl_socket.send(request.encode())
response = ssl_socket.recv(4096)
ssl_socket.close()
```

**Complete HTTPS Code:**
```python
from socket import *
import ssl

server_name = 'gaia.cs.umass.edu'
server_port = 443

client_socket = socket(AF_INET, SOCK_STREAM)
ssl_socket = ssl.wrap_socket(client_socket, server_hostname=server_name)

ssl_socket.connect((server_name, server_port))

request = "GET /kurose_ross/interactive/index.php HTTP/1.1\r\nHost: gaia.cs.umass.edu\r\n\r\n"
ssl_socket.send(request.encode())

response = ssl_socket.recv(4096)
print(response.decode())

ssl_socket.close()
```

**Evidence:**

![Python Output - 200 OK](Question%205%20-%20CMD.png)

**Explanation:** Modern servers require HTTPS. The `ssl.wrap_socket()` function adds encryption layer, performs TLS handshake, and transparently encrypts/decrypts data.

---

## Key Learnings

### HTTP Protocol
- Request structure: Request line + Headers + Blank line (`\r\n\r\n`)
- Status codes: 200 (success), 301 (redirect), 404 (not found)
- HTTP vs HTTPS: Plaintext vs encrypted (port 80 vs 443)

### Network Analysis
- TCP 3-way handshake: SYN → SYN-ACK → ACK
- Wireshark packet inspection at all protocol layers
- HTTP traffic visible, HTTPS traffic encrypted

### Socket Programming
- Socket lifecycle: Create → Connect → Send → Receive → Close
- Python API: `socket()`, `connect()`, `send()`, `recv()`, `close()`
- `.encode()` / `.decode()` for string ↔ bytes conversion
- `ssl.wrap_socket()` for HTTPS encryption

---

## Files

- `http_client.py` - HTTP client (gets 301)
- `https_client.py` - HTTPS client (gets 200)
- Screenshots: Question 1 CMD/Wireshark, Question 2 CMD, Question 5 CMD

---

## Summary

Successfully completed HTTP protocol investigation through:
-  Manual HTTP/HTTPS requests with ncat
-  Wireshark packet analysis
-  Python socket programming
-  Understanding HTTP → HTTPS redirection
-  Implementing SSL/TLS encryption

**All 5 questions answered with evidence.**
