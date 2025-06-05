from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL

def user_media_path(instance, filename):
    # Store files in media/user_<id>/<type>/<filename>
    return f'user_{instance.user.id}/{instance._meta.model_name}/{filename}'

class UploadedFile(models.Model):
    FILE_TYPE_CHOICES = (
        ('csv', 'CSV'),
        ('sql', 'SQL'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_media_path)
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    table_name = models.CharField(max_length=64, blank=True, null=True)  # DB table name

    def __str__(self):
        return f"{self.user.username} - {self.file.name}"

class MLModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    model_file = models.FileField(upload_to=user_media_path, max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)
    algorithm = models.CharField(max_length=64)
    table_used = models.CharField(max_length=64)
    query = models.TextField()  

    def __str__(self):
        return f"{self.user.username} - {self.name}"

class QueryResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.TextField()
    response_text = models.TextField()
    response_table = models.JSONField(null=True, blank=True)
    graph_file = models.FileField(upload_to=user_media_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.query[:30]}"
