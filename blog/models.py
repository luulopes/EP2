from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200)  
    content = models.TextField()  
    date_posted = models.DateTimeField(auto_now_add=True)  
    image = models.ImageField(upload_to='images/', null=True, blank=True)  

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author if self.author else "Anônimo"} on {self.post}'
