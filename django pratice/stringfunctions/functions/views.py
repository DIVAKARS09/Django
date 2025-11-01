from django.shortcuts import render
from .forms import StringInputForm

def index(request):
    form = StringInputForm(request.POST or None)
    results = None

    if request.method == 'POST' and form.is_valid():
        string = form.cleaned_data['string']
        search = form.cleaned_data['search']
        replace = form.cleaned_data['replace']
        
        uppercase = string.upper()
        
        lowercase = string.lower()
        
        try:
            indexvalue = string.index(search)
        except ValueError:
            indexvalue = f"'{search}' not found (ValueError would be raised)."
            
        split = string.split() 
        
        replace_result = string.replace(search, replace)
        
        count = string.count(search)
        
        reverse = string[::-1]
        
        words_list = string.split()

        implode = ' | '.join(words_list) 

        swap=string.swapcase()

        check=string.isalpha() 

        removeprefix=string.removeprefix(search)

        zeros=string.zfill(30)
       
        results = {
            'input': string,
            'upper': uppercase,
            'lower': lowercase,
            'index': indexvalue,
            'split': split,
            'replace': replace_result,
            'count': count,
            'reverse': reverse,
            'implode': implode,
            'swap':swap,
            'check':check,
            'removeprefix':removeprefix,
            'zeros':zeros
        }

    context = {
        'form': form,
        'results': results,
    }
    return render(request, 'index.html', context)