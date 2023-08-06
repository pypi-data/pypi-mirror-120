import threading
import socket


class PortScanner:
    def __init__(self, ipAddress: str = "127.0.0.1", timeout: float = 5.0):
        self._ipAddress = ipAddress
        self.timeout = timeout

        self.commonPorts = [
            20,
            21,
            22,
            23,
            25,
            53,
            80,
            110,
            119,
            213,
            143,
            161,
            194,
            443,
        ]

    def _scan(self, port: int, resultDict: dict) -> bool:
        s = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0, fileno=None
        )
        s.settimeout(self.timeout)
        try:
            s.connect((self._ipAddress, port))
            resultDict.update({port: True})
        except:
            resultDict.update({port: False})
        s.close()

    def scanSingle(self, port: int) -> bool:
        result = {}
        thread = threading.Thread(target=self._scan, args=(port, result))
        thread.start()

        return result

    def scanCommon(self):
        threads = [None] * len(self.commonPorts)
        result = {}
        currentCount = 0
        for port in self.commonPorts:
            threads[currentCount] = threading.Thread(
                target=self._scan, args=(port, result)
            )
            threads[currentCount].start()
            currentCount += 1

        for i in range(len(threads)):
            threads[i].join()

        return result

    def scanRange(self, portRange: range = range(65535)):
        threads = [None] * len(portRange)
        result = {}
        currentCount = 0
        for port in portRange:
            threads[currentCount] = threading.Thread(
                target=self._scan, args=(port, result)
            )
            threads[currentCount].start()
            currentCount += 1

        for i in range(len(threads)):
            threads[i].join()

        return result
