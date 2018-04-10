from rest_framework import viewsets, generics, mixins
from dt_demo.serializers import *

class CreateQueryView(generics.CreateAPIView):

    serializer_class = LookUpSerializer