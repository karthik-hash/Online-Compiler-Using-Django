from django.shortcuts import render
import os
from ipware import get_client_ip

def home(request):
    ip = get_client_ip(request)
    return render(request, 'home.html', {'ip' : ip[0]})
 
def compile(request):
    
    ip = get_client_ip(request)

    if request.method == 'POST':
        lang = request.POST.get('select1')
        if lang == 'Python3':
            source = python(request)
            if source[0] == 'Reset':
                return render(request, 'home.html', {'ip' : ip[0]})
            else:
                return render(request, 'home.html', {'ip' : ip[0], 'program': source[1], 'in': source[2], 'out': source[3]})
        elif lang == 'C++':
            source = cplus(request)
            if source[0] == 'Reset':
                return render(request, 'home.html', {'ip' : ip[0]})
            else:
                return render(request, 'home.html', {'ip' : ip[0], 'program': source[1], 'in': source[2], 'out': source[3]})
        else:
            source = c(request)
            if source[0] == 'Reset':
                return render(request, 'home.html', {'ip' : ip[0]})
            else:
                return render(request, 'home.html', {'ip' : ip[0], 'program': source[1], 'in': source[2], 'out': source[3]})

def python(request):

    program = request.POST.get('program')

    s = request.POST.get('select2')
    
    f = open('program.py','w')
    f.write(program)
    f.close()

    inp = request.POST.get('input')
    i = open('in','w')
    i.write(inp)
    i.close()
    
    if 'os.system' in program or 'Popen' in program:
        return [s, program, inp, "You can't use system() or Popen() here due to security purposes."]

    os.system('python3 program.py < in > out 2> error')
    
    o = open('out')
    output = o.read()
    o.close()

    e = open('error')
    error = e.read()
    e.close()
    
    os.system('rm in out error program.py')
    
    return [s, program, inp, output+error]

def cplus(request):

    program = request.POST.get('program')

    s = request.POST.get('select2')

    f = open('program.cpp','w')
    f.write(program)
    f.close()

    inp = request.POST.get('input')
    i = open('in','w')
    i.write(inp)
    i.close()

    if 'system' in program or 'popen' in program:
       return [s, program, inp, "You can't use system() or popen() here due to security purposes."]

    os.system('g++ program.cpp 2> error')

    e = open('error')
    error = e.read()
    e.close()

    if error != '':
        os.system('rm in a.out error program.cpp')
        return [s, program, inp, error]
    
    a = os.system('./a.out < in > out 2> error')
    
    o = open('out')
    output = o.read()
    o.close()

    os.system('rm in a.out out error program.cpp')

    if a == 35584:
        return [s, program, inp, output+'\n'+'Segmentation fault (core dumped)']
    else:
        return [s, program, inp, output+error]

def c(request):
    
    program = request.POST.get('program')
    
    s = request.POST.get('select2')

    f = open('program.c','w')
    f.write(program)
    f.close()

    inp = request.POST.get('input')
    i = open('in','w')
    i.write(inp)
    i.close()

    if 'system' in program or 'popen' in program:
       return [s, program, inp, "You can't use system() or popen() here due to security purposes."]
    
    os.system('gcc program.c 2> error')

    e = open('error')
    error = e.read()
    e.close()

    if error != '':
        os.system('rm in a.out error program.c')
        return [s, program, inp, error]
    
    a = os.system('./a.out < in > out 2> error')
    
    o = open('out')
    output = o.read()
    o.close()

    os.system('rm in a.out out error program.c')

    if a == 35584:
        return [s, program, inp, output+'\n'+'Segmentation fault (core dumped)']
    else:
        return [s, program, inp, output+error]

