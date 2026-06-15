total, is_member = 150, True
has_coupon = True

if total >= 100: # condition is true (150 >= 100)
    discount = 10
    if is_member: # condition is true (is_member = True)
        discount += 5 # discount --> 15
        if has_coupon: # condition is true (has_coupon = True)
            discount += 10 # discount --> 25
    print(discount)
