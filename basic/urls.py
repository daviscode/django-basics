from django.urls import path
from graphene_django.views import GraphQLView
from basic.schema import schema

urlpatterns = [
    # ...
    path('graphql/', GraphQLView.as_view(graphiql=True, schema = schema)), # Given that schema path is defined in GRAPHENE['SCHEMA'] in your settings.py
]