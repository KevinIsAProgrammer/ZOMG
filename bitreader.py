from buffer import Buffer
import os

class BitReader(Buffer):
    def __init__(self):
        word_size = 8
        num_words = 1
        super().__init__(word_size, num_words)

        self.pos=word_size - 1
        self.word_num = num_words
        self.last_word = True

        
    def read(self):
        """ Read a bit from the buffer. Call read_more_words() when
            out of bits to read. Returns STATUS, DATA, END
        """
        status=True
        if self.pos < 0:
            # next word, so send an end of field message 
            self.word_num +=1
            self.pos = self.word_size - 1
            return True, False, True 
        if self.word_num > self.num_words - 1:
            status = self.read_more_words()
        if  not(status):
            return False, False, False
        if self.have_eof and self.word_num == self.last_word:
            # end of file reached; so send an end of transmission
            return True, True, True

        p = self.word_num * self.word_size + self.pos
        #print("p="+str(p))
        # get the index of our bit in the buffer, and
        # then decrement down to the next bit
        self.pos -= 1
        # send our bit from the buffer 
        return True, self.buf[p], False

    def read_more_words(self):
        """ Read in more words until end of file.
            Returns status
            status = True for success, False for error

            Sets self.last_word to the index of the final
            word+1 if end of file is reached.

        """
        self.clear()
        for i in range(0, self.num_words):
            eof = self.is_eof()
            if eof:
                self.have_eof = True
                self.last_word = i
                return True

            word, status = self.read_word()
                
            if not(status): 
                return False
            if not(self.have_eof):
               self.set_word(i, word)
        return True

    def read_word(self):
        # read from stdin
        word = os.read(0,1)
        if len(word) == 0:
            self.have_eof = True
            return 0, True 
        return ord(word), True

    def is_eof(self):
        return self.have_eof
