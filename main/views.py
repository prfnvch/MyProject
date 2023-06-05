from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, View, DeleteView
from accounts.forms import UserRegistrationForm
from .models import ChapterComment, Genre, Manga, MangaChapter, Chapter, MangaComment, Rating
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from .forms import MangaCommentForm, ChapterCommentForm
from django.db.models import Q
from itertools import chain
User = get_user_model()


class MainView(TemplateView):
    template_name = "catalog/home.html"
    
    def get(self, request):
        mangas = Manga.objects.all().order_by('-created')
        liked = sorted(mangas, key=lambda manga: manga.rating_count(), reverse=True)
        other_user = User.objects.all().order_by('-date_joined')[:7]
        manga_comments = MangaComment.objects.all()
        manga_liked = sorted(manga_comments, key=lambda comment: comment.likes_count(), reverse=True)[:5]
        chapter_comments = ChapterComment.objects.all()
        chapter_liked = sorted(chapter_comments, key=lambda comment: comment.likes_count(), reverse=True)[:5]
        newest = Manga.objects.all().order_by('-publication_date')[:10]

        params = {
            'mangas': mangas,
            'liked': liked,
            'other_user': other_user,
            'manga_liked': manga_liked,
            'chapter_liked': chapter_liked,
            'newest': newest
        }
        
        return render(request, self.template_name, params)


class EntireView(TemplateView):
    template_name = "catalog/entire.html"
    
    def get(self, request):
        mangas = Manga.objects.all().order_by('-created')
        liked = sorted(mangas, key=lambda manga: manga.rating_count(), reverse=True)
        other_user = User.objects.all()
        genres = Genre.objects.all()

        params = {
            'mangas': mangas,
            'liked': liked,
            'other_user': other_user,
            'genres': genres
        }
        
        return render(request, self.template_name, params)


def index(request: HttpRequest) -> HttpResponse:
    mangas = Manga.objects.all()
    for manga in mangas:
        rating = Rating.objects.filter(manga=manga, user=request.user).first()
        manga.user_rating = rating.rating if rating else 0
    return render(request, "catalog/manga_detail.html", {"mangas": mangas})


def rate(request: HttpRequest, manga_id: int, rating: int) -> HttpResponse:
    manga = Manga.objects.get(id=manga_id)
    Rating.objects.filter(manga=manga, user=request.user).delete()
    manga.rating_set.create(user=request.user, rating=rating)
    return index(request)


class MangaDetailView(TemplateView):
    template_name = "catalog/manga_detail.html"

    def get(self, request, type, title):
        manga = Manga.objects.get(title=title)
        chapter = Chapter.objects.filter(manga=manga)
        other_user = User.objects.all()
        total = len(chapter.values_list('number'))
        comments = MangaComment.objects.filter(manga=manga)
        liked = sorted(comments, key=lambda comment: comment.likes_count(), reverse=True)
        recs = Manga.objects.filter(type=manga.type).order_by('?')
        recs = recs.exclude(title=manga.title)[:5]

        if request.user.is_authenticated:
            mangas = Manga.objects.filter(title=title)
            for manga in mangas:
                rating = Rating.objects.filter(manga=manga, user=request.user).first()
                manga.user_rating = rating.rating if rating else 0

        if request.user.is_authenticated:
            params = {
                'manga': manga,
                'chapter': chapter,
                'other_user': other_user,
                'total': total,
                'mangas': mangas,
                'comments': comments,
                'liked': liked,
                'recs': recs
            }
        else:
            params = {
                'manga': manga,
                'chapter': chapter,
                'other_user': other_user,
                'total': total,
            }

        return render(request, self.template_name, params)


