from django.db import models


class Author(models.Model):
    """Author."""

    salutation = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    headshot = models.ImageField(upload_to='authors', null=True, blank=True)

    class Meta:
        """Meta options."""

        ordering = ["id"]

    def __str__(self):
        return self.name
