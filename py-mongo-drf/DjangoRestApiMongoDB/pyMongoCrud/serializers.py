from rest_framework import serializers 
from pyMongoCrud.models import Emp


class EmpSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Emp
        fields = ('id',
                  'name',
                  'designation')
