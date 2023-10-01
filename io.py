class Buffer(object):
    def __init__(self, wordSize, numWords):
        self.pos = 0
        self.wordSize = wordSize
        self.numWords = numWords
        self.max = wordSize * numWords
        self.buf=[False] * (self.max)

class ReadBuffer(Buffer):
    def new_word(self):
        return (self.pos != 0) && ((self.pos % self.wordSize)==0)

    def last():
        return self.pos > (self.wordSize * self.numWords)

    def next_bit(self):
        return self.buf[pos++]
    
    def set_word(self, word):
        pos = 0 
        for b in word:
           self.buf[pos++] = b

    def read(self):
        """ 
        data, eof = buffer.read()
        """
        if self.last():
           return 1, 1 
        elif self.new_word():
           self.readMore()
           return 0, 1
        else:
           b = next_bit()
           return b, 0

class WriteBuffer(Buffer):
    def set(self, b):
        self.buf.set(b, pos++)

    def next_word(self):
        self.pos += self.wordSize - (self.pos % self.wordSize)

    def write(self, b, eof):
        if eof & b:
           self.done()
        elif eof:
           self.next_word()
        else:
           self.set(b)

    def done(self):
        pass

class Syscall(WriteBuffer):
      def __init__(self):
           self.result = ReadBuffer(wordSize=64, numWords=1)
      
      def done(self):
           r = syscall(self.buf)
           self.result.set_word(r)
      
      def read(self):
           return self.result.read()

class IO(object):
      def __init__(self, w_fd, r_fd):
           self.w = WriteBuffer(wordSize=8, numWords=1)
           self.w_fd = w_fd 

           self.r = ReadBuffer(wordSize=8, numWords=1)
           self.r_fd = r_fd

     def read(self):
         """ 
         data, eof = buffer.read()
         """
         if eof(self.r_fd):
           return 1, 1 
         elif self.r.new_word():
           ch = read(self.r.fd,1) 
           self.r.set_word(ch)
           self.r.pos=0
         else:
           b = self.r.next_bit()
           return b, 0

    def write(self, eof, b):
        if(eof & b):
           close(self.w_fd)
        elif(eof):
           write(self.w_fd, "") 

        self.w.set(b, eof)

        if self.w.next_word():
           write(self.w_fd, self.w.buf) 

class ErrIO(IO):
     def __init__(self, w_fd, r_fd):
           self.w = WriteBuffer(wordSize=8, numWords=1)
           self.w_fd = w_fd 

           self.r = ReadBuffer(wordSize=8, numWords=1)

     def read(self):
         """ 
         data, eof = buffer.read()
         """
         if self.r.last():
           return 1, 1 
         elif self.r.new_word():
           self.r.set_word(errno)
           self.r.pos=0
         else:
           b = self.r.next_bit()
           return b, 0

     def write(self, eof, b):
         if(eof & b):
           close(self.w_fd)
         elif(eof):
           write(self.w_fd, "") 

         self.w.set(b, eof)

         if self.w.next_word():
           write(self.w_fd, self.w.buf) 

# 
# Syscall, IO, ERR_IO
#

class IO(object):
    GO=0
    DATA=1
    MODE=2
    EOF=3

    STATUS=4
    SYS=5
    CHANNEL=6
    ERR=7

    def io(self, bits):
        print("Called IO with" + bits) 
         
        if (bits[SYS]) 
           status=self.syscall(bits)
        elif (bits[CHANNEL]):
           # w: ; ; w2 ; w3 . 
           # foreach i in 0..3
           # fds[i] = w_n if w_n was set 
           # r: fd0 ; ... fd_n .
           status=self.channel(bits)
        elif (bits[ERR]):
           # w: b ; b ; . 
           # write on fd2; (or overflow to ;), and
           # flush on .

           # r: error_no_word .
           status=self.err(bits)
        else:
           # w: b ; b ; .
           # write b on fd1 if ; ( or when overflow to ;) 
           #  
           # r: b ; b ; .
           # read b on fd0 if ; (or when overflow to ;)
           # set EOF(1) 
           status=self.io(bits) 
        return status 

    def io(self, bits):
        if bits[MODE]:
           return io_write(self, bits)        

    def syscall(self, bits):
        if bits[MODE]:
           # arg1 ; ... ; arg_n.
           # result <- syscall(arg, ..., arg_n)
           return syscall_write(self, bits)
        # result .
        return syscall_status(self, bits)

    def syscall_write(self, bits): 
        if bits[EOF] & bits[DATA]:
           result=syscall(buffer)
           if (result == -1):
              buffer.clear()
           return False
           self.sys.result.set_word(result)
        elif bits[EOF]:
	   buffer.next_word()
           return True
        else: 
           buffer.set(bits[DATA])
           return True

    def buffer_read(self, bits): 
        buffer = self.sys.result
        if buffer.last():
           bits[EOF] = True 
           bits[DATA] = True
           return True
        else:
           bits[EOF] = False
           bits[DATA] = buffer.next_bit()
           return True

    def channel_write(self, bits): 
        ch = self.channel
        if bits[EOF] && bits[DATA]:
           ch.set_fds()
        elif bits[EOF]:
           ch.next()
        else:
           ch.set(bits[DATA])
        return True

    def channel_read(self, bits):
        ch = self.channel
        e, b = ch.next_bit()
        bits[EOF]=e
        bits[DATA]=b
        return True

    
