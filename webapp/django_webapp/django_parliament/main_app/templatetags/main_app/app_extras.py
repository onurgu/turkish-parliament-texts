from django import template
register = template.Library()

@register.simple_tag
def access(xlist, index):
    return xlist[index]

@register.simple_tag
def divide(x,y):
    return x/y

