from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username  = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    specification = models.CharField(max_length = 50)
    password = models.CharField(max_length=50)


    def __str__(self):
        return self.username


class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    publication_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class Page(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    page_number = models.IntegerField()
    content = models.TextField()

    def __str__(self):
        return f"Page {self.page_number} of {self.book.title}"

