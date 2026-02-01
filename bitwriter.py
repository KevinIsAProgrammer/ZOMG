from buffer import Buffer 
import os

class BitWriter(Buffer):
    def __init__(self):
        super().__init__(word_size=8, num_words=1)

        self.last_word = True
        self.clear()

    def write(self, bit, end):
        """ Write bits to the buffer until we send an end bit or hit
            the end of the buffer.
        """
        #print("pos=",self.pos)
        if end:
            if bit:
                for i in range(0, self.num_words):
                    status = self.write_word(self.get_word(i)) 
                    if not(status):
                        return False
                self.clear()
                #os.close(1)

        
        if self.pos < 0 or (end and not(bit)):
                # next field
                status = self.write_word(self.get_word(self.word_num))
                if not(status):
                    return False
                self.word_num +=1
                if self.word_num >= self.num_words:
                    self.word_num = 0
                    self.clear()
                self.pos = self.word_size - 1

        if not(end):
            p = self.word_num * self.word_size + self.pos
            self.buf[p] = bit
            self.pos -=1
        return True
        
    def write_word(self, word):
        """
            Write a word to output
        """
        #print("Writing word"+str(word))
        status=os.write(1, word.to_bytes())
        return status == 1
