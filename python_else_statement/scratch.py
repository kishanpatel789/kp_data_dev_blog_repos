# %%
for thing in []:
    print(thing)
else:
    print('nothing')


# %%
for thing in ['at', 'least', 'one']:
    print(thing)
else:
    print('nothing')


# %%
for thing in ['at', 'least', 'one']:
    print(thing)
    break
else:
    print('nothing') # only called if no break statement is present

# %%

while True:
    break
else:
    print('else hit') # only called if while statement becomes falsey and break is not hit


# %%
counter = 0
while counter < 10:
    counter += 1
    print(counter)
else:
    print('else hit')


# %%
try: 
    print('try block')
    # raise ValueError
    # raise SyntaxError
except SyntaxError:
    print('syntaxerror caught')
else:
    print('else statement')

