from django.contrib import admin
from django.urls import path
from .views import CreateChapterComment, CreateMangaComment, FilterView, LikeChapterComment, LikeMangaComment, MainView, MangaFilterView, ManhuaFilterView, ManhwaFilterView, SignUpView, UserView, FollowToMangaView, ManhwaListView, ManhuaListView, MangaListView, EntireView, MangaDetailView, ChapterView, SearchView
from . import views

urlpatterns = [
    path("", MainView.as_view(), name="main-index"),
    path("entire/", EntireView.as_view(), name="entire-list"),
    path("<str:type>/<str:title>", MangaDetailView.as_view(), name="manga-index"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("user-<int:id>/", UserView.as_view(), name="user"),
    path("user/follow-<int:id>/", FollowToMangaView.as_view(), name="manga-follow"),
    path("manhwa/", ManhwaListView.as_view(), name="manhwa-list"),
    path("manga/", MangaListView.as_view(), name="manga-list"),
    path("manhua/", ManhuaListView.as_view(), name="manhua-list"),
    path("<str:type>/<str:title>/chapter-<int:number>/", ChapterView.as_view(), name="chapter-index"),
    path('rate/<int:manga_id>/<int:rating>/', views.rate),
    path("search/", SearchView.as_view(), name='manga-search'),
    path("create_comment/", CreateMangaComment.as_view(), name="comment-create"),
    path("create_ch_comment/", CreateChapterComment.as_view(), name="comment-ch-create"),
    path("manga/comment/like-<int:id>/", LikeMangaComment.as_view(), name="comment-like"),
    path("chapter/comment/like-<int:id>/", LikeChapterComment.as_view(), name="comment-ch-like"),
    path('filter/', FilterView.as_view(), name="filter"),
    path('manga-filter/', MangaFilterView.as_view(), name="manga-filter"),
    path('manhwa-filter/', ManhwaFilterView.as_view(), name="manhwa-filter"),
    path('manhua-filter/', ManhuaFilterView.as_view(), name="manhua-filter"),
]
