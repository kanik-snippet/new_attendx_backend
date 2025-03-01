from django.shortcuts import render

def qr_test_page(request):
    return render(request, "test.html")
