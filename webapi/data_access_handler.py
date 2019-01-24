from core.data import api
from core.data.models import *
from .models.base_response import *
from webapi.models.exceptions import *
import pandas as pd
import json
from core import BGConfig
from werkzeug.utils import secure_filename
import os

class DataAccessHandler(object):
    def __init__(self,db):
        self.db = db 
        super().__init__()

    def SearchProducts(self, searchParameters):        
        searchText = ""
        domain = ""
        if "searchtext" not in searchParameters :            
           return "[]"
        else:
            searchText = searchParameters["searchtext"]
            products = pd.read_sql("select docid, pn, weightage, incis, claims, filename, supplier from  public.search('{0}', '{1}');".format(searchText, domain),self.db.getEngine())
            return products.to_json(orient='records')

    def Products(self, supplierId):            
            products = pd.read_sql("select docid, pn, incis, claims, filename from  public.products({0});".format(supplierId),self.db.getEngine())
            return products.to_json(orient='records')
    def Product(self, productId):   
        # should return only the first row
            products = pd.read_sql("select docid, pn, incis, claims, filename from  public.product({0});".format(productId),self.db.getEngine())
            return products.to_json(orient='records')
    
    #http://flask.pocoo.org/docs/1.0/patterns/fileuploads/
    def uploadDocument(self, file):
        BGConfig.CreateFolders()
        print(os.path.join(BGConfig.DropLocation))

        if file.filename == '':
            raise CustomException("Invalid file. Please try again.", status_code=500)
        if file and self._allowed_file(file.filename):
            filename = secure_filename(file.filename)
            BGConfig.CreateAFolder(os.path.join(BGConfig.DropLocation, "1"))
            file.save(os.path.join(BGConfig.DropLocation, "1", filename)) #FIXME: Supplier id is hardcoded.

            document = Document(SupplId=1, Domain="SKN", FilePath = filename)
            session = self.db.getSession()
            session.add(document)
            try:
                session.commit()
            except Exception as ex:
                print (ex)
                raise CustomException("File upload failed. Please try again..", status_code=500)

            response = BaseResponse(1, "File Saved")
            return response
        else:
            raise CustomException("Invalid file. Please try again..", status_code=500)

        #Update database

    def _allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in BGConfig.ALLOWED_EXTENSIONS
