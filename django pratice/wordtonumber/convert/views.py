from django.shortcuts import render
from num2words import num2words

def index(request):
    final_result = None
    user_number_input = ""
    error_message = None
    selected_case = 'title'

    if request.method == 'POST':
        user_number_input = request.POST.get('number_input', '').strip()
        selected_case = request.POST.get('case_format', 'title')
        
        if user_number_input:
            try:
                if '.' in user_number_input:
                    number = float(user_number_input)
                else:
                    number = int(user_number_input)

                result_raw = num2words(number, lang='en_IN')
               
                if selected_case == 'upper':
                    final_result = result_raw.upper()
                elif selected_case == 'lower':
                    final_result = result_raw.lower()
                else:
                    final_result = result_raw.title()
                
            except ValueError:
                error_message = "Invalid input. Please enter a valid number"

    context_data = {
        'final_result': final_result,
        'user_number_input': user_number_input,
        'error_message': error_message,
        'selected_case': selected_case, 
    }
    
    return render(request, 'index.html', context_data)
