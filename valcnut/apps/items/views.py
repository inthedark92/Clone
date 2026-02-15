from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import InventoryItem

@login_required
def inventory_view(request):
    items = InventoryItem.objects.filter(user=request.user)
    return render(request, 'game/inventory.html', {'items': items})
