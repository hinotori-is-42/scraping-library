from abc import ABC , abstractmethod
from typing import List
import pandas as pd

class Product(ABC):
    @abstractmethod
    def getBookPaths() -> List[str] :
        pass
    @abstractmethod
    def getBookInfo() -> pd.Series :
        pass
    def getLibraryInfo( self , index ) :
        ndc = pd.read_csv( "./tmp_ignore/NDC.csv" , dtype=str )["NDC"]
        row = pd.read_csv( "./tmp_ignore/libraryInfo.csv" , dtype=str ).iloc[index]
        return ndc , row["library"] , row["searchPath"] , row["bookInfoPath"]
