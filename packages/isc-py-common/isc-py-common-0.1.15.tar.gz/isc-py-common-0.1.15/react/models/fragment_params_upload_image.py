import logging

from django.db import transaction

from isc_common.http.DSResponse import JsonResponseWithException
from isc_common.models.upload_image import Common_UploadImage
from isc_common.models.users_images import Users_images
from lfl_admin.user_ext.models.administrators import Administrators

logger = logging.getLogger(__name__)


@JsonResponseWithException()
class DSResponse_Fragment_params_UploadImage(Common_UploadImage):
    def __init__(self, request):
        from react.models.fragment_params import Fragment_params

        with transaction.atomic():
            file = request.FILES.get('upload_attatch')
            if file is not None:
                image, fragment_id = self.upload_image(request=request)
                res, created = Fragment_params.objects.update_or_create(fragment_id=fragment_id, defaults=dict(image=image))
                logger.debug(f'Created: {created}')
