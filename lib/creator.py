from abc import ABC, abstractmethod
from .product import Product
from typing import List
import pandas as pd

class Creator(ABC):
    @abstractmethod
    def createProduct( self ) -> Product:
        pass

    def getBookList( self ) :
        product = self.createProduct()
        product.getBookPaths()
        cols = ('YYYY/MM','title','author','library','pages','NDC','ISBN','content','titleCode','registration',)
        df = pd.DataFrame(columns=cols).set_index("ISBN")
        bookIDs = product.getBooksSet()
        booksNum = str(len(bookIDs))
        for num , id in enumerate(bookIDs) :
            if (book:=product.getBookInfo(id)) is not None :
                df.loc[book["ISBN"]] = book
                print( str(num+1) + "/" + booksNum , book["title"] )
        return df
