from .creator import Creator
from .product import Product
from .productAlpha import ProductAlpha

class CreatorAlpha(Creator):
    def createProduct( self ) -> Product:
        return ProductAlpha()
