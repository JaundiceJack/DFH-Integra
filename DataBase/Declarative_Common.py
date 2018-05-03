from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from Declarative_Base import Base
from Declarative_Labs import Assay_Price, Chem_ID_Price
from Declarative_RawLots import Raw_Lot_Spec_Assay, Raw_Lot_Spec_Chem_ID
from Declarative_RawItems import Raw_Assay, Raw_Chem_ID


class Assay_Name(Base):
    __tablename__ = 'assay_names'
    
    id   = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    
    raw_item_assays = relationship("Raw_Assay")
    raw_lot_assays  = relationship("Raw_Lot_Spec_Assay")
    assay_prices    = relationship("Assay_Price")
    
class Chem_ID_Name(Base):
    __tablename__ = 'chem_id_names'
    
    id   = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    
    raw_item_chem_ids = relationship("Raw_Chem_ID")
    raw_lot_chem_ids  = relationship("Raw_Lot_Spec_Chem_ID")
    chem_id_prices    = relationship("Chem_ID_Price")
"""   
class Plant_ID_Name(Base):
    __tablename__ = 'plant_id_names'
    
    id = Column(Integer, primary_key = True)
    name = Column(String(64), unique = True)
    
    raw_item_plant_ids = relationship("Raw_Plant_ID")
    raw_lot_plant_ids = relationship("Raw_Lot_Spec_Plant_ID")
    plant_id_prices = relationship("Plant_ID_Price")
"""