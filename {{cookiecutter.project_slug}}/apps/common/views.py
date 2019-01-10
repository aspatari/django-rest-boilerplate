from rest_framework.viewsets import ModelViewSet


class CustomSerializerViewSetMixin:
    custom_serializer_classes = {}

    def get_serializer_class(self):
        """ Return the class to use for serializer w.r.t to the request method."""
        try:
            return self.custom_serializer_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()


class CustomPermissionsViewSetMixin:
    custom_permission_classes = {}

    def get_permissions(self):
        """ Return the class to use for serializer w.r.t to the request method."""
        try:
            return [permission() for permission in self.custom_permission_classes[self.action]]
        except (KeyError, AttributeError):
            return super().get_permissions()


class CustomViewSetMixin(CustomPermissionsViewSetMixin, CustomSerializerViewSetMixin):
    pass
