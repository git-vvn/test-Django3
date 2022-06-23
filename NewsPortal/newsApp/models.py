from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from datetime import datetime


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)


    def update_rating(self):
        postRait = self.post_set.aggregate(postRating=Sum('rating'))
        pRait = 0
        if postRait.get('postRating'):
            pRait += postRait.get('postRating')

        commentRait = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRait = 0
        if commentRait.get('commentRating'):
            cRait += commentRait.get('commentRating')
        #Отличающийся способ получения рейтинга комментов к постам данного автора
        addRait = Post.objects.filter(author_id=self.authorUser.id) #QuerySet из всех постов автора
        commAPRait = 0
        if addRait:
            for elem in addRait:
                commObjct = Comment.objects.filter(commentPost_id=elem.id) #QuerySet из комментов
                for el in commObjct:
                    commAPRait += el.rating

        self.ratingAuthor = pRait*3 + cRait + commAPRait
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOISES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья')
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOISES, default=ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)


    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        #return self.text[0:4] + '...'
        return '{}... , rating = {}'.format(self.text[0:10], str(self.rating))

class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        #return self.text[0:5] + '...'
        return '{}... , rating = {}'.format(self.text[0:10], str(self.rating))