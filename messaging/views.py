from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden
from .models import Conversation, Message
from .forms import MessageForm

User = get_user_model()

class ConversationListView(LoginRequiredMixin, ListView):
    model = Conversation
    template_name = 'messaging/conversation_list.html'
    context_object_name = 'conversations'

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

class ConversationDetailView(LoginRequiredMixin, DetailView):
    model = Conversation
    template_name = 'messaging/conversation_detail.html'
    context_object_name = 'conversation'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conversation = self.get_object()
        if self.request.user not in conversation.participants.all():
            return HttpResponseForbidden()
        # Mark all messages as read
        conversation.messages.filter(sender__in=conversation.participants.exclude(id=self.request.user.id)).update(is_read=True)
        context['message_form'] = MessageForm()
        return context

class ConversationCreateView(LoginRequiredMixin, CreateView):
    model = Conversation
    template_name = 'messaging/conversation_form.html'
    fields = []

    def form_valid(self, form):
        other_user = get_object_or_404(User, id=self.kwargs['user_id'])
        if other_user == self.request.user:
            return redirect('messaging:conversation-list')
        
        # Check if conversation already exists
        conversation = Conversation.objects.filter(participants=self.request.user).filter(participants=other_user).first()
        if conversation:
            return redirect('messaging:conversation-detail', pk=conversation.pk)
        
        conversation = form.save()
        conversation.participants.add(self.request.user, other_user)
        return redirect('messaging:conversation-detail', pk=conversation.pk)

class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'messaging/message_form.html'

    def form_valid(self, form):
        conversation = get_object_or_404(Conversation, id=self.kwargs['pk'])
        if self.request.user not in conversation.participants.all():
            return HttpResponseForbidden()
        
        form.instance.conversation = conversation
        form.instance.sender = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('messaging:conversation-detail', kwargs={'pk': self.kwargs['pk']})
