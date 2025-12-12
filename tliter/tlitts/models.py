from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tlitt(models.Model):
    contents = models.TextField(max_length=140)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    hashtags = models.ManyToManyField("Hashtag", related_name="tagged_tlitts", blank=True)

    class Meta:
        permissions = [("tlitts.change_tlitt", "tlitts change tlitt"),
                       ("edit_delete_all_tlitts", "Użytkownik może edytować i usuwać posty każdego takkk")]
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
    #    permissions = [("can edit and delete all comments", "Użytkownik może edytować i usuwać komentarze każdego")]
        permissions = [("tlitts.change_comment", "tlitts change comment"),
                       ("edit_delete_all_comments", "Użytkownik może edytować i usuwać komentarz każdego takkk")]
        ordering = ['-created_at']

    def __str__(self):
        contents_skr = self.contents.split()
        if len(contents_skr) <= 10:
            return self.contents
        return " ".join(contents_skr[:10]) + "..."


class Hashtag(models.Model):
    contents = models.CharField(max_length=50, unique=True)

    class Meta:
        permissions = [("tlitts.change_hashtag", "tlitts change hashtag"),
                       ("edit_delete_all_hashtag", "Użytkownik może edytować i usuwać hasztagi takkk")]
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