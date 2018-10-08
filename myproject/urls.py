from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.flatpages import views as flat
from django.urls import include, path

from accounts import views as accounts_views
from boards import views

urlpatterns = [
    path('', views.BoardListView.as_view(), name='home'),
    path('boards/create/', views.board_create, name='board_create'),
    path(
        'boards/<int:pk>/',
        views.TopicListView.as_view(),
        name='board_topics'
    ),
    path('boards/<int:pk>/new/', views.new_topic, name='new_topic'),
    path('boards/<int:pk>/update/', views.board_update, name='board_update'),
    path('boards/<int:pk>/delete/', views.board_delete, name='board_delete'),
    path(
        'boards/<int:pk>/topics/<int:topic_pk>/',
        views.PostListView.as_view(),
        name='topic_posts'
    ),
    path(
        'boards/<int:pk>/topics/<int:topic_pk>/reply/',
        views.reply_topic,
        name='reply_topic'
    ),
    path(
        'boards/<int:pk>/topics/<int:topic_pk>/posts/<int:post_pk>/edit/',
        views.PostUpdateView.as_view(),
        name='edit_post'
    ),
    path('signup/', accounts_views.choose, name='signup'),
    path(
        'signup/blogger/',
        accounts_views.BloggerSignUpView.as_view(),
        name='blogger_signup'
    ),
    path(
        'signup/reader/',
        accounts_views.ReaderSignUpView.as_view(),
        name='reader_signup'
    ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='login.html'),
        name='login'
    ),
    path(
        'reset/',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html',
            email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt'
        ),
        name='password_reset'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uuid:uidb64>/<str:token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
    path('settings/', accounts_views.settings, name='settings'),
    path(
        'settings/password/',
        auth_views.PasswordChangeView.as_view(
            template_name='password_change.html'
        ),
        name='password_change'
    ),
    path(
        'settings/password/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='password_change_done.html'
        ),
        name='password_change_done'
    ),
    path(
        'settings/account/',
        accounts_views.updateView,
        name='my_account'
    ),
    path(
        'pages/privacy/',
        flat.flatpage,
        {'url': '/pages/privacy'},
        name='privacy'
    ),
    path(
        'pages/terms/',
        flat.flatpage,
        {'url': '/pages/terms'},
        name='terms'
    ),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('admin/', admin.site.urls)
]
