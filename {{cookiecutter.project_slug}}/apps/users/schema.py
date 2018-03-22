from graphene_django import DjangoObjectType
import graphene
from . import models

from django.contrib.auth import get_user_model


class User(DjangoObjectType):
    class Meta:
        model = get_user_model()


class Query(graphene.ObjectType):
    users = graphene.List(User)

    def resolve_users(self, info):
        return get_user_model().objects.all()


schema = graphene.Schema(query=Query)
