import os
class Buffer(object):
    def __init__(self, word_size, num_words):
        self.word_size = word_size
        self.num_words = num_words
        self.max = word_size * num_words
        self.have_eof = False

        self.buf=[False] *(self.max)
        self.pos=word_size -1
        self.word_num = num_words 
        self.last_word = True 

    def set_word(self, word_num, word):
        if (word_num > self.num_words - 1):
            print("error: invalid word number " + word_num)
            
        pos = 0 
        for shift in range(0, self.word_size): 
            bit = 1 << shift
            if (word & bit):
                self.buf[self.word_size * word_num + pos] = True
            else:
                self.buf[self.word_size * word_num + pos] = False
            pos += 1

    def get_word(self, word_num):
        if (word_num > self.num_words - 1):
            print("error in get_word: invalid word number "+word_num)

        word = 0
        for shift in range(0,self.word_size):
            if self.buf[self.word_size*word_num+shift]:
                word = word | (1 << shift)

        return word

    def clear(self):
        self.buf=[False] *(self.max)
        self.pos=self.word_size - 1
        self.word_num = 0
        self.last_word = False
    
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
        print("p="+str(p))
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


    def write(self, bit, end):
        """ Write bits to the buffer until we send an end bit or hit
            the end of the buffer.
        """
        if end:
            if bit:
                for i in range(0, self.num_words):
                    status = self.write_word(self.get_word(i)) 
                    if not(status):
                        return False
                self.clear()
                self.write_eof()

        if self.pos < 0 or (end and not(bit)):
                status = self.write_word(self.get_word(self.word_num))
                if not(status):
                    return False
                self.word_num +=1
                if self.word_num >= self.num_words:
                    self.word_num = 0
                self.pos = self.word_size - 1

        if not(end):
            p = self.word_num * self.word_size + self.pos
            self.buf[p] = bit
        return True
        
    def write_word(self, word):
        """
            Write a word to output
        """
        print("Writing word"+str(word))
        status=os.write(word,1)
        return status == 1



