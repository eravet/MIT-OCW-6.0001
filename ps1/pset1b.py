# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 15:21:50 2020

@author: ericd
"""

#Part A: House Hunting

import math

#prompt user for variables
annual_salary = input("Enter starting salary: ")
portion_saved = input("What portion, as a decimal, do you want to save? ")
total_cost = input("What is the total cost of your dream home? ")
semi_annual_raise = input("Enter a semi-annual raise: ")

#set variables, r = investment return
portion_down_payment = 0.25
current_savings = 0
r = 0.04

#calculations for formula
total_down_payment = portion_down_payment * float(total_cost)
monthly_r = r / 12
monthly_saved = float(portion_saved) * float(annual_salary) / 12
m = 0

while total_down_payment > current_savings:
    current_savings = current_savings + current_savings * r / 12 + monthly_saved    
    
    if m%6 == 0 and m > 0:
        annual_salary = int(annual_salary)*(1 + float(semi_annual_raise))
        monthly_saved = float(portion_saved) * float(annual_salary) / 12
    m = m + 1

print(m)