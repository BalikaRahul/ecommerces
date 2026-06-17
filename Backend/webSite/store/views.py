from django.shortcuts import render,get_object_or_404
from .models import Product
from category.models import Category
from carts.views import CartItem,_cart_id
from django.core.paginator import Paginator

# Create your views here.
def store (request,category_slug=None):
    categoies =None
    products = None
    if category_slug !=None:
        categoies=get_object_or_404(Category,slug=category_slug)
        products=Product.objects.filter(category = categoies,is_avaliable=True)
    else:
        products = Product.objects.all().filter(is_avaliable=True)

    product_count = products.count()
    # paginate 9 items per page
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context ={
        'products': page_obj.object_list,
        'product_count': product_count,
        'page_obj': page_obj,
    }
    return render(request,'store/store.html',context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id= _cart_id(request),product=single_product).exists()

    except Exception as e:
        raise e
    context = {
        'single_product': single_product,
        'in_cart':in_cart,

    }
    return render(request, 'store/product_detail.html', context)