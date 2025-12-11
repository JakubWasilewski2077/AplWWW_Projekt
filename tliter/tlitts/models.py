from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tlitt(models.Model):
    contents = models.TextField(max_length=140)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        contents_skr = self.contents.split()
        if len(contents_skr) <= 10:
            return self.contents
        return " ".join(contents_skr[:10]) + "..."

class Comment(models.Model):
    contents = models.TextField(max_length=140)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    tlitt = models.ForeignKey(Tlitt, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        contents_skr = self.contents.split()
        if len(contents_skr) <= 10:
            return self.contents
        return " ".join(contents_skr[:10]) + "..."


class Hashtag(models.Model):
    contents = models.CharField(max_length=50, unique=True)
    tlitts = models.ManyToManyField('Tlitt', blank=True)

    class Meta:
        ordering = ['contents']

    def __str__(self):
        return f"#{self.contents}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tlitt = models.ForeignKey(Tlitt, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'tlitt')

    def __str__(self):
        return f"#{self.user} lubi {self.tlitt.id}"

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower} follows {self.following}"