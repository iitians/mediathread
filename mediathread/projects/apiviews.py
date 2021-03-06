from django.shortcuts import get_object_or_404
from rest_framework import permissions, mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from mediathread.projects.models import ProjectSequenceAsset, Project
from mediathread.projects.serializers import ProjectSequenceAssetSerializer


class ProjectSequenceAssetViewSet(mixins.ListModelMixin, GenericViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = ProjectSequenceAsset.objects.all()
    serializer_class = ProjectSequenceAssetSerializer

    def filter_by_project(self, viewer, project_id):
        # request psa for a readable project
        project = get_object_or_404(Project, id=project_id)
        if project.can_read(project.course, viewer):
            return ProjectSequenceAsset.objects.filter(project=project)
        else:
            return ProjectSequenceAsset.objects.none()

    def filter_by_user(self, viewer):
        return ProjectSequenceAsset.objects.filter(
            sequence_asset__author=viewer)

    def list(self, request):
        project_id = request.query_params.get('project', None)
        if project_id is not None:
            queryset = self.filter_by_project(request.user, project_id)
        elif request.user.is_authenticated():
            queryset = self.filter_by_user(request.user)
        else:
            queryset = ProjectSequenceAsset.objects.none()

        serializer = ProjectSequenceAssetSerializer(queryset, many=True)
        return Response(serializer.data)
