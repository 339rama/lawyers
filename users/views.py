from django.shortcuts import render, redirect
from .models import CustomUser

def ConfirmEmail(request, uuid):
    if uuid:
        user = CustomUser.objects.get(uuid=uuid)
        user.is_active = True
        user.save(update_fields=['is_active'])
        success = 'Success'
        return render(request, 'confirm.html', {
            'success': success,
        })