from django.shortcuts import render, redirect, get_object_or_404
from .models import Image
from .forms import ImageForm

# Display the slider
def index(request):
    images = Image.objects.all()
    return render(request, 'index.html', {'images': images})

# Upload image form
def upload_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ImageForm()
    return render(request, 'upload.html', {'form': form})


def delete_image(request, pk):
    image = get_object_or_404(Image, pk=pk)
    image.delete()
    return redirect('index')
