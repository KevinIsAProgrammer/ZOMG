# ZOMG
This project is intended to be an implementation of a virtual machine supporting the ZOMG language, a silly Turing Tarpit language that I invented that's concise but
(barely) functional. The language itself is Turing Complete (it has no inherent fixed maximum addressing size). 

A virtual machine implementation will have some finite amount of addressable memory, but the language itself is not concerned with this limit.

The language is called ZOMG, named after the four operations in the language ("Zero", "One", "Math", and "Go"). It's a bitcode encoded language,
with each operation being represented by 2 bits. 

# Registers
 **M**: Memory An array of bits, addressed by bit address. 
    The first 8 bits of M are special and are used in ZOMG I/O and system calls. 

    I/O occurs when a GO command attempts to flip the bit at memory address 0. The associated branch
    always fails. 

   The other 7 bits specify which I/O event to perform, and may also be modified by an I/O event. 
   For example, the DATA bit is set during a read event, and sent during a write event. See the section on ZOMG I/O for
   more information.
     
 **C**: Pointer to 2 bits (code pointer address) The bit address of next bitcode operation to fetch from memory.
 
 **D**: Pointer to 1 bit  (data pointer) The bit address of bit to flip in memory on a GO! instruction.

  
 **F**: 1 bit flag Fixed addressing mode (When 0, branches are calculated by adding/subtracting the given number of instructions. When 1, 
      branches are given as fixed addresses in memory to branch to)
       
 *N*: Number (signed offset to D or C). A virtual register that is Set by ZERO & ONE operations which manipulate the
      S, V, and U registers internally; used in MATH operation to manipulate D, and in GO operation to manipulate C. 

    The first ZERO or ONE operation sets the sign of N to positive or negative and subsequent operations append bits to it's 
    absolute value in msb order. If no sign has been set, the sign is positive.  If no value has been set, the value is zero. 

    N := -1^S * V if U, and (+) V otherwise.

 **V**:  Value (unsigned) Absolute value of N

 **S**: 1 bit flag Sign of N (0 for positive, 1 for negative)
 
 **U**: 1 bit flag Unset sign (0 if sign is unset, 1 otherwise)  

# **Operation of the VM**


```
Loop: U=1, S=0, V=0 
      if C < 0:
          exit( abs(C)-1)
      symbol= M[c] // read 2 bits
      set_c = 0
      set_c = handle symbol(symbol) // call appropriate operation for symbol (ZERO, ONE, MATH, or GO)
      if (!set_c)
          C +=2
      
ZERO: IF U=0: S = 0, U = 1 
      Otherwise, V=2*V, C+=2 
      return 0

ONE: IF U=0, S = 1, U=1
     Otherwise, V=2V + 1, C+=2
     return 0

MATH: IF N = -0: D=C
      else if N = 0: D=0
      else D += N
      return 0

GO:   IF N = -0: F=1 			   // set fixed mode
      else IF F = 1 & N = 0: F = 0 // from fixed mode, switch back to relative mode 
      else 
            IF D > 0 
               b=FLIP bit at M[d] 
            if D = 0
               do ZOMG I/O; b = 0         // branch tests for memory address 0 always fail 
            else
               b = 1			   // branch tests for negative addres always succeed
            if b:
               if F: C=N		  // in absolute mode, N species the address of M to branch to.
               else C += 2*N		  // in relative mode, N specifies the number of symbols to offset C by. 
               return 1 
      return 0
```

ZOMG bitcode runs inside a VM with the semantics given above.

The *ZOMG language* is composed of some combination of the symbools '0',1','#','?' where '0' represents the ZERO operation, 
'1' represents the ONE operation, '#' represents the MATH operation, and '?" represents the GO operation.

A compiler for this language accepts the above 4 ascii characters as input (and ignores all other characters).

'0' generates the **Z** bitcode (two zero bits), '1' generates the **O** bitcode (a zero bit followed by a one bit),
'#' generates the **M** bitcode (a one bit followed by a zero it), and '?' generates the **G** bitcode (two one bits).

# Examples (Code Snippets)

```
# Sets D = 0 (N is initially zero; adding zero clears D)
```

```
1# Sets D=C (Adding -0 sets D to C)
```

```
0? In absolute mode, switch to relative mode.
   In relative mode, flip bit at D and branch to current address if result is not 1 (set bit at D)
```

```
1? Set absolute mode (even if already in absolute mode)
```

```
1?0? Set relative mode
```

``` 
01? Flip bit at D. (If it's 1, jump ahead 1 to next instruction. Otherwise, go on to next instruction).
```


