from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
import threading
from pathlib import Path
import sys

# using https://github.com/paulc/dnslib/tree/e266b75fab4464350346200638dbd08c254b5b01
from dnslib.server import DNSServer, BaseResolver, DNSLogger
from dnslib import DNSRecord, RR, QTYPE, A

THEMES_TXT = Path(__file__).parent / 'themes_urls.txt'

def get_local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    result = s.getsockname()[0]
    s.close()
    assert isinstance(result,str)
    return result


UPSTREAM_DNS = ("1.1.1.1", 53)
TARGET_DOMAIN = "gs2.ww.prod.dl.playstation.net."
# Get current machine IP
CURRENT_IP = get_local_ip()

global_checked_dns_server = False

class QuietDnsLogger(DNSLogger):
    def log_pass(self, *args, **kwargs): pass
    def log_recv(self, *args, **kwargs): pass
    def log_send(self, *args, **kwargs): pass
    def log_request(self, *args, **kwargs): pass
    def log_reply(self, *args, **kwargs): pass
    def log_truncated(self, *args, **kwargs): pass
    def log_error(self, *args, **kwargs): pass


class SimpleHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # disables all console logging

    def do_GET(self):
        if self.path.endswith('.json'):
            new_theme_url = f'http://gs2.ww.prod.dl.playstation.net{self.path}' 
            try:
                current_themes = set(x.strip() for x in THEMES_TXT.read_text().strip().split('\n'))
            except Exception:
                current_themes = set()
            
            current_themes.add(new_theme_url)
            payload = '\n'.join(current_themes)
            THEMES_TXT.write_text(payload)
            print(f'new theme url {new_theme_url} in {THEMES_TXT}')
        # Send a basic response
        self.send_response(500)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"cant be bothered to foward request")



class CustomResolver(BaseResolver):
    def resolve(self, request, handler):
        global global_checked_dns_server
        qname = request.q.qname
        qtype = QTYPE[request.q.qtype]

        # Create reply skeleton
        reply = request.reply()

        if str(qname).lower() == TARGET_DOMAIN and qtype == "A":
            # print(f"Intercepted {qname}, returning {CURRENT_IP}")
            reply.add_answer(RR(qname, QTYPE.A, rdata=A(CURRENT_IP), ttl=60))
            return reply

        # Forward to upstream DNS
        try:
            proxy_r = request.send(*UPSTREAM_DNS, timeout=2)
            res = DNSRecord.parse(proxy_r)
            if not global_checked_dns_server:
                print('DNS server is working!')
                global_checked_dns_server = True
            return res
        except Exception as e:
            print("Upstream query failed:", e)
            return reply  # empty response


def do_http_one():
    server = HTTPServer((CURRENT_IP, 80), SimpleHandler)
    server.serve_forever()


def do_dns_one():
    resolver = CustomResolver()
    server = DNSServer(resolver, port=53, address=CURRENT_IP,logger=QuietDnsLogger())
    
    print(f"Please enter {CURRENT_IP} on your PS4's primary and secondary DNS")
    server.start()


def main():
    if sys.version_info < (3, 11):
        input('Please use python 3.11 or higher')
    t1 = threading.Thread(target=do_http_one)
    t2 = threading.Thread(target=do_dns_one)
    
    t1.start()
    t2.start()

    t1.join()
    t2.join()


if __name__ == '__main__':
    main()
