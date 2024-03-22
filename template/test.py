def evaluate_equation(equation, tc, c):
    result = int(eval(equation, {'tc': tc, 'c': c}))
    return result

equation = "(tc / 10000 + c) / 100"
totalCount = 50000
Counter = 200
result = evaluate_equation(equation, totalCount, Counter)
print(result)