# Tomcat-Manager-RCE

Exploits for achieving RCE through authenticated WAR deployment.

## Background
The attack vector leverages the legitimate Tomcat management functionality that allows for remote `.war` file deployment. By uploading a malicious WAR package containing a JSP (JavaServer Page), the server unpacks it and exposes the script within the web server's context. This enables command execution with the privileges of the user running the Tomcat service.

## Contents
* `/windows`: Implementation for Windows-based targets.
* `/linux`: Implementation for Linux-based targets.

---
*For educational and authorized security auditing purposes only.*
