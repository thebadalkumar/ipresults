from django.contrib import admin
from .models import BCA, rsFiles, Institute, MCA, Course, Batch

class rsFilesAdmin(admin.ModelAdmin):
    readonly_fields = ['id']
class ResultAdmin(admin.ModelAdmin):
    search_fields = ['enrollment','name']

admin.site.register(BCA, ResultAdmin)
admin.site.register(MCA, ResultAdmin)
admin.site.register(rsFiles, rsFilesAdmin)
admin.site.register(Institute)
admin.site.register(Course)
admin.site.register(Batch)