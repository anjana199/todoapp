from urllib import request
from django.shortcuts import render

from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from api.models import ToDosn
from api.serializer import RegistrationSerializer, TodoSerializer
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework import authentication,permissions


class TodosView(ViewSet):
    def list(self,request,*args,**kw):
        qs=ToDosn.objects.all()
        serializer=TodoSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kw):
        id=kw.get("pk")
        qs=ToDosn.objects.get(id=id)
        serializer=TodoSerializer(qs,many=False)
        return Response(data=serializer.data)

    def destroy(self,request,*args,**kw):
        id=kw.get("pk")
        ToDosn.objects.get(id=id).delete()
        return Response(data="deleted")
        
    def update(self,request,*args,**kw):
        id=kw.get("pk")
        object=ToDosn.objects.get(id=id)
        serializer=TodoSerializer(data=request.data,instance=object)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)            




class TodosModelViews(ModelViewSet):

    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    serializer_class=TodoSerializer
    queryset=ToDosn.objects.all()

    def create(self,request,*args,**kw):
        serializer=TodoSerializer(data=request.data,context={"User":request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)





    # def perform_create(self, serializer):
    #     serializer.save(User=self.request.user)

    # def create(self,request,*args,**kw):
    #     serializer=TodoSerializer(data=request.data)
    #     if serializer.is_valid():
    #         ToDosn.objects.create(**serializer.validated_data,User=request.user)
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)    

    def  get_queryset(self):
        return ToDosn.objects.filter(User=self.request.user)

    # def list(self,request,*args,**kw):
    #     qs=ToDosn.objects.filter(User=request.user)        
    #     serializer=TodoSerializer(qs,many=True)
    #     return Response(data=serializer.data)

    




    @action(methods=['GET'],detail=False)
    def pending_todos(self,*args,**kw):
        qs=ToDosn.objects.filter(Status=False,User=self.request.user)
        serializer=TodoSerializer(qs,many=True)
        return Response(data=serializer.data)

    @action(methods=['GET'],detail=False)
    def completed_todos(self,*args,**kw):
        qs=ToDosn.objects.filter(Status=True,User=self.request.user)
        serializer=TodoSerializer(qs,many=True)
        return Response(data=serializer.data)  

    @action(methods=['POST'],detail=True)
    def mark_as_done(self,*args,**kw):
        id=kw.get("pk")
        object=ToDosn.objects.get(id=id)
        # ToDosn.objects.filter(id=id).update(Status=True)
        object.Status=True
        object.save()
        serializer=TodoSerializer(object,many=False)
        return Response(data=serializer.data)

# REGISTARING A USER FOR AUTHENICATION


class UserView(ModelViewSet):
    serializer_class=RegistrationSerializer
    queryset=User.objects.all()


    # def create(self,request,*args,**kw):
    #     serializer=RegistrationSerializer(data=request.data)
    #     if serializer.is_valid():
    #         user=User.objects.create_user(**serializer.validated_data)
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)
            
                



        
