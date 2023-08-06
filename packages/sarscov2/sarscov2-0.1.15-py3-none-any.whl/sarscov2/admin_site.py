from edc_model_admin.admin_site import EdcAdminSite

from .apps import AppConfig

sarscov2_admin = EdcAdminSite(name="sarscov2_admin", app_label=AppConfig.name)
