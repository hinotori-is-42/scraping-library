from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import pathlib
import os
import shutil
import sys

class Browser():
    def __init__( self ):
        # snap/firefoxでは動作しないことへの対応
        # 元の環境変数TMPDIRを保存
        self.originalTmpDir = os.environ.get('TMPDIR')
        # tmpdirディレクトリを指定
        self.tmpdirPath = pathlib.Path.cwd() / 'tmpdir'
        # tmpdirディレクトリが存在しない場合は作成
        self.tmpdirPath.mkdir(exist_ok=True)
        # TMPDIRを設定
        os.environ['TMPDIR'] = str(self.tmpdirPath)
        # snap/firefoxでは動作しないことへの対応 ここまで
        # geckodriverのパス
        service = Service('/usr/local/bin/geckodriver')
        # Firefoxオプション設定
        options = Options()
        options.binary_location = '/snap/bin/firefox'
        # options.add_argument('-headless')  # ヘッドレスモード
        # Firefoxブラウザを起動
        self.origin = webdriver.Firefox(service=service, options=options)
        self.origin.implicitly_wait(5)
    def get( self , path ) :
        return self.origin.get( path )
    def find_element_ID( self , id ) :
        return self.origin.find_element( By.ID , id )
    def find_element_XPATH( self , xpath ) :
        return self.origin.find_element( By.XPATH , xpath )
    def find_elements_XPATH( self , xpath ) :
        return self.origin.find_elements( By.XPATH , xpath )
    def __del__( self ) :
        # Firefoxブラウザを閉じる
        self.origin.close()
        # snap/firefoxでは動作しないことへの対応
        # tmpdirを削除
        shutil.rmtree(self.tmpdirPath)
        # 環境変数TMPDIRを元に戻す
        if self.originalTmpDir is not None:
            os.environ['TMPDIR'] = self.originalTmpDir # 元の値に戻す
        else:
            os.environ.pop('TMPDIR', None)  # 環境変数が元々なければ削除
