

from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    email = models.CharField(max_length=50, primary_key=True)
    rol_profesional = models.CharField(max_length=50)
    años_experiencia = models.IntegerField()
    principales_desafios = models.CharField(max_length=50)

    def __str__(self):
        return self.email

class Subdimension(models.Model):
    subdimension = models.CharField(max_length=2,primary_key=True)
    dimension = models.CharField(max_length=1)

    def __str__(self):
        return self.subdimension

class Preguntas(models.Model):
    id_pregunta = models.CharField(max_length=6,primary_key=True)
    pregunta = models.CharField(max_length=250)
    subdimension = models.ForeignKey(Subdimension, on_delete=models.CASCADE)
    tipo_pregunta = models.CharField(max_length=5)

    def __str__(self):
        return self.pregunta

class Elementos(models.Model):
    elementoId = models.AutoField(primary_key=True)
    elemento = models.CharField(max_length=50)
    id_pregunta = models.ForeignKey(Preguntas, on_delete=models.CASCADE)
    tipo_pregunta = models.CharField(max_length=5)
    valor = models.IntegerField()

    def __str__(self):
        return self.elemento

class PreguntaTabla(models.Model):
    pregunta_tabla_id = models.IntegerField(primary_key=True)
    id_pregunta = models.ForeignKey(Preguntas, on_delete=models.CASCADE)
    elemento_pregunta = models.CharField(max_length=50)
    valor = models.IntegerField()

    def __str__(self):
        return f"{self.id_pregunta} - {self.elemento_pregunta}"

class Respuesta(models.Model):
    id_respuesta = models.AutoField(primary_key=True)
    email = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    id_pregunta = models.ForeignKey(Preguntas, on_delete=models.CASCADE)
    ciudad = models.CharField(max_length=10)
    año = models.IntegerField()
    respuesta = models.IntegerField()

    def __str__(self):
        return f"{self.email} - {self.id_pregunta} - {self.respuesta}"

class Maturity_levels(models.Model):
    id = models.AutoField(primary_key=True)
    subdimension = models.ForeignKey(Subdimension, on_delete=models.CASCADE)
    nombreLevel  = models.CharField(max_length=10)
    maxPregunta = models.IntegerField()
    valor = models.CharField(max_length=10)
    ciudad = models.CharField(max_length=10)

    @classmethod
    def sum_subdimension_c(cls, ciudad):
     query = cls.objects.filter(subdimension__in=['C1', 'C2'], ciudad=ciudad)
     print(query.query)  # Imprime la query generada
     result = query.aggregate(models.Sum('valor')).get('valor__sum') or 0
     print(result)  # Imprime el resultado de la agregación
     return result

    @classmethod
    def sum_subdimension_i(cls, ciudad):
        return cls.objects.filter(subdimension__in=['I1', 'I2'], ciudad=ciudad).aggregate(models.Sum('valor')).get('valor__sum') or 0

    @classmethod
    def sum_subdimension_l(cls, ciudad):
        return cls.objects.filter(subdimension__in=['L1', 'L2', 'L3', 'L4'], ciudad=ciudad).aggregate(models.Sum('valor')).get('valor__sum') or 0

    @classmethod
    def sum_subdimension_p(cls, ciudad):
        return cls.objects.filter(subdimension__in=['P1', 'P2'], ciudad=ciudad).aggregate(models.Sum('valor')).get('valor__sum') or 0

    @classmethod
    def sum_subdimension_u(cls, ciudad):
        return cls.objects.filter(subdimension__in=['U1', 'U2'], ciudad=ciudad).aggregate(models.Sum('valor')).get('valor__sum') or 0
        
    def __str__(self):
        return f"{self.nombreLevel} - {self.subdimension}"

class Questions_Levels(models.Model):
  id= models.AutoField(primary_key=True)
  Level = models.CharField(max_length=255)
  Question = models.ForeignKey(Preguntas, on_delete=models.CASCADE)
