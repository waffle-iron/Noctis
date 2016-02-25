from django.contrib import admin

from .models import nProject
from .models import nProjectType
from .models import nProjectPart
from .models import nProjectPartType

admin.site.register(nProject)
admin.site.register(nProjectType)
admin.site.register(nProjectPart)
admin.site.register(nProjectPartType)