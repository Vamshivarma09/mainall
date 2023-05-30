from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .forms import *
from .serializers import *
from django.http import JsonResponse
from django.shortcuts import render
import json
from .models import *
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
# class EmployeeUpdateAPIView(APIView):
def EmployeeUpdateAPIPostView(request):
    try:
        if request.method == 'POST':
            try:
                body = request.body
                bodyObj = json.loads(body)
                id = bodyObj['id']
                fName = bodyObj['fName']
                lName = bodyObj['lName']
                email = bodyObj['email']
                desig = bodyObj['desig']
                add = bodyObj['add']

                userUpdate = Employee(id = id,first_name = fName, last_name = lName,email = email,designation = desig, address= add)
                userUpdate.save()
                return JsonResponse({"status":"success"})
            except Exception as ex:
                return JsonResponse({"status":"failed"})
    except Exception as ex:
        return ex

def PayStubCreateAPIView(request):
    try:
        if request.method == "POST":
            try:     
                bdy = request.body
                bdyObj = json.loads(bdy)
                id = bdyObj['id']
                emp = bdyObj['emp']
                stdate = bdyObj['stdate']
                enddate = bdyObj['enddate']
                grossearning = bdyObj['grossearning']
                ot = bdyObj['ot']

                pretax = bdyObj['pretax']
                ot = bdyObj['ot']
                fdincome = bdyObj['fdincome']
                stincome = bdyObj['stincome']
                posttax = bdyObj['posttax']
                emplrcontrbtn = bdyObj['emplrcontrbtn']
                netpay = bdyObj['netpay']
                usr = Paystub1(id = id, employee=emp, pay_period_start=stdate, pay_period_end=enddate, gross_earnings=grossearning, overtime_earnings=ot, pre_tax_deductions=pretax, federal_income_tax=fdincome, state_income_tax=stincome,post_tax_deductions=posttax,employer_contribution=emplrcontrbtn,net_pay=netpay)
                usr.save()
                return JsonResponse({"status":"success"})
            except Exception as ex:
                return JsonResponse({"status":"failed"})
             
    except Exception as ex: 
        print(ex)
    

@api_view(['POST'])
def create_time_off_request(request):
    serializer = create_time_off_request(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': 'Time off request created'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def policy_list_create(request):
    if request.method == 'GET':
        policies = Policy.objects.all()
        serializer = PolicySerializer(policies, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PolicySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def policy_retrieve_update_destroy(request, pk):
    try:
        policy = Policy.objects.get(pk=pk)
    except Policy.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = PolicySerializer(policy)
        return Response(serializer.data)
    elif request.method in ['PUT', 'PATCH']:
        serializer = PolicySerializer(policy, data=request.data, partial=request.method == 'PATCH')
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        policy.delete()
        return Response(status=204)