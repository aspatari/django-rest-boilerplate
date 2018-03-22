import graphene
from apps.users.schema import Query as UserQuery
from apps.bookmarks.schema import Query as BookmarksQuery


class Query(UserQuery, BookmarksQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
