from django.contrib import admin
from AuthApp.models import *

# Register your models here.



from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# Change the header text
admin.site.site_header = _("Quick Trading Administration")

# Optional: Change the title on the login page
admin.site.site_title = _("Quick Trading Administration")

# Optional: Change the index page title (the main page title)
admin.site.index_title = _("Quick Trading Administration")


admin.site.register(CustomUser)
admin.site.register(UserLoginActivity)
admin.site.register(OTP)
admin.site.register(Notifications)
admin.site.register(Team)
admin.site.register(Massege)
admin.site.register(MyRefeList)


admin.site.register(DynamicControlScheduling)

admin.site.register(MytodaysIncome)
