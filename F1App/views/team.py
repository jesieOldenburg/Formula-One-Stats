from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from F1App.models import Team


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Team
        url = serializers.HyperlinkedIdentityField(
            view_name='team',
            lookup_field='id'
        )
        fields = ('id', 'url', 'team_name', 'team_points')


class Teams(ViewSet):
    
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized ParkArea instance
        """
        newteam = Team()
        newteam.team_name = request.data["team_name"]
        newteam.team_points = request.data["team_points"]
        newteam.save()

        serializer = TeamSerializer(newteam, context={'request': request})

        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handle PUT requests for a single team

        Returns:
            Response -- Empty body with 204 status code
        """
        team = Team.objects.get(pk=pk)
        team.team_name = request.data["team_name"]
        team.team_points = request.data["team_points"]
        team.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single team

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            team = Team.objects.get(pk=pk)
            team.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Team.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single Driver

        Returns:
            Response -- JSON serialized driver instance
        """
        try:
            team = Team.objects.get(pk=pk)
            serializer = TeamSerializer(team, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
            
    def list(self, request):
        """Handle GET requests to drivers resource

        Returns:
            Response -- JSON serialized list of all drivers
        """
        teams = Team.objects.all()
        serializer = TeamSerializer(
            teams,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)