class ChapterView(TemplateView):
    template_name="read/read.html"

    def get(self, request, type, title, number):
        manga = Manga.objects.get(title=title)
        chapters = Chapter.objects.filter(manga=manga)
        try:
            chapter = Chapter.objects.get(manga=manga, number=number)
            latest = True
        except:
            chapter = Chapter.objects.get(manga=manga, number=number-1)
            manga = Manga.objects.get(title=title)
            latest = False
        images = MangaChapter.objects.filter(chapter=chapter)
        comments = ChapterComment.objects.filter(chapter=chapter)
        liked = sorted(comments, key=lambda comment: comment.likes_count(), reverse=True)
        params = {
            'manga': manga,
            'chapter': chapter,
            'images': images,
            'chapters': chapters,
            'comments': comments,
            'liked': liked,
        }

        if latest is True:
            return render(request, self.template_name, params)
        else:
            return render(request, "read/latest_chapter.html", params)
        


class SignUpView(View):

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password2'])
            new_user.save()
            new_user = authenticate(username=user_form.cleaned_data['username'], password=user_form.cleaned_data['password2'])
            login(request, new_user)
            return redirect('main-index')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class UserView(TemplateView):
    template_name = "user/user.html"

    def get(self, request, id):
        user = User.objects.get(id=id)
        bookmarks = user.bookmarks.all().order_by('-created')
        manga_comments = MangaComment.objects.all()
        chapter_comments = ChapterComment.objects.all()
        comments = chain(manga_comments, chapter_comments)
        
        params = {
            'other_user': user,
            'bookmarks': bookmarks,
            'comments': comments,
        }

        return render(request, self.template_name, params)
    

class DeleteMangaCommentView(DeleteView):
    @method_decorator(login_required)
    def post(self, request):
        manga_comment = MangaComment.objects.get(id=request.POST['comment_id'])
        if request.user == manga_comment.user:
            manga_comment.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
class DeleteChapterCommentView(DeleteView):
    @method_decorator(login_required)
    def post(self, request):
        chapter_comment = ChapterComment.objects.get(id=request.POST['comment_id'])
        if request.user == chapter_comment.user:
            chapter_comment.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class FollowToMangaView(View):

    @method_decorator(login_required)
    def post(self, request, id):
        new_follow = Manga.objects.get(id=id)
        follows = request.user.bookmarks.all()

        if new_follow not in follows and new_follow != request.user:
            request.user.bookmarks.add(new_follow)
        else:
            request.user.bookmarks.remove(new_follow)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ManhwaListView(TemplateView):
    template_name = "catalog/manhwa.html"

    def get(self, request):
        manhwas = Manga.objects.filter(type__icontains="Manhwa")
        genres = Genre.objects.all()

        params = {
            "manhwas": manhwas,
            'genres': genres,
            
        }

        return render(request, self.template_name, params)


class MangaListView(TemplateView):
    template_name = "catalog/manga.html"

    def get(self, request):
        mangas = Manga.objects.filter(type__icontains="Manga")
        genres = Genre.objects.all()

        params = {
            "mangas": mangas,
            'genres': genres,
        }

        return render(request, self.template_name, params)
    

class ManhuaListView(TemplateView):
    template_name = "catalog/manhua.html"

    def get(self, request):
        manhuas = Manga.objects.filter(type__icontains="Manhua")
        genres = Genre.objects.all()

        params = {
            "manhuas": manhuas,
            'genres': genres,
        }

        return render(request, self.template_name, params)


class FilterView(TemplateView):
    template_name = "catalog/entire.html"
    
    def post(self, request):
        mangas = Manga.objects.all()
        genres = Genre.objects.all()

        try:
            filter = request.POST.getlist('manga')
            for filtering in filter:
                manga_by_type = Manga.objects.filter(type__iregex=filtering)
                manga_by_status = Manga.objects.filter(status__iregex=filtering)
                manga_by_age = Manga.objects.filter(age_restriction__iregex=filtering)
                manga_by_genre = Manga.objects.filter(genre__name__iregex=filtering)
                manga_by_all = manga_by_status.union(manga_by_type, manga_by_age, manga_by_genre)

                if len(filter) > 1:
                    for filtering in filter:
                        manga_by_type = Manga.objects.filter(type__iregex=filtering)
                        manga_by_status = Manga.objects.filter(status__iregex=filtering)
                        manga_by_age = Manga.objects.filter(age_restriction__iregex=filtering)
                        manga_by_genre = Manga.objects.filter(genre__name__iregex=filtering)
                        manga_of_loop = manga_by_status.union(manga_by_type, manga_by_age, manga_by_genre)
                        manga_by_all = manga_by_all.intersection(manga_of_loop)

            params = {
                'liked': manga_by_all,
                'mangas': mangas,
                'genres': genres,
            }

        except:
            mangas = Manga.objects.all()
            genres = Genre.objects.all()

            params = {
                'mangas': mangas,
                'liked': mangas,
                'genres': genres,
            }

        return render(request, self.template_name, params)
    

