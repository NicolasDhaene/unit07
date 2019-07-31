from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django.forms import ModelForm, SelectDateWidget, EmailField, ValidationError
from .models import UserProfile
import re


class UserCreateForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        for fieldname in ["email", "password1", "password2"]:
            self.fields[fieldname].help_text = None

    class Meta:
        fields = [
            'email',
            'password1',
            'password2'
        ]
        model = get_user_model()


class UserProfileForm(ModelForm):

    class Meta:
        model = UserProfile
        widgets = {"date_of_birth": SelectDateWidget(attrs={"style": "width: 15%; "
                                                                     "display: inline-block; "
                                                                     "font-weight:normal"},
                                                     years=range(1900, 2100))
                   }
        fields = ["first_name", "last_name", "bio", "date_of_birth", "avatar", "country", "region", "city"]

    def clean(self):
        cleaned_data = super().clean()
        bio = cleaned_data.get("bio")
        if len(bio) < 10 and len(bio) != 0:
            raise ValidationError("Your Bio cannot be that short. Try with more than 10 characters")
        return cleaned_data


class EditAccountForm(ModelForm):
    verify_email = EmailField(label="Verify email address.")

    class Meta:
        model = get_user_model()
        fields = ["email", "verify_email"]

    def clean(self):
        data = self.cleaned_data
        email = data.get("email")
        verify = data.get("verify_email")

        if email != verify:
            raise ValidationError(
                "Both email field must match")


class ChangePasswordForm(PasswordChangeForm):

    class Meta:
        fields = ["new_password1", "new_password2"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields["new_password1"].help_text = (
            "<ul>\n"
            "<li>Must not be the same as the current password</li>\n"
            "<li>Minimum password length of 14 characters</li>\n"
            "<li>Must use of both uppercase and lowercase letters</li>\n"
            "<li>Must include one or more numerical digits</li>\n"
            "<li>Must include at least one special character, such as @, #, or $</li>\n"
            "<li>Cannot contain your username or parts of your full name, such as your first name</li>\n"
            "</ul>"
        )

    def clean(self):
        user = self.request.user
        new_password = self.cleaned_data.get('new_password1')
        old_password = self.cleaned_data.get('old_password')

        if user.check_password(old_password):
            if new_password == old_password:
                raise ValidationError(
                    "New password cannot match the old password.")
        else:
            raise ValidationError("Old password is not correct. Please try again. ")

        if not re.search("([a-z])+", new_password) or not re.search("([A-Z])+", new_password):
            raise ValidationError("The new password must use both uppercase and lowercase letters.")

        if len(new_password) < 14:
            raise ValidationError("The new password must be at least 14 characters long.")

        if not re.search("\d+", new_password):
            raise ValidationError("The new password must include one or more numerical digits.")

        if not re.search("([@#$])+", new_password):
            raise ValidationError("The new password must include the at least one of these : @, #, or $.")

        user_first_name = user.userprofile.first_name.lower()
        user_last_name = user.userprofile.last_name.lower()

        if user_first_name in new_password.lower() or user_last_name in new_password.lower():
            raise ValidationError("The new password cannot contain your username or parts of your full name.")

        return self.cleaned_data

