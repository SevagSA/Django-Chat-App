from django import forms

from .models import ChatRoom, Message

from account.models import User


class PrivateChatSelectorForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=None,  # QS will be added in __init__
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = ChatRoom
        fields = ['room_name', 'users']

    def __init__(self, *args, **kwargs):
        self.current_user_id = kwargs.pop('request').user.id
        super(PrivateChatSelectorForm, self).__init__(*args, **kwargs)
        self.fields['users'].queryset = User.objects.exclude(
            id=self.current_user_id)

    def save(self):
        instance = super(PrivateChatSelectorForm, self).save()
        instance.is_private = True
        instance.save()
        instance.users.add(self.current_user_id)
        return instance


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message', 'message_media']

    def __init__(self, user, room, *args, **kwargs):
        self.user = user
        self.room = room
        super(MessageForm, self).__init__(*args, **kwargs)

    def save(self):
        instance = super(MessageForm, self).save(commit=False)
        instance.sender = self.user
        instance.chat_room = self.room
        instance.save()
        return instance
