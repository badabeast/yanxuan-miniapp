import socket
from pathlib import Path
from proxy.proxy_run import run
from mitmproxy.tools.dump import DumpMaster
from mitmproxy.tools.cmdline import mitmdump
# from utils.log import Log

"""
HTTP proxy server

Default port 4272
"""

CURRENT_PATH = Path(__file__).parent
FLOW_PATH = CURRENT_PATH/'proxy_flow.py'

# logger = Log()

class ProxyServer():

    def __init__(self):

        self.proxy_port = '4272'
        '''
        --ignore_hosts:
        The ignore_hosts option allows you to specify a regex which is matched against a host:port
        string (e.g. “example.com:443”) of a connection. Matching hosts are excluded from interception,
        and passed on unmodified.

        # Ignore everything but sankuai.com, meituan.com and dianping.com:
        --ignore-hosts '^(?!.*sankuai.*)(?!.*meituan.*)(?!.*dianping.*)'

        According to mitmproxy docs: https://docs.mitmproxy.org/stable/howto-ignoredomains/
        '''
        # self.ignore_hosts = None
        # if conf.get('proxy.filters'):
        #     self.ignore_hosts = '^%s' % ''.join(['(?!.*%s.*)' % i for i in conf.get('proxy.filters')])

        self._master = None

    def run(self):
        server_ip = '127.0.0.1'
        # info_msg(f'start on {server_ip}:{self.proxy_port}', f'{Fore.CYAN} ***请在被测设备上设置代理服务器地址***')
        # logger.warning(f'start on {server_ip}:{self.proxy_port}   {Fore.CYAN} ***请在被测设备上设置代理服务器地址***')
        
        mitm_arguments = [
            '-s', str(FLOW_PATH),
            '-p', self.proxy_port,
            '--ssl-insecure',
            '--no-http2',
            '-q'
        ]
        # if self.ignore_hosts:
        #     mitm_arguments += ['--ignore-hosts', self.ignore_hosts]
        run(DumpMaster, mitmdump, mitm_arguments)
        
if __name__ == "__main__":
    ProxyServer().run()