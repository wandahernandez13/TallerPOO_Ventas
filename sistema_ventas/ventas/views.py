from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Cliente, Venta, DetalleProducto, Categoria, Proveedor
from .forms import ProductoForm, ClienteForm, VentaForm, CategoriaForm, ProveedorForm, DetalleProductoForm

#INICIO
def inicio(request):
    total_productos = Producto.objects.count()
    total_clientes = Cliente.objects.count()
    total_ventas = Venta.objects.count()
    ventas_recientes = Venta.objects.order_by('-fecha_venta')[:5]  # Mostrar últimas 5 ventas

    context = {
        'total_productos': total_productos,
        'total_clientes': total_clientes,
        'total_ventas': total_ventas,
        'ventas_recientes': ventas_recientes,
    }

    return render(request, 'ventas/inicio.html', context)

#PRODUCTOS
def listar_productos(request):
    productos = Producto.objects.prefetch_related('detalleproducto').all()

    return render(request, 'ventas/listar_productos.html', {'productos': productos})

def agregar_producto(request):
    if request.method == 'POST':
        producto_form = ProductoForm(request.POST)
        detalle_form = DetalleProductoForm(request.POST)
        if producto_form.is_valid() and detalle_form.is_valid():
            producto = producto_form.save(commit=False)
            producto.save()
            producto_form.save_m2m()

            detalle = detalle_form.save(commit=False)
            detalle.producto = producto
            detalle.save

            return redirect('listar_productos')

    else:
        producto_form = ProductoForm()
        detalle_form = DetalleProductoForm()

    return render(request, 'ventas/agregar_producto.html', {
         'producto_form': producto_form,
         'detalle_form': detalle_form
     })
      
def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'ventas/detalle_producto.html', {'producto': producto})


def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    try:
        detalle = producto.detalleproducto
    except DetalleProducto.DoesNotExist:
        detalle = None

    if request.method == 'POST':
        producto_form = ProductoForm(request.POST, instance=producto)
        detalle_form = DetalleProductoForm(request.POST, instance=detalle)
        if producto_form.is_valid() and detalle_form.is_valid():
            producto = producto_form.save(commit=False)
            producto_form.save()
            producto_form.save_m2m() # guardar relaciones muchos a muchos.
            detalle = detalle_form.save(commit=False)
            detalle.producto = producto
            detalle.save()
            return redirect('listar_productos')

def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('lista_productos')
    return render(request, 'ventas/eliminar_producto.html', {'producto': producto})

#CATEGORIA
def listar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'ventas/listar_categorias.html', {'categorias': categorias})

def agregar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'ventas/agregar_categoria.html', {'form': form})

def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('listar_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'ventas/editar_categoria.html', {'form': form})

def eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        return redirect('listar_categorias')
    return render(request, 'ventas/eliminar_categoria.html', {'categoria': categoria})

#PROVEEDORES
def listar_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'ventas/listar_proveedores.html', {'proveedores': proveedores})

def crear_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_proveedores')
    else:
        form = ProveedorForm()
    return render(request, 'ventas/crear_proveedor.html', {'form': form})

def editar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('listar_proveedores')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'ventas/editar_proveedor.html', {'form': form})

def eliminar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        proveedor.delete()
        return redirect('listar_proveedores')
    return render(request, 'ventas/eliminar_proveedor.html', {'proveedor': proveedor})

#CLIENTES
def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'ventas/listar_clientes.html', {'clientes': clientes})

def agregar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClienteForm()
    return render(request, 'ventas/crear_cliente.html', {'form': form})

def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'ventas/editar_cliente.html', {'form': form})

def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('listar_clientes')
    return render(request, 'ventas/eliminar_cliente.html', {'cliente': cliente})

#VENTAS
def listar_ventas(request):
    ventas = Venta.objects.all().select_related('producto', 'cliente')
    return render(request, 'ventas/listar_ventas.html', {'ventas': ventas})

def registrar_venta(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)
            producto = venta.producto

            # Verificar si hay suficiente stock (cantidad) antes de registrar la venta
            if producto.cantidad >= venta.cantidad:
                # Calcular el total de la venta
                venta.total = producto.precio * venta.cantidad

                # Reducir la cantidad (stock) del producto
                producto.cantidad -= venta.cantidad
                producto.save()

                venta.save()  # Guardar la venta con el total calculado
                return redirect('listar_ventas')
            else:
                form.add_error('cantidad', 'No hay suficiente stock para realizar esta venta.')
    else:
        form = VentaForm()

    return render(request, 'ventas/registrar_venta.html', {'form': form})

def editar_venta(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        form = VentaForm(request.POST, instance=venta)
        if form.is_valid():
            form.save()
            return redirect('listar_ventas')
    else:
        form = VentaForm(instance=venta)
    return render(request, 'ventas/editar_venta.html', {'form': form})

def eliminar_venta(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        venta.delete()
        return redirect('lista_ventas')
    return render(request, 'ventas/eliminar_venta.html', {'venta': venta})
