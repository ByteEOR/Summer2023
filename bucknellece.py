'''
Author: Taeha Jeong
Team: Bucknell ECE Summer 2023 PrairieLearn Development
Version: v1.4
Date: 17 Jul 2023

Comment: A simple demo of usage of this library can be found here: https://us.prairielearn.com/pl/course/510/question/9127117/preview
'''

import random
import numpy
import si_prefix
from eseries import find_nearest, E6


'''
This will generate a real resistor value without a prefix (i.e. 1000 instead of 1k)
Use "convStr()" function below to generate string with a SI prefix
By default, it will choose one of E6 series resistor values
'''
def genResistor(low, high, series=E6):
    num = 0
    while num == 0:
        num = random.uniform(low, high)
    res = find_nearest(E6, num)
    return res


'''
1) For unit, use one of: yzafpnumkMGTPEZY (m is mili, k is kilo, etc)
    1.1) To generate standard unit (without SI prefix), you don't need to pass paramters to `unit` argument
    1.2) Both 'u' and 'μ' supported for micro SI prefix
2) If no unit is wanted, leave the third argument blank
3) This will generate a floating point number (i.e. 1 mili-something to 0.001), up to five sig-figs
'''
def genNum(low, high, unit=' '):
    num = 0
    while num == 0:
        num = random.uniform(low, high)

    if (unit == 'u') or (unit == 'μ'):
        num = num*si_prefix.si_prefix_scale('\xb5')
    else:
        num = num*si_prefix.si_prefix_scale(unit)
    
    num = si_prefix.split(num)
    num = round(num[0], 2)*(10**num[1])

    return num


'''
1) Since resistor with real values are preferred,
   this function will return power, voltage, and current with power < assigned power (defulat is 250mW).
2) This will generate V and I with up to five sig-figs, and P which is equal to V*I
'''
def genWatt(R, pLim = 0.25):
    P = pLim + 1
    while (P > pLim):
        P = random.uniform(1e-15, pLim)
    I = numpy.sqrt(P/R)
    V = P/I

    V = si_prefix.split(V)
    I = si_prefix.split(I)


    V = round(V[0], 2)*(10**V[1])
    I = round(I[0], 2)*(10**I[1])
    P = V*I

    return P, V, I


'''
While it is easier to use floating point for mathematical calculations, we also want numbers to have SI-prefixes.
This function will convert the value to a string with proper SI prefix with two decimal digits.

Example usage:
    import bucknellece as ece
    
    R = ece.genResistor(1000, 7000)
    R_str = convStr(R)+'Ω'
    print(R_str)
    ...
    >> (some random resistor value) kΩ
'''
def convStr(input):
    return str(si_prefix.si_format(input, 2))


'''
1) This function will compare correct answer and student answer with 10% tolerance,
    returning True if student answer is within 10% tolerance range and False if not
2) This function should be located in `grade()/server.py`
3) Supported std_unit include: 'yzafpnμmkMGTPEZY' (both μ and u work for 'micro' SI prefix)
4) The submitted SI prefix (std_unit) is assigned as first character in student unit (i.e. 'm' if std_unit = 'mA'),
    so please keep this in mind; usage of `genUnit()` function below is recommended to avoid errors

Example code (in `server.py`):
    def grade(data):
        if bucknellece.compAns(correct_ans, data['submitted_answers'][question_asked], data['submitted_answers'][name_assigned_to_dropdown]):
            data['score'] = 1
        else:
            data['score'] = 0
'''
def compAns(correct_ans, std_ans, std_unit=' '):
    std_unit = std_unit[0]
    if (std_unit == 'μ') or (std_unit == 'µ') or (std_unit == 'u'): # The first and second 'mu's are different characters
        std_unit = '\xb5'
    elif std_unit not in 'yzafpnmkMGTPEZY':
        std_unit = ' '

    std_ans = std_ans*si_prefix.si_prefix_scale(std_unit)

    if abs(correct_ans - std_ans) <= abs(correct_ans*0.1):
        return True
    else:
        return False

'''
This function will generate a list of dictionaries used for dropdown.
1) The first argument takes in unit (in string; i.e. 'A', 'W', etc) to be displayed
2) For 'Ω', both 'ohm' or 'Ohm' can be put in as a unit
3) If single_unit = True, then a single unit given in first argument with different SI prefixes will be shown
4) If single_unit = False, then multiple units - A, V, W, etc - will be shown with an appropriate SI prefix.
    In this case, correct_ans (float) argument MUST BE assigned.
'''
def genUnit(desired_unit = '', single_unit = True, correct_ans = 42):
    if (desired_unit == 'Ohm') or (desired_unit == 'ohm'):
        desired_unit = 'Ω'
    
    output_list = []
    multi_unit_list = ['A', 'V', 'W', 'C', 'F', 'Ω', 'H', 'J', 'S', 'T']

    if single_unit == True:
        for i in 'pnμm kMGTP':
            output_list.append({'tag': 'false', 'unit': i.strip()+desired_unit})
            output_list[0]['tag'] = 'true'
    else:
        correct_ans = str(si_prefix.si_format(correct_ans))
        correct_ans_unit = correct_ans[-1]
        for j in multi_unit_list:
            output_list.append({'tag': 'false', 'unit': correct_ans_unit.strip()+j})
            for k in range(len(output_list)-1):
                if output_list[k]['unit'] in (correct_ans_unit.strip()+desired_unit):
                    output_list[k]['tag'] = 'true'
    
    return output_list