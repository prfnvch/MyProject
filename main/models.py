from django.utils import timezone
from django.db import models
from django.urls import reverse
from accounts.models import User
from django.db.models import Avg, Count

def manga_image_upload_path(instance, filename):
    return f"mangas/{instance.chapter.manga.title}/{instance.chapter.number}/{filename}"


class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def getGenreUrl(self):
        return reverse("catalog-genres", args=[self.id])
    

class Author(models.Model):
    firstName = models.CharField(max_length=100, blank=True)
    lastName = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.firstName} {self.lastName}"

    def getAuthorUrl(self):
        return reverse("author-index", args=[self.firstName, self.lastName, self.id])

    def getFullName(self):
        return f"{self.firstName} {self.lastName}"


class Manga(models.Model):
    title = models.TextField()
    type = models.TextField(null=True)
    description = models.TextField()
    publication_date = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to="mangas/covers/", blank=True, default="book-placeholder.jpeg")
    genre = models.ManyToManyField(Genre)
    author = models.ForeignKey(Author, on_delete=models.PROTECT, null=True, related_name="books")
    bookmarks = models.ManyToManyField(User, blank=True, related_name="users")
    created = models.DateField(null=True, blank=True)
    status = models.TextField(null=True, blank=True)
    age_restriction = models.TextField(null=True, blank=True)
    language = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    def getGenre(self):
        return ", ".join([genre.name for genre in self.genre.all()])

    def get_date(self):
        return self.publication_date.strftime("%Y")
    
    def get_follow_url(self):
        return reverse("manga-follow", args=[self.id])

    def get_manga_url(self):
        return reverse("manga-index", args=[self.type, self.title])
    
    def likes_count(self):
        return len(self.likes.all())
    
    def get_bookmarks(self):
        return len(self.bookmarks.all())
    
    def get_all_genres(self):
        default_genres = Genre.objects.all()
        genres = list(default_genres)
        return genres
    
    def get_date(self):
        return self.created.strftime("%Y")


    getGenre.short_description = "Genre"

    try:
        def average_rating(self) -> float:
            return Rating.objects.filter(manga=self).aggregate(Avg("rating"))["rating__avg"] or 0
    except:
        pass

    try:
        def rating_count(self) -> float:
            return Rating.objects.filter(manga=self).aggregate(Count("rating"))["rating__count"] or 0
    except:
        pass

    def list_of_commented_users(self):
        user_list = []
        for comment in self.comments.all():
            user_list.append(comment.user)
        return user_list


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f"{self.manga.title}: {self.rating}"
    

class Chapter(models.Model):
    manga = models.ForeignKey(Manga, on_delete=models.PROTECT, null=True, blank=True)
    name = models.TextField()
    number = models.IntegerField(blank=True, null=True)
    added = models.DateTimeField(blank=True, null=True, default=timezone.now)

    def get_chapter_url(self):
        return reverse("chapter-index", args=[self.manga.type, self.manga.title, self.number])
    
    def get_next_chapter_url(self):
        return reverse("chapter-index", args=[self.manga.type, self.manga.title, self.number+1])
    
    def get_previous_chapter_url(self):
        return reverse("chapter-index", args=[self.manga.type, self.manga.title, self.number-1])
    
    class Meta:
        get_latest_by = 'added'

    def list_of_commented_users(self):
        user_list = []
        for comment in self.comments.all():
            user_list.append(comment.user)
        return user_list
    

class MangaChapter(models.Model):
    chapter = models.ForeignKey(
        Chapter, on_delete=models.PROTECT, related_name="chapters")
    chapter_image = models.ImageField(null=True, blank=True,
                              upload_to=manga_image_upload_path)

    def images_count(self):
        return len(self.chapter.all())



class MangaComment(models.Model):
    content = models.TextField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='manga_comments')
    created = models.DateTimeField(auto_now_add=True)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE, related_name='manga_comments')
    likes = models.ManyToManyField(User)

    def get_likecomment_url(self):
        return reverse("comment-like", args=[self.id])

    def likes_count(self):
        return len(self.likes.all())

    def comments_count(self):
        return len(MangaComment.objects.all())


class ChapterComment(models.Model):
    content = models.TextField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chapter_comments')
    created = models.DateTimeField(auto_now_add=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='chapter_comments')
    likes = models.ManyToManyField(User)

    def get_likecomment_url(self):
        return reverse("comment-ch-like", args=[self.id])

    def likes_count(self):
        return len(self.likes.all())

    def comments_count(self):
        return len(ChapterComment.objects.all())
