"""
REST API endpoints.
"""
from pathlib import Path

from rest_framework import mixins, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .conf import settings
from .models import UserTaskArtifact, UserTaskStatus
from .serializers import ArtifactSerializer, StatusSerializer
import logging

logger = logging.getLogger(__name__)


class DjangoObjectPermissionsIncludingView(permissions.DjangoObjectPermissions):
    """
    Django REST Framework object permissions including ``<app>.view_<model>``.

    Yields better response codes than using the superclass directly, assuming
    you've defined a view_* permission for the models.  The rationale for
    overriding perms_map is described in the Django REST framework
    documentation for `permissions`_ and `filters`_.

    .. _permissions: http://www.django-rest-framework.org/api-guide/permissions/#djangoobjectpermissions
    .. _filters: http://www.django-rest-framework.org/api-guide/filtering/#djangoobjectpermissionsfilter
    """

    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
        'HEAD': ['%(app_label)s.view_%(model_name)s'],
        'POST': ['%(app_label)s.cancel_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class StatusViewSet(
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """
    REST API endpoints for user-triggered asynchronous tasks.

    The status of a task can be viewed, listed, deleted, or used to cancel the
    underlying task.
    """

    filter_backends = settings.USER_TASKS_STATUS_FILTERS
    permission_classes = ([])
    queryset = UserTaskStatus.objects.order_by('-created')
    serializer_class = StatusSerializer

    @action(detail=True, methods=['post'])
    def cancel(self, request, *args, **kwargs):
        """
        Cancel the task associated with the specified status record.

        Arguments:
            request (Request): A POST including a task status record ID

        Returns:
            Response: A JSON response indicating whether the cancellation succeeded or not

        """
        status = self.get_object()
        status.cancel()
        serializer = StatusSerializer(status, context={'request': request})
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        for artifact in instance.artifacts.all():
            try:
                bundle_path = Path(artifact.file.path)
                bundle_path.unlink()
            except (ValueError, FileNotFoundError, NotADirectoryError, NotImplementedError) as e:
                logger.warning(f'Could not delete artifact {artifact.file.path} : {e}', exc_info=True)
        return super().destroy(request, *args, **kwargs)


class ArtifactViewSet(viewsets.ReadOnlyModelViewSet):
    """
    REST API endpoints for asynchronous task artifacts.

    Artifact data can only be viewed or listed, not modified in any way via
    this API.
    """

    filter_backends = settings.USER_TASKS_ARTIFACT_FILTERS
    permission_classes = (DjangoObjectPermissionsIncludingView,)
    queryset = UserTaskArtifact.objects.all()
    serializer_class = ArtifactSerializer
