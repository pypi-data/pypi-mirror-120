import json
import shlex
import inspect
import logging
import subprocess
from robot.api.deco import keyword

class api(object):

    def __init__(self):
        logging.basicConfig()
        logging.getLogger().setLevel(logging.INFO)
        logger = logging.getLogger(__name__)

    def _logDebug(self, funcName, status):
        time_s = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print('[{}]{}: {}'.format(time_s, funcName, status))

    def _status(self, status='fail'):
        if status == 'pass':
            status = 'PASSED'
        else:
            status = 'FAILED'
        return status

    @keyword('Request cURL')
    def cURL(curl_command):
        status = self._status()
        funcName = inspect.stack()[0][3]
        try:
            args = shlex.split(curl_command)
            process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            parsed = json.loads(stdout)
            status = self._status('pass')
            self._logDebug(funcName, status)
            return parsed
        except KeyboardInterrupt:
            status = self._status()
            self._logDebug(funcName, status)