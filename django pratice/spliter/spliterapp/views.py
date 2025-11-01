from django.shortcuts import render
from .forms import TextInputForm 

def index(request):
    form = TextInputForm(request.POST or None)           
    results_data = None 

    if request.method == 'POST' and form.is_valid():
        input_text = form.cleaned_data['text']
        number = []
        uppercase = []
        lowercase = []
        specialchar = []
        
        for char in input_text:
            
            if char.isdigit():
                number.append(char)
            elif char.isalpha():
                
                if char.isupper():
                    uppercase.append(char)
                elif char.islower():
                    lowercase.append(char)
            else:
                specialchar.append(char)

        
        totalletters = len(uppercase) + len(lowercase)
        
        categorized_lists = {
            'Numbers': ''.join(number),
            'Uppercase Letters': ''.join(uppercase),
            'Lowercase Letters': ''.join(lowercase),
            'Special Characters': ''.join(specialchar),
        }

        results_data = {
            'input_text': input_text,
            'total_length': len(input_text),
            'total_alphabets': totalletters,
            'total_numbers': len(number),
            'total_special': len(specialchar),
            'categories': categorized_lists,
        }
    context = {
        'form': form,
        'results': results_data,
    }
    return render(request, 'index.html', context)