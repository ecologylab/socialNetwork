from django.db.models import Q
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from friends.models import Friendship, FriendshipInvitation, Blocking
from friends.forms import InviteFriendForm, RemoveFriendForm, BlockUserForm
from friends import settings as friends_settings


@login_required
def list_friends(request):
    """
    Lists friends of currently logged user.
    """
    friends = Friendship.objects.friends_for_user(request.user)
    return render_to_response('friends/friends_list.html',
                              {'friends': friends},
                              context_instance=RequestContext(request))


@login_required
def list_friend_friends(request, username):
    """
    Lists friends of user friend.
    """
    # showing friends of friends can be disabled or enabled in settings
    if not friends_settings.SHOW_FRIENDS_OF_FRIEND:
        raise PermissionDenied

    user = get_object_or_404(User, username=username)

    # check if user specified by username is friend of current user
    if not Friendship.objects.are_friends(request.user, user):
        raise PermissionDenied

    friends = Friendship.objects.friends_for_user(user)
    return render_to_response('friends/friends_of_friend.html',
                              {'friends': friends,
                               'friend': user},
                              context_instance=RequestContext(request))


@login_required
def invite_friend(request, username, redirect_to_view=None, message=_("I would like to add you to my friends.")):
    """
    Invite user to be user friend.
    """
    friend = get_object_or_404(User, username=username)
    if request.method == "POST":
        form = InviteFriendForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _("Friendship invitation for %(username)s was created.") % {'username': username}, fail_silently=True)
            if not redirect_to_view:
                redirect_to_view = list_sent_invitations
            return redirect(redirect_to_view)
    else:
        form = InviteFriendForm(initial={'to_user': username, 'message': message})
    return render_to_response('friends/friend_invite.html',
                              {'form': form,
                               'friend': friend},
                              context_instance=RequestContext(request))


@login_required
def remove_friend(request, username, redirect_to_view=None):
    """
    Remove user from friends.
    """
    friend = get_object_or_404(User, username=username)
    if request.method == "POST":
        form = RemoveFriendForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _("User %(username)s was removed from friends.") % {'username': username}, fail_silently=True)
            if not redirect_to_view:
                redirect_to_view = list_friends
            return redirect(redirect_to_view)
    else:
        form = RemoveFriendForm(initial={'to_user': username})
    return render_to_response('friends/friend_remove.html',
                              {'form': form,
                               'friend': friend},
                              context_instance=RequestContext(request))


@login_required
def block_user(request, username, redirect_to_view=None):
    """
    Block user from sending invitations.
    """
    to_user = get_object_or_404(User, username=username)
    if request.method == "POST":
        form = BlockUserForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _("User %(username)s was blocked from sending invitations.") % {'username': username}, fail_silently=True)
            FriendshipInvitation.objects.remove(to_user, request.user)
            if not redirect_to_view:
                redirect_to_view = list_blocked_users
            return redirect(redirect_to_view)
    else:
        form = BlockUserForm(initial={'to_user': username})
    return render_to_response('friends/user_block.html',
                              {'form': form,
                               'blocked': to_user},
                              context_instance=RequestContext(request))


@login_required
def unblock_user(request, username, redirect_to_view=None):
    """
    Unblock user from sending invitations.
    """
    to_user = get_object_or_404(User, username=username)
    blocking = Blocking.objects.filter(from_user=request.user, to_user=to_user)
    blocking.delete()

    messages.success(request, _("User %(username)s was unblocked from sending invitations.") % {'username': username}, fail_silently=True)

    if not redirect_to_view:
        redirect_to_view = list_blocked_users
    return redirect(redirect_to_view)


@login_required
def list_blocked_users(request):
    """
    Lists users blocked from sending invitations.
    """
    blocked = Blocking.objects.blocked_for_user(request.user)
    return render_to_response('friends/blocked_users_list.html',
                              {'friends': blocked},
                              context_instance=RequestContext(request))


@login_required
def list_received_invitations(request):
    """
    List invitations received by user.
    """
    invitations = FriendshipInvitation.objects.filter(to_user=request.user)
    return render_to_response('friends/invitations_list.html',
                              {'invitations': invitations,
                               'status': 'received'},
                              context_instance=RequestContext(request))


@login_required
def list_sent_invitations(request):
    """
    List invitations sent by user.
    """
    invitations = FriendshipInvitation.objects.filter(from_user=request.user)
    return render_to_response('friends/invitations_list.html',
                              {'invitations': invitations,
                               'status': 'sent'},
                              context_instance=RequestContext(request))


@login_required
def show_invitation(request, invitation_id):
    """
    Show friendship invitation.
    """
    invitation = get_object_or_404(FriendshipInvitation,
        Q(to_user=request.user) | Q(from_user=request.user),
        pk=invitation_id
    )
    return render_to_response('friends/invitation_show.html',
                              {'invitation': invitation},
                              context_instance=RequestContext(request))


@login_required
def remove_invitation(request, invitation_id, redirect_to_view=None):
    """
    Remove invitation (only sender shoul be able to remove invitation
    and only before it was accepted or rejected).
    """
    invitation = get_object_or_404(FriendshipInvitation,
        Q(to_user=request.user) | Q(from_user=request.user),
        pk=invitation_id
    )
    invitation.delete()
    messages.success(request, _("Invitation deleted."), fail_silently=True)
    if not redirect_to_view:
        redirect_to_view = list_friends
    return redirect(redirect_to_view)


@login_required
def respond_to_invitation(request, invitation_id, resp='a', redirect_to_view=None):
    """
    Accept or decline invitation.
    """
    invitation = get_object_or_404(FriendshipInvitation,
        to_user=request.user,
        pk=invitation_id
    )
    if resp == 'a':
        invitation.accept()
        messages.success(request, _("Invitation accepted."), fail_silently=True)
    elif resp == 'd':
        invitation.decline()
        messages.success(request, _("Invitation declined."), fail_silently=True)
    if not redirect_to_view:
        redirect_to_view = list_friends
    return redirect(redirect_to_view)


