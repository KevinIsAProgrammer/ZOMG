from zomg import ZOMG

def test_create():
    z = ZOMG(128)
    assert z.f == False
    assert z.c == 0 
    assert z.d == 0

    assert z.v == 0
    assert z.u == True
    assert z.s == True 

    assert z.m.at(8) == '0' 

def test_first_zero_sets_s_to_positive():
    z = ZOMG(16)
    assert z.u == True
    assert z.v == 0
    r = z.zero()
    assert r == True
    assert z.u == False
    assert z.s == True
    assert z.v == 0

def test_zero_multiplies_n_by_two():
    z = ZOMG(16)
    z.v = 1
    z.u = False
    r = z.zero()
    assert r == True
    assert z.v == 2
    z.zero()
    assert z.v == 4
    z.v = 3
    z.zero()
    assert z.v == 6

def test_one_sets_negative():
    z = ZOMG(16)
    z.one()

    # verify negative with no value = negative zero
    assert z.u == False

    assert z.sign() == "-"
    assert z.v == 0
    assert z.n() == 0

    z.one()
    assert z.n() == -1
    z.one()
    assert z.n() == -3

def test_math_adding_zero_clears_d():
    z = ZOMG(16)
    z.d = 100
    assert z.sign() == "+"
    assert z.n() == 0
    z.math()

    assert z.d == 0
    assert z.n() == 0
    assert z.sign() == "+"
    assert z.u == True

def test_math_adding_negative_zero_sets_d_to_c():
    z = ZOMG(16)
    z.d = 100   # some random value different from c
    z.c = 8     # pretend we're running at instruction 8 
    z.s = False
    assert z.sign() == "-"
    assert z.n() == 0

    z.math()
    # d was set to c
    assert z.d == 8 

    # n is cleared 
    assert z.n() == 0
    assert z.sign() == "+"


def test_math_adds_n_to_d():
    z = ZOMG(16)
    z.d = 100
    z.c = 8
    z.s = True
    z.u = False
    z.v = 15
    assert z.sign() == "+"
    assert z.n() == 15

    z.math()

    assert z.d == 115
    assert z.sign() == "+"
    assert z.n() == 0
    assert z.u == True

def test_go_to_address_negative_zero_sets_fixed_addressing():
    z = ZOMG(16)
    assert z.f == False
    z.s = False
    z.u = False

    assert z.sign() == "-"
    assert z.n() == 0

    z.c = 18  # set some values for c & d, see that they remain unchanged
    z.d = 20
    
    z.go()

    assert z.f == True
    assert z.s == True
    assert z.u == True
    assert z.n() == 0

    # c,d unchanged by go
    assert z.c == 18
    assert z.d == 20

def test_go_to_address_zero_in_fixed_addressing_mode_sets_relative_addressing():
    z = ZOMG(16)
    z.f = True  # set fixed addressing mode
    z.u = False
    
    # assert n=+0
    assert z.sign() == "+"
    assert z.n() == 0

    z.go()

    assert z.f == False
    assert z.u == True

def test_go_to_negative_in_fixed_addressing_mode_exits():
    z = ZOMG(16)
    z.run = True
    z.f = True
    z.u = False
    z.s = False
    z.v = 15

    z.go()
    assert z.run == False
    assert z.exit_status == 14

# d = 0 is the only location that reacts to a go operation in a special way
# So, we can test normal behaviour by not using d = 0. 
def test_go_flips_bit_at_d():
    z = ZOMG(16)
    z.d = 10 
    z.c = 12
    
    assert z.m.at(z.d) == '0' 

    z.u = False
    # set n = +4 instructions
    z.s = True
    z.v = 4 

    r=z.go()
    assert z.c == 20 # 12 + 4 instructions * 2 bits = 12 + 8 bits = bit 20
    assert r == False # branch taken, c computed

    assert z.d == 10 # unchanged
    assert z.m.at(z.d) == '1'

    assert z.u == True
    assert z.v == 0


    z.v = 4
    z.u = False
    r = z.go()

    assert r == True # branch not taken, c not updated 
    assert z.c == 20 # unchanged 

    assert z.d == 10 # unchanged
    assert z.m.at(z.d) == '0'

    assert z.u == True
    assert z.v == 0


def test_branch_to_fixed_offset():
    z = ZOMG(16)
    z.d = 10 
    z.c = 12
    
    assert z.m.at(z.d) == '0' 

    z.u = False
    # set n = +4 instructions
    z.s = True
    z.v = 4 
    z.f = True # fixed addressing mode

    r=z.go()
    assert z.c == 4 # fixed address to branch to 
    assert r == False # branch taken, c computed

