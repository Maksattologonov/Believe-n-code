from django.contrib import admin

from .models import CoursePrompt, PayboxUrl, Course


class CoursePromptAdmin(admin.ModelAdmin):
    pass


class UrlsAdmin(admin.ModelAdmin):
    pass


class CourseAdmin(admin.ModelAdmin):
    pass


admin.site.register(CoursePrompt, CoursePromptAdmin)
admin.site.register(PayboxUrl, UrlsAdmin)
admin.site.register(Course, CourseAdmin)
