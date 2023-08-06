from django.db import models
from django.contrib.auth import get_user_model


class ShellSettings(models.Model):
    code_before = models.TextField(null=True)
    code_after = models.TextField(null=True)

class Command(models.Model):
    text = models.TextField(null=True)
    output = models.TextField(null=True)
    error = models.TextField(null=True)
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    user = models.ForeignKey(get_user_model()(), related_name="sh_commands", on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ("-id",)
    
    def to_dict(self):
        return {
            "id": self.pk,
            "output": self.output,
        }

class SavedCommand(models.Model):
    user = models.ForeignKey(get_user_model()(), related_name="sh_saved_commands", on_delete=models.CASCADE)
    command = models.ForeignKey(Command, related_name="users", on_delete=models.PROTECT)
    description = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)