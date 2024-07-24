import yt_dlp
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
import os

hostName = "localhost"
serverPort = 8080

ydl_opts = {
    'format': 'best',
}


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                meta = ydl.extract_info(self.path[6:], download=False)
                print(meta['url'])
                video_url = meta['url']
                self.send_response(301)
                self.send_header("Location", video_url)
                self.end_headers()
                return None
        except:
            self.send_response(500)
            return None


if __name__ == "__main__":
    if sys.argv[1] == "start-server":
        sys.stdout = sys.stderr = open(os.devnull, "w")
        webServer = HTTPServer((hostName, serverPort), MyServer)
        print("Server started http://%s:%s" % (hostName, serverPort))

        try:
            webServer.serve_forever()
        except KeyboardInterrupt:
            pass

        webServer.server_close()
        print("Server stopped.")
    elif sys.argv[1] == 'create-task':
        ps_path = 'C:/Users/rene/source/repos/VideoPlayer/videoplayer.ps1'
        python_path = 'C:/Users/rene/source/repos/VideoPlayer/videoplayer.py'

        with open(ps_path, mode='w') as ps_file:
            s = f"""
$action = New-ScheduledTaskAction -Execute 'pythonw.exe' -Argument '{python_path} start-server'
sleep 1
$trigger = New-ScheduledTaskTrigger -Once -At 01:00 -RepetitionInterval (New-TimeSpan -Minutes 1) -RepetitionDuration (New-TimeSpan -Hours 23 -Minutes 55)
sleep 1
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
sleep 1
# $principal = New-ScheduledTaskPrincipal -UserId 'SYSTEM' -LogonType ServiceAccount -RunLevel Highest
sleep 1
Register-ScheduledTask -Action $action -Trigger $trigger -Settings $settings -TaskName 'Redirect Youtube' -Description 'Redirect Youtube'
sleep 1
    """
            ps_file.write(s)
        subprocess.Popen(['powershell', f'Start-Process -Verb RunAs -Wait powershell.exe -Args "-Command {ps_path}"'])
        # os.remove(ps_path)


