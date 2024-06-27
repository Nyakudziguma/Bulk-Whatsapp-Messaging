from django.contrib import admin
from .models import *

class ResponsesAdmin(admin.ModelAdmin):
    list_display=('batch','phone_number','response','status', 'created_at', 'updated_at')

class TemplateAdmin(admin.ModelAdmin):
    list_display=('name','value',)

class MessageAdmin(admin.ModelAdmin):
    list_display=('template','message', 'created_at', 'updated_at')

class SessionAdmin(admin.ModelAdmin):
    list_display=('user','state','position', 'created_at', 'updated_at')

class PromotionAdmin(admin.ModelAdmin):
    list_display=('file','message', 'created_at', 'updated_at')



admin.site.register(BulkMessages, MessageAdmin)
admin.site.register(Templates, TemplateAdmin)
admin.site.register(MessageResponse, ResponsesAdmin)
admin.site.register(Sessions, SessionAdmin)
admin.site.register(Promotions, PromotionAdmin)
admin.site.register(Locations, PromotionAdmin)