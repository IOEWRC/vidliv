from django import template


register = template.Library()


@register.filter
def is_file_field(field):
    return type(field.field).__name__ == 'ImageField'
