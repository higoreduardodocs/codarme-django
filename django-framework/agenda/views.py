from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.views import APIView

from rest_framework import mixins, generics

from agenda.models import Agendamento, AgendamentoCustom
from agenda.serializers import AgendamentoSerializer, AgendamentoSerializerCreateUpdate, AgendamentoSerializerModelSerialiazer, AgendamentoSerializerModelSerialiazerCustom


# Primeiro método
def agendamento_list(request):
  qs = Agendamento.objects.all()
  serializer = AgendamentoSerializer(qs, many=True)
  data = serializer.data
  return JsonResponse(data, safe=False)

def agendamento_detail(request, id):
  obj = get_object_or_404(Agendamento, id=id)
  serializer = AgendamentoSerializer(obj)
  data = serializer.data
  return JsonResponse(data)

# Segundo método
@api_view(http_method_names=["GET", "POST"])
def agendamento_list_api_view(request):
  if request.method == "GET":
    qs = Agendamento.objects.all()
    serializer = AgendamentoSerializer(qs, many=True)
    data = serializer.data
    return JsonResponse(data, safe=False)
  
  if request.method == "POST":
    data = request.data
    serializer = AgendamentoSerializer(data=data)
    if serializer.is_valid():
      validated_data = serializer.validated_data
      Agendamento.objects.create(
        data_agendamento=validated_data["data_agendamento"],
        nome_cliente=validated_data["nome_cliente"],
        email_cliente=validated_data["email_cliente"],
        telefone_cliente=validated_data["telefone_cliente"]
      )
      return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)

@api_view(http_method_names=["GET", "PUT", "PATCH", "DELETE"])
def agendamento_detail_api_view(request, id):
  if request.method == "GET":
    obj = get_object_or_404(Agendamento, id=id)
    serializer = AgendamentoSerializer(obj)
    data = serializer.data
    return JsonResponse(data)
  
  if request.method == "PUT":
    obj = get_object_or_404(Agendamento, id=id)
    data = request.data
    serializer = AgendamentoSerializer(data=data)
    if serializer.is_valid():
      validated_data = serializer.validated_data
      obj.data_agendamento = validated_data.get("data_agendamento", obj.data_agendamento)
      obj.nome_cliente = validated_data.get("nome_cliente", obj.nome_cliente)
      obj.email_cliente = validated_data.get("email_cliente", obj.email_cliente)
      obj.telefone_cliente = validated_data.get("telefone_cliente", obj.telefone_cliente)
      obj.save()
      return JsonResponse(serializer.data, status=200)
    return JsonResponse(serializer.errors, status=400)
    
  if request.method == "PATCH":
    obj = get_object_or_404(Agendamento, id=id)
    data = request.data
    serializer = AgendamentoSerializer(data=data, partial=True)
    if serializer.is_valid():
      validated_data = serializer.validated_data
      obj.data_agendamento = validated_data.get("data_agendamento", obj.data_agendamento)
      obj.nome_cliente = validated_data.get("nome_cliente", obj.nome_cliente)
      obj.email_cliente = validated_data.get("email_cliente", obj.email_cliente)
      obj.telefone_cliente = validated_data.get("telefone_cliente", obj.telefone_cliente)
      obj.save()
      return JsonResponse(validated_data, status=200)
    return JsonResponse(serializer.errors, status=400)
  
  if request.method == "DELETE":
    obj = get_object_or_404(Agendamento, id=id)
    obj.delete()
    return Response(status=204)
  
# Terceiro método (Create Update)
@api_view(http_method_names=["GET", "POST"])
def agendamento_list_api_view_create_update(request):
  if request.method == "GET":
    qs = Agendamento.objects.all()
    serializer = AgendamentoSerializerCreateUpdate(qs, many=True)
    data = serializer.data
    return JsonResponse(data, safe=False)

  if request.method == "POST":
    data = request.data
    serializer = AgendamentoSerializerCreateUpdate(data=data)
    if serializer.is_valid():
      serializer.save()
      return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)
  
@api_view(http_method_names=["GET", "PUT", "PATCH", "DELETE"])
def agendamento_detail_api_view_create_update(request, id):
  if request.method == "GET":
    obj = get_object_or_404(Agendamento, id=id)
    serializer = AgendamentoSerializerCreateUpdate(obj)
    data = serializer.data
    return JsonResponse(data)
  
  if request.method == "PUT":
    obj = get_object_or_404(Agendamento, id=id)
    data = request.data
    serializer = AgendamentoSerializerCreateUpdate(obj, data=data)
    if serializer.is_valid():
      serializer.save()
      return JsonResponse(serializer.data, status=200)
    return JsonResponse(serializer.errors, status=400)
  
  if request.method == "PATCH":
    obj = get_object_or_404(Agendamento, id=id)
    data = request.data
    serializer = AgendamentoSerializerCreateUpdate(obj, data=data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return JsonResponse(serializer.data, status=200)
    return JsonResponse(serializer.errors, status=400)
  
  if request.method == "DELETE":
    obj = get_object_or_404(Agendamento, id=id)
    obj.delete()
    return Response(status=204)
  
# Quarto método (Model Serializer)
@api_view(http_method_names=["GET", "POST"])
def agendamento_list_api_view_model_serializer(request):
  if request.method == "GET":
    qs = Agendamento.objects.all()
    serializer = AgendamentoSerializerModelSerialiazer(qs, many=True)
    data = serializer.data
    return JsonResponse(data, safe=False)

  if request.method == "POST":
    data = request.data
    serializer = AgendamentoSerializerModelSerialiazer(data=data)
    if serializer.is_valid():
      serializer.save()
      return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)
  
