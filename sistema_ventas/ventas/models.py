from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return str(self.nombre)

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return str(self.nombre)
    
class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return str(self.nombre) 
    
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    descripcion = models.TextField()
    etiquetas = models.ManyToManyField(Etiqueta)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField()

    def __str__(self):
        return str(self.nombre)
    
class DetalleProducto(models.Model):
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE)
    especificaciones = models.TextField()
    fecha_vencimiento = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Detalles de {self.producto.nombre}"

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)    
    email = models.EmailField(max_length=50, unique=True)
    direccion = models.CharField(max_length=100)

    def __str__(self):
        return str(self.nombre)

class Venta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_venta = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField()

    def __str__(self):
        return f"Venta de {self.cantidad} x {self.producto.nombre} a {self.cliente.nombre} el {self.fecha_venta} por {self.total}"