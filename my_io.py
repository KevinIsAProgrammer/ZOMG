from bitreader import BitReader
from bitwriter import BitWriter
class IO(object):
    GO = 0
    DATA = 1
    MODE = 2
    END = 3
    STATUS = 4
    SYS = 5
    CHANNEL = 6
    ERR = 7
    def __init__(self):
        self.reader = BitReader()
        self.writer = BitWriter()

    def do_io(self, m):
        if (m[IO.ERR] or m[IO.CHANNEL] or m[IO.SYS]):
            m[IO.STATUS] = False # Not implemented
            return m

        if m[IO.MODE]:
            # write
            m[IO.STATUS] = self.writer.write(m[IO.DATA], m[IO.END])
            return m

        # read
        m[IO.STATUS],m[IO.DATA], m[IO.END] = self.reader.read()
        return m


