# -*- coding: utf-8 -*-

# Copyright (C) 2007-2010, Salmaso Raffaele <raffaele@salmaso.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

def __init__():
    from django.conf import settings

    # patch user creation forms to allow more characters in username
    if 'django.contrib.auth' in settings.INSTALLED_APPS:
        from django.contrib.auth.models import User
        from django import forms
        from django.utils.translation import ugettext_lazy as _
        from django.contrib.auth import forms as auth_forms

        class UserCreationForm(forms.ModelForm):
            username = forms.RegexField(label=_("Username"), max_length=30, regex=r'^\w[\w.\-\+]*$',
                help_text = _("Required. 30 characters or fewer. Use letters, digits, underscores, dots,'-' and '+'."),
                error_message = _("This value must contain only letters, numbers, underscores, dots, '-' and '+' signs."))
            password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
            password2 = forms.CharField(label=_("Password confirmation"), widget=forms.PasswordInput)

            class Meta:
                model = User
                fields = ("username",)

            def clean_username(self):
                username = self.cleaned_data["username"]
                try:
                    User.objects.get(username=username)
                except User.DoesNotExist:
                    return username
                raise forms.ValidationError(_("A user with that username already exists."))

            def clean_password2(self):
                password1 = self.cleaned_data.get("password1", "")
                password2 = self.cleaned_data["password2"]
                if password1 != password2:
                    raise forms.ValidationError(_("The two password fields didn't match."))
                return password2

            def save(self, commit=True):
                user = super(UserCreationForm, self).save(commit=False)
                user.set_password(self.cleaned_data["password1"])
                if commit:
                    user.save()
                return user

        class UserChangeForm(forms.ModelForm):
            username = forms.RegexField(label=_("Username"), max_length=30, regex=r'^\w[\w.\-\+]*$',
                help_text = _("Required. 30 characters or fewer. Use letters, digits, underscores, dots,'-' and '+'."),
                error_message = _("This value must contain only letters, numbers, underscores, dots, '-' and '+' signs."))

            class Meta:
                model = User

        auth_forms.UserCreationForm = UserCreationForm
        auth_forms.UserChangeForm = UserChangeForm
__init__()

