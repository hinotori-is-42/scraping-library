from .product import Product
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time
import sys
import re
import datetime
from .browser import Browser


class ProductAlpha(Product):
    def __init__( self ):
        self.browser = Browser()
        self.bookIDs = set()
        self.bookCodes , self.library , self.searchPath , self.bookInfoPath = \
            self.getLibraryInfo( 0 )
        self.today = datetime.date.today().strftime("%Y/%m/%d")
    def getBooksSet( self ) :
        return self.bookIDs
    def getBookPaths( self ):
        # bookIDを取得
        for classCode in self.bookCodes :
            self.browser.get( self.searchPath )
            time.sleep(3)
            self.browser.find_element_ID( "SearchKW3Input" ).send_keys( classCode )
            self.browser.find_element_ID( "AssistListSelect" ).find_element( By.XPATH , "option[@value='100']" ).click()
            self.browser.find_element_ID( "startYear" ).send_keys( "2024" )
            self.browser.find_element_ID( "startMonth" ).send_keys( "11" )
            self.browser.find_element_ID( "endYear" ).send_keys( "2025" )
            self.browser.find_element_ID( "endMonth" ).send_keys( "02" )
            self.browser.find_element_XPATH( "//input[@value='検索']" ).click()
            time.sleep(5)
            self.getPage()
    def getBookInfo( self , id ) :
        self.browser.get( self.bookInfoPath + id )
        time.sleep(1)
        xp = "//*[@id='myshelf']/following-sibling::div[@class='detail-block bookinfo']/table/tbody/*"
        elements = self.browser.find_elements_XPATH( xp )
        book = dict()
        for tr in elements :
            tagText = tr.find_element( By.TAG_NAME , "th" ).text
            keyText = ""
            if tagText == "タイトルコード" :
                keyText = "titleCode"
            elif tagText == "出版年月" :
                keyText = "YYYY/MM"
            elif tagText == "書名" :
                keyText = "title"
            elif tagText == "著者名" :
                keyText = "author"
            elif tagText == "出版者" :
                keyText = "publisher"
            elif tagText == "ページ数" :
                keyText = "pages"
            elif tagText == "分類" :
                keyText = "NDC"
            elif tagText == "ISBN" :
                keyText = "ISBN"
            elif tagText == "内容紹介" :
                keyText = "content"
            elif tagText == "書誌種別" :
                keyText = "type"
            if keyText != "" :
                book[keyText] = tr.find_element( By.TAG_NAME , "td" ).text
        yyyymm = re.sub( r'[^0-9.]' , '' , book['YYYY/MM'] )
        if "." not in yyyymm :
            yyyymm += ".01"
        book['YYYY/MM'] = \
            datetime.datetime.strptime( yyyymm , "%Y.%m" ).strftime( "%Y/%m" )
        book['registration'] = self.today
        if "author" not in book.keys() :
            book["author"] = book["publisher"]
        book["library"] = self.library
        if len(book["NDC"]) > 3 :
            book["NDC"] = ".".join( [ book['NDC'][:3] , book['NDC'][3:] ] )
        if book["type"] == "電子図書" :
            book["library"] = "e-"+book["library"]
            if "ISBN" not in book.keys() :
                book["ISBN"] = "e" + book["titleCode"]
        elif "ISBN" not in book.keys() :
            book = None
        return book

    def getPage( self ) :
        e = self.browser.find_element_ID( "Main" ).find_element( By.XPATH , "form" )
        self.bookIDs \
            .update \
                ( \
                    { i.get_attribute("href")[-13:] \
                     for i in e.find_elements( By.XPATH , "div/div[@class='main']/table/tbody/tr/td/strong/a" ) \
                    } \
                )
        child = iter(e.find_elements( By.XPATH , "div[@class='paging p-bot']/*" ))
        while next(child).tag_name != "span":
            pass
        next_child = next(child)
        if next_child.tag_name == "a" :
            if next_child.text.rstrip().isnumeric() == True :
                next_child.click()
                time.sleep(15)
                self.getPage()
        return
