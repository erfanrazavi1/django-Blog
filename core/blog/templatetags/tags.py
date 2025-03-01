import jdatetime
from django import template
from blog.models import Post
from django.shortcuts import render

register = template.Library()

@register.filter
def to_jalali(value):
    if value:
        return jdatetime.datetime.fromgregorian(datetime=value).strftime("%Y/%m/%d")
    return ""

@register.simple_tag
def get_all_posts():
    return Post.objects.all()