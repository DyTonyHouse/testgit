from django.shortcuts import render
from crm import models
# Create your views here.
def index(request):
    # users = models.UserProfile.objects.all()
    #
    # for user in users:
    #     roles = user.roles.all()
    #     for role in roles:
    #         menus = role.menus.all()
    #         for menu in menus:
    #             print(menu.name)
    return render(request, 'index.html')

def customer(request):

    return render(request, 'sales/customer.html')