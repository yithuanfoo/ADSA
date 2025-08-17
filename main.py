import sys

# Helper functions

# Converts a string into a list of digits
def parse_digits(num_string):
    return [int(c) for c in num_string.strip()] # the strip function removes any spaces before it splits into digits

# Remove any leading zeros from list
def remove_zeros(digits):
    i = 0
    while i < len(digits) - 1 and digits[i] == 0:   # this makes sure that there will always be at leat one digit
        i += 1
    return digits[i:]

def school_addition(a, b, B):   # school method of addition with two values a, b and base B
    # Define variables
    i = len(a) - 1  # last digit of a
    j = len(b) - 1  # last digit of b
    carry = 0
    out = []

    while i >= 0 or j >= 0 or carry:    #  this loops through the digits from right to left until it has gone through evertything and there is no more carry
        digit_a = a[i] if i >= 0 else 0
        digit_b = b[j] if j >= 0 else 0
        total = digit_a + digit_b + carry

        if total >= B:  # this determines the new digit and carry
            digit = total - B
            carry = 1
        else:
            digit = total
            carry = 0

        out.append(digit)
        i -= 1
        j -= 1
    out.reverse()
    return remove_zeros(out)

def subtraction(a, b, B):   # subtrction needed for Karatsuba Multiplication
    # Define variables
    i = len(a) - 1  # last digit of a
    j = len(b) - 1  # last digit of b
    borrow = 0
    out = []
    
    while i >= 0:   # this loops through the digits from right to left until it has gone through all of a
        digit_a = a[i] - borrow
        digit_b = b[j] if j >= 0 else 0


        if digit_a < digit_b:   # check if we need to borrow
            digit_a += B
            borrow = 1
        else:
            borrow = 0

        out.append(digit_a - digit_b)
        i -= 1
        j -= 1
    out.reverse()
    return remove_zeros(out)

def school_multiplication(a, b, B):   # school multiplication needed for base case of Karatsuba Multuplication
    a = remove_zeros(a)
    b = remove_zeros(b)
    if a == [0] or b == [0]: return [0] # return 0 if a or b is 0

    # Find maximum digits result can have
    n = len(a)
    m = len(b)
    out = [0]*(n+m)

    # Multiplication
    for i in range(n-1, -1, -1):
        carry = 0
        for j in range(m-1, -1, -1):
            raw_sum = out[i+j+1] + a[i]*b[j] + carry # this holds the raw sum before it gets split
            out[i+j+1] = raw_sum % B # stores only the last digit
            carry = raw_sum // B  # the rest of the result becomes a carry
        out[i] += carry  # the leftover carry goes to the left digit
    return remove_zeros(out)

def karatsuba_multiplication(a, b, B):  # Karatsuba method of multiplication with two values a, b and base B
    a = remove_zeros(a)
    b = remove_zeros(b)
    if a == [0] or b == [0]: return [0] # return 0 if a or b is 0

    n = max(len(a), len(b))
    if n < 4:
        return school_multiplication(a, b, B)
    
    # Makes sure length is even
    if n % 2: 
        n += 1
    
    # Pad numbers with zeros
    a = [0]*(n-len(a)) + a
    b = [0]*(n-len(b)) + b
    
    # Split the numbers
    k = n // 2
    a1, a0 = a[:k], a[k:]
    b1, b0 = b[:k], b[k:]

    # Solve subproblems
    P0 = karatsuba_multiplication(a0, b0, B)
    P2 = karatsuba_multiplication(a1, b1, B)
    P1 = karatsuba_multiplication(school_addition(a0, a1, B), school_addition(b0, b1, B), B)
    mid = subtraction(subtraction(P1, P2, B), P0, B)

    P2_shifted = P2 + [0]*(2*k)
    mid_shifted = mid + [0]*k

    # Combine the results of the subproblems
    out = school_addition(school_addition(P2_shifted, mid_shifted, B), P0, B)
    return remove_zeros(out)

# Main function
def main():
    input = sys.stdin.readline().strip() # read line of input
    sa, sb, sB = input.split()  # split into two numbers and base
    B = int(sB) # converts the base string into an integer

    a = parse_digits(sa)    # converts a into list of digits
    b = parse_digits(sb)    # converts b into list of digits

    addition = school_addition(a, b, B) # calls the school_addition function
    multiplication = karatsuba_multiplication(a, b, B)  # calls karatsuba_multiplication function
    division = [0]  # returns 0 as division is not required

    # Converts digits back into strings and removes any leading zeros
    addition_str = ''.join(str(d) for d in remove_zeros(addition))  
    multiplication_str = ''.join(str(d) for d in remove_zeros(multiplication))
    division_str = '0'  

    print(addition_str, multiplication_str, division_str)   # prints results in one line
    main()  # calls main function