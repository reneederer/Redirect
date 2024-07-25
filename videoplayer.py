import yt_dlp
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
import os
from psutil import process_iter
from signal import SIGTERM

hostName = "localhost"
serverPort = 8080

ydl_opts = {
    'format': 'best',
}

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f'{self.path}')
        if self.path.startswith('/?url='):
            try:
                video_id = self.path[6:]  # Changed to correctly extract video ID from the path
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    meta = ydl.extract_info(video_id, download=False)
                    video_url = meta['url']
                    print(video_url)
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(bytes(f'<html><head><title>{meta["title"]}</title></head><body style="background-color: black"><h1 style="text-align: center; color: gray">{meta["title"]}</h1><div style="text-align: center"><video style="min-width:70%; min-height:70%" autoplay="true" controls="true" loop="true" src="{meta["url"]}"></div></video></body></html>', 'utf-8'))
            except Exception as e:
                print(f'Error: {e}')
                self.send_response(301)
                self.send_header("Location", f'http://localhost:8080/?error={e}')
                self.end_headers()
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(f"<p>Can't show: {self.path[8:]}", 'utf-8'))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "start-server":
            for proc in process_iter(['pid', 'name']):
                for conns in proc.connections(kind='inet'):
                    if conns.laddr.port == serverPort:
                        try:
                            proc.send_signal(SIGTERM)
                        except Exception as e:
                            print(f'Error stopping process: {e}')

            webServer = HTTPServer((hostName, serverPort), MyServer)
            print(f"Server started http://{hostName}:{serverPort}")
            try:
                sys.stdout = sys.stderr = open(os.devnull, "w")
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
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval (New-TimeSpan -Minutes 1) -RepetitionDuration (New-TimeSpan -Hours 23 -Minutes 55)
sleep 1
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
sleep 1
Register-ScheduledTask -Action $action -Trigger $trigger -Settings $settings -TaskName 'Redirect Youtube' -Description 'Redirect Youtube'
sleep 1
    """
                ps_file.write(s)
            subprocess.Popen(['powershell', f'Start-Process -Verb RunAs -Wait powershell.exe -Args "-Command {ps_path}"'])
            # os.remove(ps_path)
