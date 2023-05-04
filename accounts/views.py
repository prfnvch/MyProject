from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import ProfileEditForm
from django.contrib.auth import authenticate, login


class ProfileEditView(TemplateView):
    template_name = "user/edit_profile.html"

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, self.template_name)
        else:
            return redirect('user')

    def post(self, request):
        if request.user.is_authenticated:
            user_form = ProfileEditForm(request.POST, request.FILES, instance=request.user)

            if user_form.is_valid():
                edit_user = user_form.save()
                edit_user.save()

                return redirect('user', id=request.user.id)

            return render(request, self.template_name)
        else:
            return redirect('user')
