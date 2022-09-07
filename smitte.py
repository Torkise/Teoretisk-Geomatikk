
#Initializing list of values, with value at x = 0
s_values = [1.0]
i_values = [10/5e6]
r_values = [0.0]

b = 1/3 
k = 1/10 

# SiR function.
def updateSIR(s_y, i_y, r_y, b, k): 
    # Formulas for the values S, I and R. 
    # Formula from assignment text. 
    s = s_y - b*s_y * i_y 
    i = i_y + b*s_y*i_y - k*i_y 
    r = r_y + k*i_y
    return s, i, r


for i in range(120): 
    s_y, i_y, r_y = s_values[-1], i_values[-1], r_values[-1]
    s, i, r = updateSIR(s_y, i_y, r_y, b, k)
    s_values.append(s), i_values.append(i), r_values.append(r)

f = open("pan.csv", 'w')
for i in range(121):
    f.write(f'{i}, {s_values[i]:.3e}, {i_values[i]:.3e}, {r_values[i]:.3e}\n') 
f.write("Hils Odin og si at broren han er jævlig god til å progge. ")

f.close()