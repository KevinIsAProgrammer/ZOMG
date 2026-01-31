from mem import Mem

def test_create():
    m = Mem(64)
    for i in range(1,64):
        assert m.at(i) == '0' 

def test_flip():
    m = Mem(64)
    assert m.at(8) == '0' 

    m.flip(8)
    assert m.at(8) == '1'

def test_flip2():
    m = Mem(64)
    assert m.flip(8) == True 
    assert m.flip(8) == False 
    
def test_flip_out_of_range():
    m = Mem(64)
    assert m.flip(88) == False 
    assert m.flip(88) == False 
    
def test_negative_flip():
    m = Mem(64)
    assert m.flip(-3) == True
    assert m.flip(-3) == True

def test_symbols():
    m = Mem(64)
    m.flip(8)
    assert m.symbol(8) == '#'
    m.flip(9)
    assert m.symbol(8) == '?'
    m.flip(8)
    assert m.symbol(8) == '1'
    m.flip(9)
    assert m.symbol(8) == '0'


def test_address():
    m = Mem(64)
    assert m.at(-1) == '1'
    m.flip(-1) 
    assert m.at(-1) == '1'

        
