from django.http import HttpResponse
# https://www.runoob.com/django/django-views-fbv-cbv.html
def musicQA(request):
    issue = request.GET.get("issue")
    ans = "这是答案！" 
    return HttpResponse(ans)