class MangaFilterView(TemplateView):
    template_name = "catalog/manga.html"
    
    def post(self, request):
        mangas = Manga.objects.all()
        genres = Genre.objects.all()

        try:
            filter = request.POST.getlist('manga')
            for filtering in filter:
                manga_by_status = Manga.objects.filter(Q(type="Manga") & Q(status__iregex=filtering))
                manga_by_age = Manga.objects.filter(Q(type="Manga") & Q(age_restriction__iregex=filtering))
                manga_by_genre = Manga.objects.filter(Q(type="Manga") & Q(genre__name__iregex=filtering))
                manga_by_all = manga_by_status.union(manga_by_age, manga_by_genre)

                if len(filter) > 1:
                    for filtering in filter:
                        manga_by_status = Manga.objects.filter(Q(type="Manga") & Q(status__iregex=filtering))
                        manga_by_age = Manga.objects.filter(Q(type="Manga") & Q(age_restriction__iregex=filtering))
                        manga_by_genre = Manga.objects.filter(Q(type="Manga") & Q(genre__name__iregex=filtering))
                        manga_of_loop = manga_by_status.union(manga_by_age, manga_by_genre)
                        manga_by_all = manga_by_all.intersection(manga_of_loop)

            params = {
                'mangas': manga_by_all,
                'genres': genres,
            }

        except:
            mangas = Manga.objects.filter(type__icontains="Manga")
            genres = Genre.objects.all()

            params = {
                'mangas': mangas,
                'genres': genres,
            }

        return render(request, self.template_name, params)   
    

class ManhwaFilterView(TemplateView):
    template_name = "catalog/manhwa.html"
    
    def post(self, request):
        mangas = Manga.objects.all()
        genres = Genre.objects.all()

        try:
            filter = request.POST.getlist('manga')
            for filtering in filter:
                manga_by_status = Manga.objects.filter(Q(type="Manhwa") & Q(status__iregex=filtering))
                manga_by_age = Manga.objects.filter(Q(type="Manhwa") & Q(age_restriction__iregex=filtering))
                manga_by_genre = Manga.objects.filter(Q(type="Manhwa") & Q(genre__name__iregex=filtering))
                manga_by_all = manga_by_status.union(manga_by_age, manga_by_genre)

                if len(filter) > 1:
                    for filtering in filter:
                        manga_by_status = Manga.objects.filter(Q(type="Manhwa") & Q(status__iregex=filtering))
                        manga_by_age = Manga.objects.filter(Q(type="Manhwa") & Q(age_restriction__iregex=filtering))
                        manga_by_genre = Manga.objects.filter(Q(type="Manhwa") & Q(genre__name__iregex=filtering))
                        manga_of_loop = manga_by_status.union(manga_by_age, manga_by_genre)
                        manga_by_all = manga_by_all.intersection(manga_of_loop)

            params = {
                'manhwas': manga_by_all,
                'genres': genres,
            }

        except:
            mangas = Manga.objects.filter(type__icontains="Manhwa")
            genres = Genre.objects.all()

            params = {
                'manhwas': mangas,
                'genres': genres,
            }

        return render(request, self.template_name, params)   
    

