# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 15:21:50 2020

@author: ericd
"""

#Part A: House Hunting

import math

#prompt user for variables
input_salary = input("Enter starting salary: ")
annual_salary = int(input_salary)

total_cost = 1000000
portion_down_payment = 0.25
total_down_payment = portion_down_payment * float(total_cost)

r = 0.04
monthly_r = r / 12
semi_annual_raise = .07

current_savings = 0

#calculations for formula
p0 = 0
p100 = 10000
p = 10000
count = 0

while abs(total_down_payment - current_savings) > 100:
    portion_saved = p / 10000
    annual_salary = int(input_salary)
    current_savings = 0
    monthly_saved = float(portion_saved) * float(annual_salary) / 12
    
    for m in range(1,37,1):
        current_savings = current_savings + current_savings * r / 12 + monthly_saved
        
        if m%6 == 0 and m > 0:
            annual_salary = int(annual_salary)*(1 + float(semi_annual_raise))
            monthly_saved = float(portion_saved) * float(annual_salary) / 12
    
    print(int(current_savings), portion_saved, count)
    
    if total_down_payment < current_savings:
        print('Lower p')
        p100 = p
        p = (p + p0) // 2       
    else:
        if p == 10000:
            print('It is not possible to pay the down payment in three years.')
            break
        print('Raise p')
        p0 = p
        p = (p + p100) // 2        
    count += 1
if count > 0:
    print('Steps in bisection search:',count)