from django import forms
from .models import Producto, Categoria, DetalleProducto, Proveedor, Cliente, Venta

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'categoria', 'descripcion', 'etiquetas', 'precio', 'cantidad']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
            'especificaciones_tecnicas': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'fecha_lanzamiento': forms.DateInput(attrs={'type': 'date'}),
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre:
            raise forms.ValidationError('El nombre no puede quedar vacio.')
        if len(nombre) <= 3:
            raise forms.ValidationError('el nombre debe tener al menos 3 caracteres.')
        return nombre

class DetalleProductoForm(forms.ModelForm):
    class Meta:
        model = DetalleProducto
        fields = ['especificaciones', 'fecha_vencimiento']
        
class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'telefono']

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono.isdigit():
            raise forms.ValidationError('el numero de telefono debe contener solo digitos.')
        return telefono
    
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'telefono', 'email', 'direccion']

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['producto', 'cliente', 'fecha_venta', 'total','cantidad']
        widgets = {
            'fecha_venta': forms.DateInput(attrs={'type': 'date'}),
        }