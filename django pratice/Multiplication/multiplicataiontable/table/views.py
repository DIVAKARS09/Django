from django.shortcuts import render
from .forms import MultiplicationForm

def index(request):
    result = []
    rows = columns = 0

    if request.method == 'POST':
        form = MultiplicationForm(request.POST)
        if form.is_valid():
            rows = form.cleaned_data['rows']
            columns = form.cleaned_data['columns']

            # Generate table result
            for i in range(1, rows + 1):
                row = []
                for j in range(1, columns + 1):
                    row.append(f"{i}×{j}={i * j}")
                result.append(row)
    else:
        form = MultiplicationForm()

    return render(request, 'index.html', {
        'form': form,
        'result': result,
        'rows': rows,
        'columns': columns
    })
