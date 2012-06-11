from django import template

from friends.models import Friendship, FriendshipInvitation


register = template.Library()


class AreFriendsNode(template.Node):
    """
    Returns True if two users are friends, False otherwise.
    """
    def __init__(self, user1, user2, varname=None):
        self.user1 = user1
        self.user2 = user2
        self.varname = varname

    def render(self, context):
        user1 = self.user1.resolve(context)
        user2 = self.user2.resolve(context)
        if user1.is_anonymous() or user2.is_anonymous():
            friends = False
        else:
            if Friendship.objects.are_friends(user1, user2):
                friends = True
            else:
                friends = False
        if self.varname:
            context[self.varname] = friends
            return ""
        return friends


@register.tag
def are_friends(parser, token):
    bits = token.split_contents()
    tag_name = bits[0]
    bits = bits[1:]
    if len(bits) == 4:
        if bits[2] != "as":
            raise template.TemplateSyntaxError("This tag should be used like: "
                "{%% %s user1 user2 [as varname] %%}" % tag_name)
        return AreFriendsNode(
            parser.compile_filter(bits[0]),
            parser.compile_filter(bits[1]),
            bits[3]
        )
    elif len(bits) == 2:
        return AreFriendsNode(
            parser.compile_filter(bits[0]),
            parser.compile_filter(bits[1])
        )
    else:
        raise template.TemplateSyntaxError("This tag should be used like: "
            "{%% %s user1 user2 [as varname] %%}" % tag_name)
