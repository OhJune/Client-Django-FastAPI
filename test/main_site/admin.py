from django.contrib import admin
from .models import board


class boardAdmin(admin.ModelAdmin):
    search_fields = ['subject']


admin.site.register(board, boardAdmin)