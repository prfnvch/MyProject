from django.contrib import admin
from .models import Author, ChapterComment, Genre, Manga, Chapter, MangaChapter, MangaComment, Rating


@admin.register(Manga)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "description", "publication_date", "author", "getGenre", "image", "likes_count", "get_bookmarks", "created", "status", "age_restriction")


@admin.register(Rating)
class MangaRating(admin.ModelAdmin):
    list_display = ("user", "manga", "rating")


class MangaChapterAdmin(admin.StackedInline):
    model = MangaChapter


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    inlines = [MangaChapterAdmin]


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("firstName", "lastName")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(MangaComment)
class MangaCommentAdmin(admin.ModelAdmin):
    list_display = ['content', 'user', 'created', 'likes_count']


@admin.register(ChapterComment)
class ChapterCommentAdmin(admin.ModelAdmin):
    list_display = ['content', 'user', 'created', 'likes_count']
