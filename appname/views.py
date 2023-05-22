from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from rest_framework import generics
from .models import Producto, Maturity_levels, Subdimension, Elementos, Preguntas, Respuesta, Cliente
from .serializers import ProductoSerializer
from django.views.generic import View
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.decorators import api_view


class ProductoList(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response["Access-Control-Allow-Origin"] = "*"
        return response

class ProductoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer


class TotalesView(APIView):
    def get(self, request, ciudad, format=None):
        sum1 = Maturity_levels.sum_subdimension_c(ciudad)
        sum2 = Maturity_levels.sum_subdimension_i(ciudad)
        sum3 = Maturity_levels.sum_subdimension_l(ciudad)
        sum4 = Maturity_levels.sum_subdimension_p(ciudad)
        sum5 = Maturity_levels.sum_subdimension_u(ciudad)
        return Response({
            'sum1': sum1,
            'sum2': sum2,
            'sum3': sum3,
            'sum4': sum4,
            'sum5': sum5,
        }, status=status.HTTP_200_OK)


class SubdimensionesView(APIView):
 def get(self, request, dimension, format=None):
        subdimensiones = Subdimension.objects.filter(dimension=dimension).values('subdimension')
        return Response(list(subdimensiones), status=status.HTTP_200_OK)

class SumaSubAPIView(APIView):
    def get(self, request, constante, ciudad, format=None):
        suma_valor = Maturity_levels.objects.filter(subdimension=constante, ciudad=ciudad).values('nombreLevel', 'maxPregunta', 'valor')
        return Response(list(suma_valor), status=status.HTTP_200_OK)

class PreguntaAPIView(APIView):
    def get(self, request, subdimension, format=None):
        preguntas = Preguntas.objects.filter(subdimension=subdimension).values()
        return Response(list(preguntas), status=status.HTTP_200_OK)

class ElementoAPIView(APIView):
    def get(self, request, id_pregunta, format=None):
        elementos = Elementos.objects.filter(id_pregunta=id_pregunta).values()
        return Response(list(elementos), status=status.HTTP_200_OK)

class TotalCiudadAPIView(APIView):
    def get(self, request):
        total_values_by_city = Maturity_levels.objects.values('ciudad').annotate(total_value=Sum('valor'))

        percent_complete_by_city = [
            {
                'ciudad': city['ciudad'],
                'percent_complete': round((city['total_value'] / 122) * 100, 2)
            } for city in total_values_by_city
        ]

        return Response(percent_complete_by_city)

class ActualizarMaturityLevels(APIView):
    def update_maturity_levels(self):
        # Obtener todas las respuestas
        respuestas = Respuesta.objects.all()

        # Iterar por cada respuesta
        for respuesta in respuestas:
            # Obtener la pregunta asociada a la respuesta
            pregunta = Preguntas.objects.get(id_pregunta=respuesta.id_pregunta_id)

            # Obtener la ciudad asociada a la respuesta
            ciudad = respuesta.ciudad

            # Obtener el maturity level asociado a la subdimension de la pregunta y la ciudad de la respuesta
            maturity_levels = Maturity_levels.objects.filter(subdimension_id=pregunta.subdimension, ciudad=ciudad)

            # Actualizar el valor del maturity level con el valor de la respuesta
            for maturity_level in maturity_levels:
                if maturity_level.valor:
                    maturity_level.valor = int(maturity_level.valor) + respuesta.respuesta
                else:
                    maturity_level.valor = respuesta.respuesta

                # Guardar el maturity level actualizado
                maturity_level.save()

        return Response({'message': 'Los maturity levels han sido actualizados exitosamente.'})

    def get(self, request):
        self.update_maturity_levels()
        return Response({'message': 'Los maturity levels han sido actualizados exitosamente.'})

@method_decorator(csrf_exempt, name='dispatch')
class CrearRespuestaViewSet(viewsets.ViewSet):
    @csrf_exempt
    @action(detail=False, methods=['post'])
    def create_respuesta(self, request):
        email = request.data.get('email')
        id_pregunta = request.data.get('id_pregunta', 0)
        ciudad = request.data.get('ciudad')
        año = request.data.get('año')
        respuesta = request.data.get('respuesta')

        try:
            cliente = Cliente.objects.get(email=email)
            pregunta = Preguntas.objects.get(id_pregunta=id_pregunta)

            nueva_respuesta = Respuesta(
                email=cliente,
                id_pregunta=pregunta,
                ciudad=ciudad,
                año=año,
                respuesta=respuesta
            )

            nueva_respuesta.save()

            return Response({'message': 'Respuesta creada correctamente'}, status=status.HTTP_201_CREATED)
        except Cliente.DoesNotExist:
            return Response({'message': 'Cliente no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Preguntas.DoesNotExist:
            return Response({'message': 'Pregunta no encontrada'}, status=status.HTTP_404_NOT_FOUND)