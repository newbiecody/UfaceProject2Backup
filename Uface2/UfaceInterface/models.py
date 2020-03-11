from django.db import models

# Create your models here.

class select1(models.Model):
    course_choices = (
            ('CZ3002', 'CZ3002'),
            ('CZ3003', 'CZ3003'),
        )
    Course = models.CharField(max_length=30, blank=True, null=True, choices=course_choices)

class select2(models.Model):
    index_choices = (
            ('10215', '10215'),
            ('10216', '10216'),
            ('10224', '10224'),
            ('10225', '10225'),
        )
    Index = models.CharField(max_length=30, blank=True, null=True, choices=index_choices)

class select3(models.Model):
    session_choices = (
            ('Lab1', 'Lab1'),
            ('Lab2', 'Lab2'),
            ('Lab3', 'Lab3'),
            ('Lab1', 'Lab1'),
            ('Lab2', 'Lab2'),
            ('Lab3', 'Lab3'),
            ('Lab1', 'Lab1'),
            ('Lab2', 'Lab2'),
            ('Lab3', 'Lab3'),
        )
    Session = models.CharField(max_length=30, blank=True, null=True, choices=session_choices)
