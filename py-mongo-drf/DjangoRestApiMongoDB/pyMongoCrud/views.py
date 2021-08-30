import json
from pyMongoCrud.models import Emp
from django.http.response import JsonResponse
from pyMongoCrud.serializers import EmpSerializer
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from utils import get_db_handle
from bson.json_util import dumps
from rest_framework.parsers import JSONParser 

# Create your views here.
@api_view(['GET', 'DELETE', 'PUT', 'POST'])
def getEmpById(request, pk):
   
    if request.method == 'GET':
        print('Get Employee By Id')
        try:  
            emp = Emp.objects.get(pk=pk)
            empSerializer = EmpSerializer(emp)
            return JsonResponse(empSerializer.data, status=status.HTTP_200_OK)
        except Emp.DoesNotExist:
            print("Employee Does not exist")
            return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'DELETE':
        try: 
            emp = Emp.objects.get(pk=pk)
            emp.delete()
            return JsonResponse({'message': 'Tutorial was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT) 
        except Emp.DoesNotExist:
            print("Employee Does not exist")
            return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'PUT':
        emp_serializer = ''
        try: 
            emp = Emp.objects.get(pk=pk)
            emp_data = JSONParser().parse(request)
            emp_serializer = EmpSerializer(emp, data=emp_data) 
            if emp_serializer.is_valid(): 
                emp_serializer.save() 
                return JsonResponse(emp_serializer.data) 
        except Emp.DoesNotExist:
            print("Employee Does not exist")
            return JsonResponse(emp_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'POST':
        emp_data = JSONParser().parse(request)
        emp_serializer = EmpSerializer(data=emp_data)
        if emp_serializer.is_valid():
            emp_serializer.save()
            return JsonResponse(emp_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(emp_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        


@api_view(['POST'])
def createNewEmployee(request):
    if request.method == 'POST':
        db_handle, mongo_client = get_db_handle('boot_mongodb', 'localhost', '27017', 'mongouser', 'password')
        print("Create a new employee")    
        #pyMongoCrud_emp = db_handle.pyMongoCrud_emp
        #pyMongoCrud_emp.insert(request.data)
        #print(Emp.objects.all())
        emp = Emp.objects.create(
        id=request.data['id'],
        name=request.data['name'],
        designation=request.data['designation'] 
        )
        
    return Response(status=status.HTTP_201_CREATED)
# Create your views here.
@api_view(['GET', 'POST'])
def getAllEmps(request):
    
    print('GET API Invoked')
    # GET all employees
    if request.method == 'GET':
        employees = Emp.objects.all()
        
        emp_serializer = EmpSerializer(employees, many=True)
        return JsonResponse(emp_serializer.data, safe=False)
    
    if request.method == 'POST':
        customHeader = request.headers['x-custom-header']
        emp_serializer = EmpSerializer(data=request.data)
        
        if emp_serializer.is_valid():
            emp_serializer.save()
            response = Response(emp_serializer.data, status=status.HTTP_201_CREATED)
            response.headers['Content-Type'] = 'application/json'
            response.headers['X-CUSTOM-HEADER'] = customHeader
            return response
        return Response(emp_serializer.errors, status=status.HTTP_400_BAD_REQUEST)