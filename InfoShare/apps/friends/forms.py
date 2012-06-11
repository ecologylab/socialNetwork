from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from friends.models import Friendship, FriendshipInvitation, Blocking


class UserForm(forms.Form):

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(UserForm, self).__init__(*args, **kwargs)


class InviteFriendForm(UserForm):

    to_user = forms.CharField(widget=forms.HiddenInput)
    message = forms.CharField(
        label=_("Message"),
        required=False,
        widget=forms.Textarea(attrs={"cols": "20", "rows": "5"})
    )

    def clean_to_user(self):
        to_username = self.cleaned_data["to_user"]
        try:
            User.objects.get(username=to_username)
        except User.DoesNotExist:
            raise forms.ValidationError(_(u"Unknown user."))
        return self.cleaned_data["to_user"]

    def clean(self):
        to_user = User.objects.get(username=self.cleaned_data["to_user"])
        if to_user == self.user:
            raise forms.ValidationError(
                _(u"You can't request friendship with yourself.")
            )
        if Friendship.objects.are_friends(self.user, to_user):
            raise forms.ValidationError(
                _(u"You are already friends with %(username)s.") % {'username': to_user.username}
            )
        blocking = Blocking.objects.filter(from_user=to_user, to_user=self.user)
        if blocking.count() > 0:
            raise forms.ValidationError(
                _(u"You can't invite %(username)s to friends.") % {'username': to_user.username}
            )
        previous_invitations_to = FriendshipInvitation.objects.filter(
            to_user=to_user,
            from_user=self.user,
        )
        if previous_invitations_to.count() > 0:
            raise forms.ValidationError(
                _(u"Already requested friendship with %(username)s.") % {'username': to_user.username}
            )
        previous_invitations_from = FriendshipInvitation.objects.filter(
            to_user=self.user,
            from_user=to_user,
        )
        if previous_invitations_from.count() > 0:
            raise forms.ValidationError(
                _(u"%(username)s has already requested friendship with you.") % {'username': to_user.username}
            )
        return self.cleaned_data

    def save(self):
        to_user = User.objects.get(username=self.cleaned_data["to_user"])
        message = self.cleaned_data["message"]
        invitation = FriendshipInvitation(
            from_user=self.user,
            to_user=to_user,
            message=message,
        )
        invitation.save()
        return invitation


class RemoveFriendForm(UserForm):

    to_user = forms.CharField(widget=forms.HiddenInput)

    def clean_to_user(self):
        to_username = self.cleaned_data["to_user"]
        try:
            User.objects.get(username=to_username)
        except User.DoesNotExist:
            raise forms.ValidationError(_(u"Unknown user."))
        return self.cleaned_data["to_user"]

    def clean(self):
        to_user = User.objects.get(username=self.cleaned_data["to_user"])
        if not Friendship.objects.are_friends(self.user, to_user):
            raise forms.ValidationError(
                _(u"%(username)s and you are not friends.") % {'username': to_user.username}
            )
        return self.cleaned_data

    def save(self):
        to_user = User.objects.get(username=self.cleaned_data["to_user"])
        Friendship.objects.remove(self.user, to_user)


class BlockUserForm(UserForm):

    to_user = forms.CharField(widget=forms.HiddenInput)

    def clean_to_user(self):
        to_username = self.cleaned_data["to_user"]
        try:
            User.objects.get(username=to_username)
        except User.DoesNotExist:
            raise forms.ValidationError(_(u"Unknown user."))
        return self.cleaned_data["to_user"]

    def clean(self):
        to_user = User.objects.get(username=self.cleaned_data["to_user"])
        if Friendship.objects.are_friends(self.user, to_user):
            raise forms.ValidationError(
                _(u"%(username)s and you are friends. You can't block user that is your friend.") % {'username': to_user.username}
            )
        return self.cleaned_data

    def save(self):
        to_user = User.objects.get(username=self.cleaned_data["to_user"])
        blocking = Blocking(
            from_user=self.user,
            to_user=to_user,
        )
        blocking.save()
        return blocking


