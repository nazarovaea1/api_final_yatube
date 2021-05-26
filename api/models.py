import textwrap

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200, verbose_name="Группа",
                             help_text="Выберите группу",)

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(
        "Дата публикации", auto_now_add=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts"
    )
    group = models.ForeignKey(Group, models.SET_NULL, blank=True, null=True,
                              related_name="posts",)

    def __str__(self):
        return textwrap.shorten(self.text, width=15)


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    created = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )

    def __str__(self):
        return textwrap.shorten(self.text, width=15)


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="follower")
    following = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name="following")

    class Meta:
        constraints = (
            models.UniqueConstraint(fields=("user", "following",),
                                    name="User cant follow someone twice"),)

    def __str__(self):
        return f"{self.user} follows {self.following}"
