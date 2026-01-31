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
