from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from F1App.models import Driver


class DriverSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Driver
        url = serializers.HyperlinkedIdentityField(
            view_name='driver',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name', 'team', 'teammate', 'season_points', 'championships', 'wins')


class Drivers(ViewSet):

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single Driver

        Returns:
            Response -- JSON serialized driver instance
        """
        try:
            driver = Driver.objects.get(pk=pk)
            serializer = DriverSerializer(driver, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
            
    def list(self, request):
        """Handle GET requests to drivers resource

        Returns:
            Response -- JSON serialized list of all drivers
        """
        drivers = Driver.objects.all()
        serializer = DriverSerializer(
            drivers,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)