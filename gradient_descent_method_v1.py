# Below is an attempt at implementing the gradient/steepest descent
# algorithm. Can be used to find the local minimum of a differentiable
# funciton, and a golbal minimum if the function is convex.
#
# The idea is to take a fucntion f and starting point x_k, and 
# iteratively 'take steps' in a 'direction' towards the mininum,
# i.e. we want to find a such that x_(k+1) = x_k + a*s(x_k) minimises f.
# For this, we solve d/da f(x_k + a*s(x_k)) = 0 (*), where s(x_k) is a 
# descent direction. We can take s(x_k) = -g(x_k), where g is the
# gradient vector of f.      
# Note that (*) simplifies to g(x_k + a*s(x_k))^T*g(x_k).  

import sympy
import numpy

# Input the variables for your function. 
x = sympy.symbols('x', real = True)
y = sympy.symbols('y', real = True)
variables = [x,y]

# Step length variable
a = sympy.symbols('a', real = True)

# Choosing a starting point
start = numpy.array([1, -2])

# Enter your function here
f = x**2 - 4*x + 5*y**2 + 30*y + 50

print('Your chosen function:',f)
print('\n')

# Calcuates the gradient vector of f at a given point
def gradient_at_a_point(c_j, variables, gradient):
    i = 0
    x_0 = {variables[i]: c_j[i] for i in range(len(variables))}
    nabla = numpy.array([])
    while i < len(variables):
        g = gradient[i].evalf(subs=x_0)
        nabla = numpy.append(nabla, g)
        i += 1
    return nabla

# Returns the line x_k - a*g(x_k) as an array
def line_segment(c_j, nabla):
    line = numpy.array([])
    i = 0
    while i < len(nabla):
        l = c_j[i] - a*nabla[i]
        line = numpy.append(line,l)
        i += 1
    return line

# Returns f(x_k - a*g(x_k)) as an array
def f_line_segment(gradient, variables, line):
    subs_val = [(v, l) for (v, l) in zip(variables, line)]
    h = numpy.array([])
    i = 0
    while i < len(gradient):
        f_l = gradient[i].subs(subs_val)
        h = numpy.append(h,f_l)
        i += 1
    return h

def gradient_descent(f, variables, start):
    counter = 0
    c_j = start
    
    # Find the gradient vector of f
    gradient = numpy.array([])
    for variable in variables:
        gradient = numpy.append(gradient, sympy.diff(f,variable))

    print('Start point:', c_j)
    print('Start value:', f.evalf(subs={x:c_j[0], y: c_j[1]}))
    print('\n')
    
    nabla = gradient_at_a_point(c_j, variables, gradient) 
    nabla = numpy.array(nabla, dtype=numpy.float64)
    
    # Repeat the procedure described until the gradient is close to 0
    while numpy.linalg.norm(nabla) > 0.0000001:
        print('Iteration', counter + 1,':')
        nabla = gradient_at_a_point(c_j, variables, gradient) 
        nabla = numpy.array(nabla, dtype=numpy.float64)
        
        step_direction = -nabla
        print('Step direction:', step_direction)
        
        line = line_segment(c_j, nabla)
        
        f_line = f_line_segment(gradient, variables, line)
        expr = numpy.dot(f_line, nabla)
        
        # Should use a more powerful, numeric solver here
        step_length = sympy.solve(expr, a)
            
        print('eqn:', expr)
        print('step length:', step_length)
        
        c_j = c_j + step_length*step_direction
        print('New point:', c_j)
        print('New value:', f.evalf(subs={x:c_j[0], y: c_j[1]}))
        counter += 1
        print('\n')
        
    return None

gradient_descent(f, variables, start)
