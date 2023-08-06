from django.contrib import admin
from .models import Commit, Human, Branch, Changelog


class CommitAdmin(admin.ModelAdmin):
    model = Commit
    list_display = ('hash', 'head', 'body', 'branch', 'tag_name', 'executed')
    readonly_fields = ('hash', 'head', 'body', 'branch', 'tag_name')
    fields = (*readonly_fields, 'executed')
    search_fields = ('hash', 'head', 'body', 'tag_name')
    list_filter = ('executed', 'branch', 'created_at')


class HumanAdmin(admin.ModelAdmin):
    model = Human
    list_display = ('name', 'email', 'user', 'master', 'beta')
    search_fields = list_display
    list_filter = ('master', 'beta')


admin.site.register(Commit, CommitAdmin)
admin.site.register(Human, HumanAdmin)
