from django.conf import settings
from rest_framework import serializers

from atv.exceptions import MaximumFileSizeExceededException
from utils.files import b_to_mb

from ..models import Attachment


class AttachmentSerializer(serializers.ModelSerializer):
    """Basic "read" serializer for the Attachment model"""

    href = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Attachment
        fields = (
            "id",
            "created_at",
            "updated_at",
            "filename",
            "media_type",
            "size",
            "href",
        )

    def get_href(self, instance) -> str:
        if request := self.context.get("request"):
            return request.build_absolute_uri(instance.uri)

        return instance.uri


class CreateAttachmentSerializer(serializers.ModelSerializer):
    """Create an Attachment associated to an anonymous document."""

    class Meta:
        model = Attachment
        exclude = (
            "size",
            "filename",
        )

    def validate(self, attrs):
        """Validate that the uploaded files are smaller than settings.MAX_FILE_SIZE."""
        if (size := attrs.get("file").size) > settings.MAX_FILE_SIZE:
            raise MaximumFileSizeExceededException(file_size=b_to_mb(size))

        return attrs
