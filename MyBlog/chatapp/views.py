from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic import ListView, DetailView, TemplateView, View
from django.views.generic.edit import FormMixin

from chatapp.forms import ChatForm
from chatapp.models import Chat
from tempcheck.forms import CommentForm


# class UserMessageListView(ListView, LoginRequiredMixin):
#     model = User
#     template_name = 'chatapp/chat.html'
#     form_class = ChatForm
#
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data()
#         context['user_list'] = self.model.objects.exclude(username=self.request.user)
#
#         return context
from users.models import Profile


def chatajaxview(request):
    user_id = request.GET.get('user_id')
    print("In chat ajax function",user_id)
    data = {}
    # data['is_taken'] =
    print(data)
    return JsonResponse(data)


class UserMessageListView(TemplateView, LoginRequiredMixin):
    model = User
    # template_name ='chatapp/chat.html'
    # context_object_name = 'chat'
    template_name = 'chatapp/chat.html'
    form_class = ChatForm

    def get_context_data(self, **kwargs):
        context = {}
        context['form2'] = self.form_class
        # from_user = Chat.objects.filter(sendto=self.request.user, sendfrom=id)
        # to_user = Chat.objects.filter(sendfrom=self.request.user, sendto=id)
        # merge_queryser = from_user | to_user
        # user_chats = merge_queryser.all()
        # context['user_chats'] = user_chats
        # print(context['user_chats'])
        context['user_list'] = self.model.objects.exclude(username=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        if request.method == "POST" and 'userpost' in request.POST:
            form = ChatForm(request.POST)
            if form.is_valid():
                context = self.get_context_data(request=request)
                user_id = self.request.POST.get('userid')
                from_user = Chat.objects.filter(sendto=self.request.user, sendfrom=user_id)
                to_user = Chat.objects.filter(sendfrom=self.request.user, sendto=user_id)
                merge_queryser = from_user | to_user
                user_chats = merge_queryser.all()
                context['user_chats'] = user_chats
                context['user_id1'] = user_id
                context['userimg'] = Profile.objects.filter(user=user_id)
                image = Profile.objects.filter(user=user_id)
                for i in image:
                    print(i.image.url)
                    context['user_image'] = i.image.url
                    context['user_username'] = i.user.username
                return render(request, self.template_name, context=context)
            else:
                return ChatForm()
        elif request.method == "POST" and 'chatpost' in request.POST:
            form = ChatForm(request.POST)
            print(" inside chat post ")
            if form.is_valid():

                context = self.get_context_data(request=request)
                # user_id = request.GET.get('user_id')

                user_id = self.request.POST.get('uservalue')
                print(user_id)
                print(Profile.objects.filter(user=user_id))
                form.instance.sendfrom = self.request.user
                form.instance.sendto = User.objects.get(id=user_id)
                form.save()
                from_user = Chat.objects.filter(sendto=self.request.user, sendfrom=user_id)
                to_user = Chat.objects.filter(sendfrom=self.request.user, sendto=user_id)
                merge_queryser = from_user | to_user
                user_chats = merge_queryser.all()
                context['user_chats'] = user_chats
                context['user_id1'] = user_id
                image = Profile.objects.filter(user=user_id)
                for i in image:
                    print(i.image.url)
                    context['user_image'] = i.image.url
                    context['user_username'] = i.user.username
                return render(request, self.template_name, context=context)
            else:
                return ChatForm()

        return HttpResponseRedirect(self.request.path_info)










#
# class MessageDetailView(TemplateView, LoginRequiredMixin):
#     # model = Chat
#     # template_name ='chatapp/chat.html'
#     # context_object_name = 'chat'
#     form_class = ChatForm
#
#     def get_context_data(self, **kwargs):
#         context = {}
#         context['form'] = self.form_class
#         from_user = Chat.objects.filter(sendto=self.request.user, sendfrom=self.kwargs['pk'])
#         to_user = Chat.objects.filter(sendfrom=self.request.user, sendto=self.kwargs['pk'])
#         merge_queryser = from_user | to_user
#         user_chats = merge_queryser.all()
#         context['user_chats'] = user_chats
#         return context
#
#     def post(self, request, *args, **kwargs):
#         if request.method == "POST":
#             form = ChatForm(request.POST)
#             if form.is_valid():
#                 form.instance.sendfrom = self.request.user
#                 form.instance.sendto = User.objects.get(id=self.kwargs['pk'])
#                 form.save()
#                 context = self.get_context_data(request=request)
#                 return render(request, self.template_name, context=context)
#             else:
#                 return ChatForm()
#         return HttpResponseRedirect(self.request.path_info)