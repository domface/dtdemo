from rest_framework import viewsets, generics, mixins
from data_theorem_demo.serializers import *

class CreateQueryView(generics.CreateAPIView):

    serializer_class = LookUpSerializer