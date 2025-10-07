from django.shortcuts import render

def index(request):
    ascii_results = None
    input_text = ""

    if request.method == 'POST':
        input_text = request.POST.get('text_input')
        
        if input_text:
            ascii_results = [
                {'char': char, 'value': ord(char)}
                for char in input_text
            ]
            
    context = {
        'ascii_results': ascii_results,
        'input_text': input_text,
    }
    
    return render(request, 'index.html', context)