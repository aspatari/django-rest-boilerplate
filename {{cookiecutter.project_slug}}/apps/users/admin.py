from django.contrib import admin
from . import models


# Register your models here.


@admin.register(models.User, models.Profile, models.Transaction)
class Admin(admin.ModelAdmin):
    '''
        Admin View for
    '''
    # list_display = ('',)
    # list_filter = ('',)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    # search_fields = ('',)

# admin.site.register(, Admin)
