from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
import pandas as pd
from datetime import datetime
from core.data.common_models import *
from core.data.user_models import *

iff = lambda x, df : x if x else df

class Supplier(Base):
    '''
    SupplId     Name
    1           BASF
    '''
    __tablename__ = 'Suppliers'
    
    SupplId = Column(BigInteger, primary_key=True)
    Name = Column(String)
    Location = Column(String)
    Documents = None

    def __repr__(self):
        return "<Supplier(SupplId='%u', Name='%s')>" % (iff(self.SupplId, 0), self.Name)

class Document(Base):
    '''
    DocId	SupplId	Domain	File_Path
    1	1	SKN	/abc/bcd.pdf
    '''
    __tablename__ = 'Documents'

    DocId = Column(BigInteger, primary_key=True)
    SupplId = Column(BigInteger, ForeignKey('Suppliers.SupplId'))
    Domain = Column(String)
    FilePath = Column(String)
    
    Suppl = relationship("Supplier", back_populates="Documents")

    TagMetaData = None


    def __repr__(self):
        return "<Document(DocId='%u', SupplId='%u', Domain='%s', FilePath='%s')>" % (
            iff(self.DocId, 0), self.SuppId, self.Domain, self.FilePath)

Supplier.Documents = relationship("Document", order_by="Document.DocId", back_populates="Suppl")


class TagClass(Base):
    '''
    ClassId	    ClassName
    1	        Document
    2	        Paragraph
    3	        Sentence
    4	        Phrase
    '''
    __tablename__ = 'TagClasses'
    ClassId = Column(BigInteger, primary_key=True)
    Name = Column(String, unique=True)



    TagMetaData = None


    def __repr__(self):
        return "<TagClass(ClassId='%u', Name='%s')>" % (iff(self.ClassId, 0), self.Name)


class Tag(Base):
    '''
    TagID   TagName     TagDesc
    1       BEN     Benefit
    '''
    __tablename__ = 'Tags'

    TagId= Column(BigInteger, primary_key=True)
    Name = Column(String, unique=True)
    Definition = Column(String)
    Description = Column(String)

    TagMetaData = None

    def __repr__(self):
        return "<Tag(TagId='%u', Name='%s', Definition='%s', Description='%s')>" % (iff(self.TagId, 0), self.Name, self.Definition, self.Description)


class DocMetaData(Base):
    '''
    DocId   Tag     TagClass    Score   TagData             PageNo  Offset
    1       1       2             .35   Sdsdfafsafss sdsds  1       20
    '''
    __tablename__ = 'DocMetaData'

    Id = Column(BigInteger, primary_key=True)
    DocId = Column(BigInteger, ForeignKey("Documents.DocId"))
    TagId = Column(BigInteger, ForeignKey("Tags.TagId"))
    TagClassId = Column(BigInteger, ForeignKey("TagClasses.ClassId"))
    Score = Column(Float, nullable=True)
    TagData = Column(String, nullable=False)
    PageNo = Column(Integer, nullable=True)
    Offset = Column(Integer, nullable=True)
    TStamp = Column(DateTime, onupdate=datetime.now)

    Doc = relationship('Document', back_populates="TagMetaData")
    tag = relationship("Tag", back_populates="TagMetaData")
    tagClass = relationship("TagClass", back_populates="TagMetaData")

    def __repr__(self):
        return "<DocMetaData(DocId='%u', TagId='%u', TagClassId='%u', Score=%.4f, TagData='%s', PageNo=%i, Offset=%i)>" % (
            iff(self.DocId, 0), iff(self.TagId, 0), iff(self.TagClassId, 0), iff(self.Score, 0.0), self.TagData, iff(self.PageNo, 0), iff(self.Offset, 0)
            )

Document.TagMetaData = relationship("DocMetaData", order_by=DocMetaData.Id, back_populates="Doc")
Tag.TagMetaData = relationship("DocMetaData", order_by=DocMetaData.Id, back_populates="tag")
TagClass.TagMetaData = relationship("DocMetaData", order_by=DocMetaData.Id, back_populates="tagClass")

def dropTables(engine):
    Base.metadata.drop_all(engine)

def createTables(engine):
    Base.metadata.create_all(engine)

def seedTagClasses(dbsession):
    #1          Document
    #2	        Paragraph
    #3	        Sentence
    #4	        Phrase
    tagclasses = [
       TagClass(ClassId=1, Name="Document"),
       TagClass(ClassId=2, Name="Paragraph"),
       TagClass(ClassId=3, Name="Sentence"),
       TagClass(ClassId=4, Name="Phrase")
    ]
    dbsession.add_all(tagclasses)
    dbsession.commit()

def seedTags(dbsession):
    tagDataFrame = pd.read_csv("Tags.csv")
    tagDataFrame = tagDataFrame.fillna('')
    tags = [Tag(Name=row[0], Definition=row[1], Description=row[2]) for index, row in tagDataFrame.iterrows()]
    dbsession.add_all(tags)
    print(dbsession.dirty)
    dbsession.commit()

def seedSampleSupplier(dbsession):
    supl = Supplier()
    supl.SupplId = 1
    supl.Name = 'Eureka Products'
    supl.Location = "USA"
    dbsession.add(supl)
    dbsession.commit()

def seedDatabase(dbsession):
    ''' Populate tags from tag dictionary '''

    #return # to avoid accidental running.

    if not dbsession:
        raise ValueError("dbsession is not defined.")
    # drop all tables
    #dropTables(dbsession.get_bind())
    createTables(dbsession.get_bind())
    #seedTags(dbsession)
    #seedTagClasses(dbsession)
    #seedSampleSupplier(dbsession)

