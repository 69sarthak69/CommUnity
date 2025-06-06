from django.db import models
from django.conf import settings

class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=50)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_groups')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='joined_groups', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def member_count(self):
        return self.members.count()

    def __str__(self):
        return self.name
    

class GroupPost(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='group_posts/', blank=True, null=True)   
    created_at = models.DateTimeField(auto_now_add=True)

class GroupPostReaction(models.Model):
    post = models.ForeignKey('GroupPost', related_name='reactions', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=10, default='like')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user', 'reaction_type')

class GroupActivity(models.Model):
    group = models.ForeignKey('Group', on_delete=models.CASCADE, related_name='activities')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=50) 
    post = models.ForeignKey('GroupPost', on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    extra = models.TextField(blank=True, null=True) 

    def __str__(self):
        return f"{self.user} {self.activity_type} {self.group} @ {self.timestamp}"


