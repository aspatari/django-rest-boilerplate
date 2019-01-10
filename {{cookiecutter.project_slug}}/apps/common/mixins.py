from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response


class CreateOrUpdateMixin(object):
    def create_or_update(self, request, *args, **kwargs):

        pk = self.request.data.get("id", None)

        if pk:
            partial = True
            instance = get_object_or_404(self.get_queryset(), pk=pk)
            serializer = self.get_serializer(instance, data=self.request.data, partial=partial)
            response_status = status.HTTP_200_OK
        else:
            serializer = self.get_serializer(data=self.request.data)
            response_status = status.HTTP_201_CREATED

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=response_status)
