# TCP File Server — Network Programming Task 3

> Pemrograman Jaringan (Network Programming) · ITS Surabaya · 2025

A multithreaded TCP file server built from scratch in Python, supporting file listing and download over a custom JSON-based protocol. Includes a CLI client for interactive access.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Socket](https://img.shields.io/badge/Socket_Programming-3DDC84?style=flat)
![Threading](https://img.shields.io/badge/Multithreading-FF6B6B?style=flat)

---

## Overview

This project implements a TCP file server that allows clients to list and download files over raw TCP sockets using a custom text-based protocol. The server uses a **thread-per-client** model — each incoming connection is handled in its own thread. Responses are returned as JSON and terminated with `\r\n\r\n`.

A CLI client (`file_client_cli.py`) is provided for interactive use from the terminal.

---

## Protocol

Requests are plain text strings in the format `REQUEST PARAMETER`. Responses are always JSON terminated with `\r\n\r\n`.

| Command | Format | Response |
|---|---|---|
| List files | `LIST` | `{"status": "OK", "data": ["file1.txt", ...]}` |
| Download file | `GET <filename>` | `{"status": "OK", "data_namafile": "...", "data_file": "<base64>"}` |
| Unknown command | *(any other string)* | `{"status": "ERROR", "data": "request tidak dikenali"}` |

Files are transmitted as **Base64-encoded strings** to safely handle binary content over the text protocol. Every response ends with `\r\n\r\n` as the message terminator.

**Example session:**
```
Client → LIST
Server → {"status": "OK", "data": ["hello.txt", "image.png"]}\r\n\r\n

Client → GET hello.txt
Server → {"status": "OK", "data_namafile": "hello.txt", "data_file": "SGVsbG8..."}\r\n\r\n
```

---

## Architecture

```
Client (file_client_cli.py)
        │
        │  TEXT command (e.g. "GET hello.txt")
        ▼
file_server.py            ← accepts connections, spawns 1 thread per client
        │
        ▼
FileProtocol              ← parses command string, routes to correct method
        │
        ▼
FileInterface             ← executes LIST or GET, reads from files/ directory
        │
        │  JSON + \r\n\r\n
        ▼
Client
```

---

## Repository Structure

```
progjar-task-03/
│
├── file_server.py          ← Multithreaded TCP server (port 9999)
├── file_client_cli.py      ← Interactive CLI client
├── file_interface.py       ← File operations: list, get (Base64)
├── file_protocol.py        ← Protocol parser & JSON response builder
├── PROTOKOL.txt            ← Protocol specification (Bahasa Indonesia)
│
└── files/                  ← Server-side file storage
```

---

## Getting Started

### Run the server
```bash
python file_server.py
# Server berjalan di ip address ('0.0.0.0', 9999)
```

### Run the CLI client
```bash
python file_client_cli.py
```

### Test manually with netcat
```bash
nc localhost 9999
LIST
# {"status": "OK", "data": ["hello.txt", "image.png"]}

GET hello.txt
# {"status": "OK", "data_namafile": "hello.txt", "data_file": "SGVsbG8..."}
```

---

## Key Concepts Covered

- **TCP socket programming** — raw `socket.AF_INET` / `SOCK_STREAM`, bind, listen, accept
- **Thread-per-client concurrency** — `threading.Thread` spawned for each incoming connection
- **Custom protocol design** — text commands with JSON responses, `\r\n\r\n` message terminator
- **Base64 file encoding** — safe binary-over-text transfer using `base64.b64encode`
- **Layered architecture** — clean separation of server logic, protocol parsing, and file operations
- **CLI client** — interactive terminal interface for real-time server interaction

---

## Relation to Other Tasks

This task builds the foundation for more advanced implementations in the same course:

| Task | Feature Added |
|---|---|
| **Task 2** | TCP time server — basic client-server with custom protocol |
| **Task 3 (this)** | File server — LIST & GET, thread-per-client, Base64 transfer |
| **Task 4** | HTTP server — 7 concurrency models, SSL/TLS, socket proxy |
| **Midterm** | Full file server — UPLOAD & DELETE added, thread pool vs process pool, stress test |

---

## Course Context

This is **Task 3** of the *Pemrograman Jaringan* (Network Programming) course at Institut Teknologi Sepuluh Nopember (ITS) Surabaya. The task introduces file transfer over TCP sockets with a formally documented protocol (`PROTOKOL.txt`).

---

## Author

**Agnes Priscilla Sekartaji Hadikusuma**  
S1 Teknik Informatika · Institut Teknologi Sepuluh Nopember (ITS) Surabaya

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/agnespriscilla)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/agnespriscilla)
[![Email](https://img.shields.io/badge/Email-D14836?style=flat&logo=gmail&logoColor=white)](mailto:agnes.priscilla33@gmail.com)
