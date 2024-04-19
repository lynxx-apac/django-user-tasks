"""
REST API serialization classes.
"""

from rest_framework import serializers

from .models import UserTaskArtifact, UserTaskStatus


class ArtifactSerializer(serializers.ModelSerializer):
    """
    REST API serializer for the UserTaskArtifact model.
    """

    file = serializers.SerializerMethodField()

    class Meta:
        """
        Artifact serializer settings.
        """

        model = UserTaskArtifact
        fields = ('name', 'created', 'modified', 'status', 'file', 'text', 'url')

    def get_file(self, obj):
        """
        Get the URL of the artifact's associated file data.

        Arguments:
            obj (UserTaskArtifact): The artifact being serialized

        Returns:
            six.text_type: The URL of the artifact's file field (empty if there isn't one)

        """
        if not obj.file:
            return ''
        return obj.file.url


class StatusSerializer(serializers.ModelSerializer):
    """
    REST API serializer for the UserTaskStatus model.
    """

    artifacts = ArtifactSerializer(many=True, read_only=True)

    class Meta:
        """
        Status serializer settings.
        """

        model = UserTaskStatus
        fields = (
            'name', 'state', 'state_text', 'completed_steps', 'total_steps', 'attempts', 'created', 'modified',
            'artifacts'
        )

