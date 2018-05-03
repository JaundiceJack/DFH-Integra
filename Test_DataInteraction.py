import sys
sys.path.append("./DataBase")
sys.path.append("./Direct")

from Declarative_Base import Base
import Declarative_RawItems
import Declarative_RawLots
import Declarative_Labs
import Declarative_Common
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#create a temporary database in memory for testing purposes
engine = create_engine('sqlite://')
#create database tables
Base.metadata.create_all(engine)
#create a session to communicate with the database
Session = sessionmaker(bind=engine)

#import stuff to test
import unittest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError
from DataInteraction import Interactive_RawItem, Interactive_RawLot
from DataInteraction import Interactive_RawAssay, Assay_Names

class OpenSession:
    def __enter__(self):
        self.session = Session()
        return self.session
    def __exit__(self, ex, exc, exce):
        self.session.close()

class If_all_goes_well_Tests(unittest.TestCase):
    def test_assay_names(self):
        assays = Assay_Names()
        with OpenSession() as session:
            assays.add_name(session, 'berberine')
            assays.add_name(session, 'taurine')
            assays.get_names(session)
            print(assays.names)
    
    def test_new_item(self):
        session = Session()
        item = Interactive_RawItem()
        item.item_number = 10001
        item.new(session)
        self.assertIsNotNone(item.data)
        session.close()
        
    def test_new_assays(self):
        session = Session()
        item = Interactive_RawItem()
        item.item_number = 10002
        item.new(session)
        item.assays.new(session, 'berberine')
        item.assays.new(session, 'magnesium')
        for key in item.assays.specific_keys:
            self.assertIsNotNone(item.assays.specific[key].data.name)
        session.close()
        
    def test_new_lots(self):
        session = Session()
        item = Interactive_RawItem(10003)
        item.new(session)
        item.lots.new(session, 'a8082233')
        for key in item.lots.specific_keys:
            self.assertIsNotNone(item.lots.specific[key].data)
        session.close()
    
    def test_new_lot_without_item(self):
        session = Session()
        lot = Interactive_RawLot(10004, 'a5553332')
        lot.new(session)
        self.assertIsNotNone(lot.data)
        session.close()

    #problem to solve here: when making a new assay, the new one does not receive the item number
    def test_assays(self):
        with OpenSession() as session:      
            item = Interactive_RawItem(10005)
            item.new(session)
            item.assays.new(session, 'berberine')
            print("assays test:")
            print(item.assays.data)
            print(item.assays.specific['berberine'].item_number)
            print(item.assays.specific['berberine'].table_class.__name__)  
            print("end assays test")
            print()

    def test_assay(self):
        with OpenSession() as session:
            item = Interactive_RawItem(10006)
            item.new(session)
            assay = Interactive_RawAssay(10006, 'berberine')
            assay.new(session)
            print("assay test:")
            print(assay.item_number)
            print(assay.identifier)
            print(assay.data)
            print("end assay test")
        
if __name__ == '__main__':
    unittest.main()