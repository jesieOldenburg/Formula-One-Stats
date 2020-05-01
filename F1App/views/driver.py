import requests
import pprint
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from F1App.models import Driver

pp = pprint.PrettyPrinter()

class DriverSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Driver
        url = serializers.HyperlinkedIdentityField(
            view_name='driver',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name', 'team', 'teammate', 'season_points', 'championships', 'wins')

def getDriverResults(query):
    result_data = requests.get(query).json()
    raceRounds = result_data["MRData"]["RaceTable"]["Races"]
    for race in raceRounds:
        print(race["round"])


def initial_driver_retrieval():
    data = requests.get('https://ergast.com/api/f1/2019/drivers.json')
    parsedData = data.json()
    driverList = parsedData["MRData"]["DriverTable"]["Drivers"]
    for driver in driverList:
        # print(driver["driverId"])
        driverId = driver["driverId"]
        queryString = f'https://ergast.com/api/f1/2018/drivers/{driverId}/results.json'
        getDriverResults(queryString)
        # print(driver["givenName"] + ' ' + driver["familyName"])

class Drivers(ViewSet):

    # def initial_driver_retrieval(self, request):
    #     data = requests.get('https://ergast.com/api/f1/2019/drivers.json')
    #     parsedData = data.json()
    #     return print(parsedData)
    
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Driver instance
        """
        newdriver = Driver()
        newdriver.name = request.data["name"]
        newdriver.team = request.data["team"]
        newdriver.teammate = request.data["teammate"]
        newdriver.season_points = request.data["season_points"]
        newdriver.championships = request.data["championships"]
        newdriver.wins = request.data["wins"]
        newdriver.save()

        serializer = DriverSerializer(newdriver, context={'request': request})

        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handle PUT requests for a single team

        Returns:
            Response -- Empty body with 204 status code
        """
        driver = Driver.objects.get(pk=pk)
        driver.name = request.data["name"]
        driver.team = request.data["team"]
        driver.teammate = request.data["teammate"]
        driver.season_points = request.data["season_points"]
        driver.championships = request.data["championships"]
        driver.wins = request.data["wins"]
        driver.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single team

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            driver = Driver.objects.get(pk=pk)
            driver.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Driver.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        initial_driver_retrieval()
        drivers = Driver.objects.all()
        serializer = DriverSerializer(
            drivers,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)