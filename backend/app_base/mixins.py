from django.db import models

class CustomIDMixin(models.Model):
    custom_id = models.CharField(max_length=255, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.custom_id:
            last_instance = self.__class__.objects.order_by('-id').first()
            last_id = last_instance.id if last_instance else 0
            self.custom_id = f"{self._meta.object_name.lower()}_{last_id + 1}"
        super().save(*args, **kwargs)

    class Meta:
        abstract = True