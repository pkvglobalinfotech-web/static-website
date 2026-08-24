from django.db import models
from django.contrib.auth.models import User



# Services Section

class Service(models.Model):

    title=models.CharField(max_length=100)

    description=models.TextField()

    icon=models.CharField(
        max_length=50,
        default="bi bi-code"
    )


    def __str__(self):
        return self.title



# Portfolio Projects

class Project(models.Model):
    title = models.CharField(max_length=150)
    technology = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="portfolio/")
    github = models.URLField(blank=True)
    live_demo = models.URLField(blank=True)

    def __str__(self):
        return self.title



# Blog CMS


class Blog(models.Model):

    title=models.CharField(
        max_length=200
    )

    image=models.ImageField(
        upload_to="blogs/"
    )


    content=models.TextField()


    author=models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )


    created=models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):

        return self.title



# Testimonials


class Testimonial(models.Model):

    name=models.CharField(
        max_length=100
    )


    company=models.CharField(
        max_length=100
    )


    message=models.TextField()


    image=models.ImageField(
        upload_to="testimonial/",
        blank=True
    )


    def __str__(self):

        return self.name




# Contact Database


class Contact(models.Model):

    name=models.CharField(
        max_length=100
    )


    email=models.EmailField()


    phone=models.CharField(
        max_length=15
    )


    message=models.TextField()


    created=models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):

        return self.name



# Newsletter


class Newsletter(models.Model):

    email=models.EmailField()


    created=models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):

        return self.email
