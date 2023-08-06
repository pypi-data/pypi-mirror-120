# logicexp

A package which can help in calculating the result of any logical expression consisting of various logical operations. 

It would be very helpful when you have to calculate the result of a logical expression with given input values or to verify the correctness of your output. 


## Examples of How To Use

```Python
from logicexp import Nand, Nor, Not, Or, Xor,Calculate

print(Calculate(Xor(0,1)))
# 1
print(Calculate(Nor(1,0)))
# 0
print(Calculate(Or(Nand(1,1),Not(1))))
# 0

```

## Function Description
| Function | Description |
| :------------: |:---------------|
| Or | Represents Logical Or Operation |
| And | Represents Logical And Operation |
| Not | Represents Logical Not Operation |
| Xor | Represents Logical Xor Operation |
| Nand | Represents Logical Nand Operation |
| Nor | Represents Logical Nor Operation |
| Calculate | Calculates the result of logical expression |
