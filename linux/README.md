# Implementation: Linux

This directory contains the exploit logic tailored for Apache Tomcat instances running on **Linux-based** environments.

## Features

* **Text-API Integration:** Leverages the `/manager/text` endpoint for efficient deployment and management.
* **Volatile Payload:** Dynamically generates a malicious WAR file containing a JSP web shell specifically crafted for POSIX-compliant execution, leveraging /bin/sh to ensure compatibility across a wide range of Linux distributions and containerized environments.
* **Automated Cleanup:** The script automatically deletes the local `.war` file and undeploys the application from the server immediately after execution.

## Prerequisites

Ensure you have the required dependencies installed before execution.

```bash
pip install -r requirements.txt
```
## Usage
```bash
python3 tomcat_rce.py -t <TARGET_URL> -u <USER> -p <PASSWORD> -c <COMMAND>
```

---
*For educational and authorized security auditing purposes only.*
