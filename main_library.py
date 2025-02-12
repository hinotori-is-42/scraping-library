from time import sleep
from lib.creatorAlpha import CreatorAlpha
import sys

def main() :
    creator = CreatorAlpha()
    df = creator.getBookList()
    print(df)


if __name__ == "__main__":
    main()
