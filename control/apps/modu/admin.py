from django.contrib import admin
from .models import DistriModel
from .models import PartableModel
from .models import TimetableModel
from .models import SignalModel
from .models import AisdataModel
# Register your models here.

# admin.site.register([DistriModel])


@admin.register(DistriModel)
class DistriModelAdmin(admin.ModelAdmin):
    list_display = ("id",
                    "user",
                    "distri_id",
                    "distri_lon",
                    "distri_lat",
                    "distri_height",
                    "distri_ves_num",
                    "distri_mode",
                    "create_datetime",
                    "deleted",
                    "deleted_at"
                    )

@admin.register(PartableModel)
class PartableModelAdmin(admin.ModelAdmin):
    list_display = ("id",
                    "distri",
                    "pitch",
                    "azimuth",
                    "antenna_type",
                    "channel_type",
                    "create_datetime",
                    "deleted",
                    "deleted_at"
                    )

@admin.register(TimetableModel)
class TimetableModelAdmin(admin.ModelAdmin):
    list_display = ("id",
                    "distri",
                    "partable",
                    "obtime",
                    "protocol",
                    "create_datetime",
                    "deleted",
                    "deleted_at"
    )

@admin.register(AisdataModel)
class AisdataModelAdmin(admin.ModelAdmin):
    list_display = ("id",
                    "distri",
                    "timetable",
                    "create_datetime",
                    "deleted",
                    "deleted_at"
                    )
@admin.register(SignalModel)
class SignalModelAdmin(admin.ModelAdmin):
    list_display = ("id",
                    "partable",
                    "timetable",
                    "snr",
                    "create_datetime",
                    "deleted",
                    "deleted_at"
                    )