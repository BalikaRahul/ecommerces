from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from store.models import Product, Variation

# Helper to retrieve or create cart based on session key
def _cart_id(request):
    """Return the session key used as the cart identifier, creating a session if needed."""
    cart_id = request.session.session_key
    if not cart_id:
        request.session.create()
        cart_id = request.session.session_key
    return cart_id


def add_cart(request, product_id):
    """Add a product (with optional variations) to the cart.

    Handles POST data containing variation selections and updates quantity if the same
    product/variation combination already exists.
    """
    product = get_object_or_404(Product, id=product_id)
    product_variation = []

    if request.method == "POST":
        for key, value in request.POST.items():
            try:
                variation = Variation.objects.get(
                    variation_category__iexact=key,
                    variation_value__iexact=value,
                )
                product_variation.append(variation)
            except Variation.DoesNotExist:
                continue

    # Get or create the cart for the current session
    cart, _ = Cart.objects.get_or_create(cart_id=_cart_id(request))

    # Determine if a cart item with the same product & variation already exists
    existing_item = None
    for item in CartItem.objects.filter(product=product, cart=cart):
        if list(item.variations.all()) == product_variation:
            existing_item = item
            break

    if existing_item:
        existing_item.quantity += 1
        existing_item.save()
    else:
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
        if product_variation:
            cart_item.variations.add(*product_variation)

    return redirect('cart')


def remove_cart(request, product_id):
    """Decrease quantity of a cart item or remove it if quantity becomes zero."""
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


def remove_cart_item(request, product_id):
    """Remove all cart items for the given product regardless of quantity.

    Previously this used ``CartItem.objects.get`` which raised ``MultipleObjectsReturned``
    when more than one ``CartItem`` existed for the same product (e.g., duplicate
    entries created by earlier bugs). Using ``filter(...).delete()`` safely removes
    all matching rows.
    """
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    # Delete all matching items to avoid MultipleObjectsReturned
    CartItem.objects.filter(product=product, cart=cart).delete()
    return redirect('cart')


def cart(request):
    """Display the current cart with totals, tax, and grand total."""
    total = 0
    quantity = 0
    tax = 0
    grand_total = 0
    cart_items = []
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for item in cart_items:
            total += item.product.price * item.quantity
            quantity += item.quantity
        tax = total * 0.02  # 2% tax
        grand_total = total + tax
    except Cart.DoesNotExist:
        pass

    context = {
        "total": total,
        "quantity": quantity,
        "cart_items": cart_items,
        "tax": tax,
        "grand_total": grand_total,
    }
    return render(request, "store/cart.html", context)