@api_view(http_method_names=["GET", "PUT", "PATCH", "DELETE"])
def agendamento_detail_api_view_model_serializer(request, id):
  if request.method == "GET":
    obj = get_object_or_404(Agendamento, id=id)
    serializer = AgendamentoSerializerModelSerialiazer(obj)
    data = serializer.data
    return JsonResponse(data)
  
  if request.method == "PUT":
    obj = get_object_or_404(Agendamento, id=id)
    data = request.data
    serializer = AgendamentoSerializerModelSerialiazer(obj, data=data)
    if serializer.is_valid():
      serializer.save()
      return JsonResponse(serializer.data, status=200)
    return JsonResponse(serializer.errors, status=400)
  
  if request.method == "PATCH":
    obj = get_object_or_404(Agendamento, id=id)
    data = request.data
    serializer = AgendamentoSerializerModelSerialiazer(obj, data=data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return JsonResponse(serializer.data, status=200)
    return JsonResponse(serializer.errors, status=400)
  
  if request.method == "DELETE":
    obj = get_object_or_404(Agendamento, id=id)
    obj.delete()
    return Response(status=204)
  
# Quinto método (Model Serializer)
class AgendamentoListClassBasedView(APIView):
  def get(self, request):
    qs = Agendamento.objects.all()
    serializer = AgendamentoSerializerModelSerialiazer(qs, many=True)
    data = serializer.data
    return JsonResponse(data, safe=False)
  
  def post(self, request):
    data = request.data
    serializer = AgendamentoSerializerModelSerialiazer(data=data)
    if serializer.is_valid():
      serializer.save()
      return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)
  
class AgendamentoDetailClassBasedView(APIView):
  def get(self, request, id):
    obj = get_object_or_404(Agendamento, id=id)
    serializer = AgendamentoSerializerModelSerialiazer(obj)
    data = serializer.data
    return JsonResponse(data)
  
  def put(self, request, id):
    obj = get_object_or_404(Agendamento, id=id)
    data = request.data
    serializer = AgendamentoSerializerModelSerialiazer(obj, data=data)
    if serializer.is_valid():
      serializer.save()
      return JsonResponse(serializer.data, status=200)
    return JsonResponse(serializer.errors, status=400)
  
  def patch(self, request, id):
    obj = get_object_or_404(Agendamento, id=id)
    data = request.data
    serializer = AgendamentoSerializerModelSerialiazer(obj, data=data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return JsonResponse(serializer.data, status=200)
    return JsonResponse(serializer.errors, status=400)
  
  def delete(self, request, id):
    obj = get_object_or_404(Agendamento, id=id)
    obj.delete()
    return Response(status=204)
  
# Sexto método (Model Serializer)
class AgendamentoListMixins(
  mixins.ListModelMixin, # method list
  mixins.CreateModelMixin, # method create
  generics.GenericAPIView,
):
  queryset = Agendamento.objects.all()
  serializer_class = AgendamentoSerializerModelSerialiazer

  def get(self, request, *args, **kwargs):
    return self.list(request, *args, **kwargs)
  
  def post(self, request, *args, **kwargs):
    return self.create(request, *args, **kwargs)
  
class AgendamentoDetailMixins(
  mixins.RetrieveModelMixin, # method get
  mixins.UpdateModelMixin, # method update
  mixins.DestroyModelMixin, # method delete
  generics.GenericAPIView,
):
  queryset = Agendamento.objects.all()
  serializer_class = AgendamentoSerializerModelSerialiazer
  lookup_field = 'id'

  def get(self, request, *args, **kwargs):
    return self.retrieve(request, *args, **kwargs)
  
  def put(self, request, *args, **kwargs):
    return self.update(request, *args, **kwargs)
  
  def patch(self, request, *args, **kwargs):
    return self.partial_update(request, *args, **kwargs)
  
  def delete(self, request, *args, **kwargs):
    return self.destroy(request, *args, **kwargs)
  
# Sétimo método (Model Serializer)
class AgendamentoListGenericView(generics.ListCreateAPIView):
  queryset = Agendamento.objects.all()
  serializer_class = AgendamentoSerializerModelSerialiazer

class AgendamentoDetailGenericView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Agendamento.objects.all()
  serializer_class = AgendamentoSerializerModelSerialiazer
  lookup_field = 'id'

# Oitavo método (Model Serializer)
class AgendamentoListGenericCustom(generics.ListCreateAPIView):
  serializer_class = AgendamentoSerializerModelSerialiazerCustom

  def get_queryset(self):
    username = self.request.query_params.get("username", None)
    queryset = AgendamentoCustom.objects.filter(prestador__username=username)
    return queryset