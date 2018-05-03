from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from Declarative_Base import Base


#-----------------------------------------------------------------------------#

class Lab(Base):
    __tablename__ = 'labs'
    
    #
    id      = Column(Integer, primary_key=True)
    name    = Column(String(64), unique=True)
    address = Column(String(256))   
    
    #relationships:
    assay_prices = relationship("Assay_Price", back_populates='lab')
    chem_id_prices = relationship("Chem_ID_Price",  back_populates='lab')
    plant_id_price = relationship("Plant_ID_Price", uselist = False, back_populates='lab')
    hm_price = relationship("HM_Price", uselist = False, back_populates='lab')
    micro_price =  relationship("Micro_Price", uselist = False, back_populates='lab')
       
    raw_assays_tested  = relationship("Raw_Assay_Test", back_populates='lab')
    raw_chem_ids_tested = relationship("Raw_Chem_ID_Test", back_populates='lab')
    raw_plant_ids_tested =  relationship("Raw_Plant_ID_Test", back_populates='lab')
    raw_pesticides_tested =  relationship("Raw_Pesticides_Test", back_populates='lab')
    raw_hms_tested  =  relationship("Raw_HM_Test", back_populates='lab')
    raw_allergens_tested = relationship("Raw_Allergens_Test", back_populates='lab')
    raw_microbes_tested =  relationship("Raw_Microbes_Test", back_populates='lab')
    raw_pathogens_tested =  relationship("Raw_Pathogens_Test", back_populates='lab')
    raw_organoleptics_tested =  relationship("Raw_Organoleptics_Test", back_populates='lab')
    raw_densities_tested =  relationship("Raw_Density_Test", back_populates='lab')
    raw_moistures_tested =  relationship("Raw_Moisture_Test", back_populates='lab')
    raw_avgwts_tested =  relationship("Raw_Avgwt_Test", back_populates='lab')
    raw_rancidities_tested =  relationship("Raw_Rancidity_Test", back_populates='lab')
    
    def __repr__(self):
        line1 = "Lab(id: %s)" % self.id
        line2 = "Columns(name: %s, address: %s)" % \
        (self.name, self.address)
        return line1 + "\n" + line2
    
#-----------------------------------------------------------------------------#

class Assay_Price(Base):
    __tablename__ = 'assay_prices'
    
    #identifiers
    id        = Column(Integer, primary_key = True)
    lab       = relationship("Lab", back_populates='assay_prices')
    lab_id    = Column(Integer, ForeignKey('labs.id'))

    name = Column(String(64), ForeignKey('assay_names.name'))
    method = Column(String(64))
    
    #price data
    price     = Column(String(16))
    base_tat  = Column(Integer)
    rush_tat  = Column(Integer)
    emerg_tat = Column(Integer)

#-----------------------------------------------------------------------------#

class Chem_ID_Price(Base):
    __tablename__ = 'chem_id_prices'
    
    #identifiers
    id        = Column(Integer, primary_key = True)
    lab       = relationship("Lab", back_populates='chem_id_prices')
    lab_id    = Column(Integer, ForeignKey('labs.id'))

    name = Column(String(64), ForeignKey('chem_id_names.name'))
    method = Column(String(64))
    
    #price data
    price     = Column(String(16))
    base_tat  = Column(Integer)
    rush_tat  = Column(Integer)
    emerg_tat = Column(Integer)    

#-----------------------------------------------------------------------------#

class Plant_ID_Price(Base):
    __tablename__ = 'plant_id_prices'
    
    #identifiers
    id        = Column(Integer, primary_key = True)
    lab       = relationship("Lab", back_populates='plant_id_price')
    lab_id    = Column(Integer, ForeignKey('labs.id'))

    method = Column(String(64))
    
    #price data
    price     = Column(String(16))
    base_tat  = Column(Integer)
    rush_tat  = Column(Integer)
    emerg_tat = Column(Integer)

#-----------------------------------------------------------------------------#    

class HM_Price(Base):
    __tablename__ = 'hm_prices'
    
    #identifiers
    id        = Column(Integer, primary_key = True)
    lab       = relationship("Lab", back_populates='hm_price')
    lab_id    = Column(Integer, ForeignKey('labs.id'))

    method = Column(String(64))
    
    #price data
    price     = Column(String(16))
    base_tat  = Column(Integer)
    rush_tat  = Column(Integer)
    emerg_tat = Column(Integer)

#-----------------------------------------------------------------------------#

class Micro_Price(Base):
    __tablename__ = 'micro_prices'
    
    #identifiers
    id        = Column(Integer, primary_key = True)
    lab       = relationship("Lab", back_populates='micro_price')
    lab_id    = Column(Integer, ForeignKey('labs.id'))
    
    #price data
    standard_panel_price = Column(String(16))
    pathogens_price = Column(String(16))
    tpc_price = Column(String(16))
    ym_price = Column(String(16))
    
    base_tat  = Column(Integer)
    rush_tat  = Column(Integer)
    emerg_tat = Column(Integer) 
    
#-----------------------------------------------------------------------------#    