class ManhuaFilterView(TemplateView):
    template_name = "catalog/manhua.html"
    
    def post(self, request):
        mangas = Manga.objects.all()
        genres = Genre.objects.all()

        try:
            filter = request.POST.getlist('manga')
            for filtering in filter:
                manga_by_status = Manga.objects.filter(Q(type="Manhua") & Q(status__iregex=filtering))
                manga_by_age = Manga.objects.filter(Q(type="Manhua") & Q(age_restriction__iregex=filtering))
                manga_by_genre = Manga.objects.filter(Q(type="Manhua") & Q(genre__name__iregex=filtering))
                manga_by_all = manga_by_status.union(manga_by_age, manga_by_genre)

                if len(filter) > 1:
                    for filtering in filter:
                        manga_by_status = Manga.objects.filter(Q(type="Manhua") & Q(status__iregex=filtering))
                        manga_by_age = Manga.objects.filter(Q(type="Manhua") & Q(age_restriction__iregex=filtering))
                        manga_by_genre = Manga.objects.filter(Q(type="Manhua") & Q(genre__name__iregex=filtering))
                        manga_of_loop = manga_by_status.union(manga_by_age, manga_by_genre)
                        manga_by_all = manga_by_all.intersection(manga_of_loop)

            params = {
                'manhuas': manga_by_all,
                'genres': genres,
            }

        except:
            mangas = Manga.objects.filter(type__icontains="Manhua")
            genres = Genre.objects.all()

            params = {
                'manhuas': mangas,
                'genres': genres,
            }

        return render(request, self.template_name, params)   


class SearchView(TemplateView):
    template_name = "catalog/search_result.html"

    def post(self, request):
        search = request.POST['search']

        try:
            search_list = search.split()

            keyword = search_list.pop(0)
            manga_by_title = Manga.objects.filter(title__iregex=keyword)
            manga_by_status = Manga.objects.filter(status__iregex=keyword)
            # manga_by_genre = Manga.objects.filter(getGenre__iregex=keyword)
            manga_by_all = manga_by_title.union(manga_by_status)

            if len(search_list) > 0:
                for keyword in search_list:
                    manga_by_title = Manga.objects.filter(title__iregex=keyword)
                    manga_by_status = Manga.objects.filter(status__iregex=keyword)
                    # manga_by_genre = Manga.objects.filter(genre__iregex=keyword)
                    manga_of_loop = manga_by_title.union(manga_by_status)
                    manga_by_all = manga_by_all.union(manga_of_loop)

            caption = f'Search results for "{search}":' if manga_by_all else f'Your search - {search} - did not match any titles.'
            count = len([post for post in manga_by_all])

            params = {
                'mangas': manga_by_all,
                'title': f'Search - "{search}"',
                'caption': caption,
                'count': count,
            }

        except:
            params = {
                'title': f'Search - {search}"',
                'caption': "i can't find it..."
            }

        return render(request, self.template_name, params)


class CreateMangaComment(View):

    @method_decorator(login_required)
    def post(self, request):
        if request.method == 'POST':
            form = MangaCommentForm(request.POST)
            if form.is_valid():
                manga = Manga.objects.get(id=request.POST['manga_id'])
                new_comment = form.save(commit=False)
                new_comment.user = request.user
                new_comment.manga = manga
                new_comment.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            else:
                form = MangaCommentForm()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class CreateChapterComment(View):

    @method_decorator(login_required)
    def post(self, request):
        if request.method == 'POST':
            form = ChapterCommentForm(request.POST)
            if form.is_valid():
                chapter = Chapter.objects.get(id=request.POST['chapter_id'])
                new_comment = form.save(commit=False)
                new_comment.user = request.user
                new_comment.chapter = chapter
                new_comment.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            else:
                form = ChapterCommentForm()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class LikeMangaComment(View):
    @method_decorator(login_required)
    def post(self, request, id):
        current_comment = MangaComment.objects.get(id=id)
        likes = [user for user in current_comment.likes.all()]
        if request.user not in likes:
            current_comment.likes.add(request.user)
        else:
            current_comment.likes.remove(request.user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    

class LikeChapterComment(View):
    @method_decorator(login_required)
    def post(self, request, id):
        current_comment = ChapterComment.objects.get(id=id)
        likes = [user for user in current_comment.likes.all()]
        if request.user not in likes:
            current_comment.likes.add(request.user)
        else:
            current_comment.likes.remove(request.user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
