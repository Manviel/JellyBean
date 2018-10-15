from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import FormView, ListView, UpdateView, View

import xlwt
from accounts.models import User
from accounts.tasks import notice_reply

from .forms import (BoardForm, GenerateRandomUserForm, NewTopicForm, PhotoForm,
                    PostForm)
from .models import Board, Photo, Post, Topic
from .render import Render
from .tasks import create_random_user_accounts


class BoardListView(ListView):
    model = Board
    template_name = 'home.html'
    context_object_name = 'boards'
    paginate_by = 5
    queryset = Board.objects.all()


class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_updated').annotate(
            replies=Count('posts') - 1
        )
        return queryset


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        session_key = 'viewed_topic_{}'.format(self.topic.pk)
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True

        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(
            Topic,
            board__pk=self.kwargs.get('pk'),
            pk=self.kwargs.get('topic_pk')
        )
        queryset = self.topic.posts.order_by('created_at')
        return queryset


class UsersListView(ListView):
    template_name = 'core/users_list.html'
    model = User


class GenerateRandomUserView(FormView):
    template_name = 'core/generate_users.html'
    form_class = GenerateRandomUserForm

    def form_valid(self, form):
        total = form.cleaned_data.get('total')
        create_random_user_accounts(total)
        messages.success(
            self.request,
            'We are generating your users! Wait a moment and refresh page'
        )
        return redirect('users_list')


class UploadView(View):
    def get(self, request):
        photos_list = Photo.objects.all()
        return render(
            self.request,
            'core/basic_upload.html',
            {'photos': photos_list}
        )

    def post(self, request):
        form = PhotoForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {
                'is_valid': True,
                'name': photo.file.name,
                'url': photo.file.url
            }
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


def get_pdf(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        topic = Topic.objects.get(topic_pk=topic_pk)
    params = {
        'topic': topic,
        'request': request
    }
    return Render.render('topic_posts.html', params)


def export_users_xls(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="my.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Topics')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Subject', 'Board', 'User', 'Views', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    topic = Topic.objects.all().values_list(
        'subject',
        'board',
        'starter',
        'views'
    )
    for row in topic:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def save_board_form(request, form, template_name, msg):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            boards = Board.objects.all()
            data['list'] = render_to_string(
                'includes/list.html',
                {'boards': boards}
            )
            data['msg'] = render_to_string(
                'includes/messages.html',
                {'message': msg}
            )
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html'] = render_to_string(
        template_name,
        context,
        request=request,
    )
    return JsonResponse(data)


def board_create(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
    else:
        form = BoardForm()
    return save_board_form(
        request,
        form,
        'board_create.html',
        'Has been created'
    )


def board_update(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = BoardForm(request.POST, instance=board)
    else:
        form = BoardForm(instance=board)
    return save_board_form(
        request,
        form,
        'board_update.html',
        'Has been updated'
    )


def board_delete(request, pk):
    board = get_object_or_404(Board, pk=pk)
    data = dict()
    if request.method == 'POST':
        board.delete()
        data['form_is_valid'] = True
        boards = Board.objects.all()
        data['list'] = render_to_string(
            'includes/list.html',
            {'boards': boards}
        )
        data['msg'] = render_to_string(
            'includes/messages.html',
            {'message': 'Has been deleted'}
        )
    else:
        context = {'board': board}
        data['html'] = render_to_string(
            'board_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)


@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})


@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            topic.last_updated = timezone.now()
            topic.save()

            topic_url = reverse(
                'topic_posts',
                kwargs={'pk': pk, 'topic_pk': topic_pk}
            )
            topic_post_url = '{url}?page={page}#{id}'.format(
                url=topic_url,
                id=post.pk,
                page=topic.get_page_count()
            )

            notice_reply(request.user.email)
            return redirect(topic_post_url)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message', )
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect(
            'topic_posts',
            pk=post.topic.board.pk,
            topic_pk=post.topic.pk
        )
