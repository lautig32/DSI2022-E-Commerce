from django.contrib.auth.models import User, AbstractUser
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.db import models
from django_upload_path.upload_path import auto_cleaned_path_stripped_uuid4


class UserProfile(AbstractUser):
    email = models.EmailField(_('correo electronico'), blank=False, null=True, unique=True,)
    first_name = models.CharField(_('nombre'), max_length=50, blank=False,)
    last_name = models.CharField(_('apellido'), max_length=50, blank=False, )
    document_number = models.CharField(_('documento'), max_length=30, null=True, blank=True,)
    profile_picture = models.ImageField(_('foto de perfil'), upload_to=auto_cleaned_path_stripped_uuid4, null=True,
                                       blank=True)
    address = models.CharField(_('domicilio'), max_length=50, blank=False, null=True, )
    number_adress = models.IntegerField(_('numero de domicilio'), blank=False, null=True, )
    number_phone = models.IntegerField(_('numero de telefono'), blank=False, null=True, )
    description = models.TextField(_("descripción"), blank=True, null=True, )

    is_staff = models.BooleanField(
        _("staff status"),
        default=True,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def profile_picture_short_tag(self):
        if self.profile_picture:
            url_image = self.profile_picture.url
            return format_html("""<img src='{}' width='40'"/>""", url_image)
        return "-"
    profile_picture_short_tag.short_description = _('foto de perfil')
    profile_picture_short_tag.allow_tags = True

    def profile_picture_medium_tag(self):
        if self.profile_picture:
            url_image = self.profile_picture.url
            return format_html("""<img src='{}' height='160'"/>""", url_image)
        return "-"
    profile_picture_medium_tag.short_description = _('foto de perfil')
    profile_picture_medium_tag.allow_tags = True

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        if not self.password:
            self.set_password(str(self.document_number))
        super(UserProfile, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        if self.is_active:
            self.is_active = False
            self.save()
        else:
            super(UserProfile, self).delete(using, keep_parents)

    def __str__(self):
        if self.document_number:
            return "%s - %s" % (self.get_full_name(), self.document_number)
        else:
            return self.get_full_name()


class AddressUserProfile(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='AdrresUserProfile_user')
    #province = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='AdrresUserProfile_province')
    #location = models.ForeignKey(UserProfile, on_delete=models.PROTECT, related_name="NoteClaim_author")
    postal_code = models.IntegerField(_('codigo postal'), blank=False, null=True)
    street = models.CharField(_('calle'), max_length=100, blank=False, null=True)
    number_adress = models.IntegerField(_('numero de calle'), blank=False, null=True)

    class Meta:
        verbose_name = 'direccion'
        verbose_name_plural = 'direcciones'

    def __str__(self):
        return self.location