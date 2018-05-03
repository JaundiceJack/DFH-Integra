from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from Declarative_Base import Base
from Declarative_RawLots import Raw_Lot

#-----------------------------------------------------------------------------#

class Raw_Item(Base):
    __tablename__ = 'raw_items'
    
    #specifications: id is raw item number
    id     = Column(Integer, primary_key=True)
    name   = Column(String(64))
    note   = Column(String(256))
    fridge = Column(Boolean)
    
    #relationships:
    #array relations:
    lots      = relationship("Raw_Lot",      back_populates='item')    
    chem_ids  = relationship("Raw_Chem_ID",  back_populates='item')
    plant_ids = relationship("Raw_Plant_ID", back_populates='item')
    assays    = relationship("Raw_Assay",    back_populates='item')   
    #scalar relations:
    heavy_metals   = relationship("Raw_HM",           uselist=False, back_populates='item')
    allergens      = relationship("Raw_Allergens",    uselist=False, back_populates='item')
    pesticides     = relationship("Raw_Pesticides",   uselist=False, back_populates='item')
    organoleptics  = relationship("Raw_Organoleptics",uselist=False, back_populates='item')
    moisture       = relationship("Raw_Moisture",     uselist=False, back_populates='item')
    density        = relationship("Raw_Density",      uselist=False, back_populates='item')
    average_weight = relationship("Raw_Avgwt",        uselist=False, back_populates='item')
    microbes       = relationship("Raw_Microbes",     uselist=False, back_populates='item')
    pathogens      = relationship("Raw_Pathogens",    uselist=False, back_populates='item')
    rancidity      = relationship("Raw_Rancidity",    uselist=False, back_populates='item')
   
    def __repr__(self):
        line1 = "Raw_Item(id: %s)" % self.id
        line2 = "Columns(name: %s, note: %s, fridge: %s)" % \
        (self.name, self.note, self.fridge)
        return line1 + "\n" + line2
    
#-----------------------------------------------------------------------------#
    
class Raw_Assay(Base):
    __tablename__ = 'raw_assays'
    
    #identifiers
    id          = Column(Integer, primary_key=True)
    item        = relationship("Raw_Item", back_populates='assays')
    item_id     = Column(Integer, ForeignKey('raw_items.id'))
    #specifications
    name        = Column(String(64), ForeignKey('assay_names.name'))
    method      = Column(String(64))   
    lower_bound = Column(String(16))
    upper_bound = Column(String(16))
    units       = Column(String(32))
    dry_basis   = Column(Boolean)
    
    #duplicate prevention
    UniqueConstraint(item_id, name)       

    def __repr__(self):
        line1 = "Raw_Assay(item_id: %s)" % self.item_id
        line2 = "Columns(name: %s, method: %s, lower_bound: %s, upper_bound: %s, units: %s, dry_basis: %s)" % \
        (self.name, self.method, self.lower_bound, self.upper_bound, self.units, self.dry_basis)
        return line1 + "\n" + line2
    
#-----------------------------------------------------------------------------#

class Raw_Chem_ID(Base):
    __tablename__ = 'raw_chem_ids'
    
    #identifiers
    id       = Column(Integer, primary_key=True)   
    item     = relationship("Raw_Item", back_populates='chem_ids')
    item_id  = Column(Integer, ForeignKey('raw_items.id'))
    #specification
    name     = Column(String(64), ForeignKey('chem_id_names.name'))
    method   = Column(String(64))
    presence = Column(Boolean)  
 
    #duplicate prevention
    UniqueConstraint(item_id, name)

    def __repr__(self):
        line1 = "Raw_Chem_ID(item_id: %s)" % self.item_id
        line2 = "Columns(name: %s, method: %s, presence: %s)" % \
        (self.name, self.method, self.presence)
        return line1 + "\n" + line2

#-----------------------------------------------------------------------------#

class Raw_Plant_ID(Base):
    __tablename__ = 'raw_plant_ids'
    
    #identifiers
    id            = Column(Integer, primary_key=True)
    item          = relationship("Raw_Item", back_populates='plant_ids')
    item_id       = Column(Integer, ForeignKey('raw_items.id'))
    #specifications
    genus_species = Column(String(64))
    method        = Column(String(64))
    part          = Column(String(64))
    solvent       = Column(String(64))

    #duplicate prevention
    UniqueConstraint(item_id, genus_species)    

    def __repr__(self):
        line1 = "Raw_Plant_ID(item_id: %s)" % self.item_id
        line2 = "Columns(genus & species: %s, part: %s, solvent: %s, method: %s)" % \
        (self.genus_species, self.part, self.solvent, self.method)
        return line1 + "\n" + line2
    
#-----------------------------------------------------------------------------#

class Raw_HM(Base):
    __tablename__ = 'raw_hms'

    #identifiers
    id          = Column(Integer, primary_key=True)
    item        = relationship("Raw_Item", back_populates='heavy_metals')
    item_id     = Column(Integer, ForeignKey('raw_items.id'))
    #specifications
    units       = Column(String(32))
    arsenic_max = Column(String(16))
    cadmium_max = Column(String(16))
    lead_max    = Column(String(16))
    mercury_max = Column(String(16))
        
    def __repr__(self):
        line1 = "Raw_HM(item_id: %s)" % self.item_id
        line2 = "Columns(arsenic_max: %s, cadmium_max: %s, lead_max: %s, mercury_max: %s, units: %s)" % \
        (self.arsenic_max, self.cadmium_max, self.lead_max, self.mercury_max, self.units)
        return line1 + "\n" + line2

#-----------------------------------------------------------------------------#

class Raw_Allergens(Base):
    __tablename__ = 'raw_allergens'
    
    #identifiers
    id        = Column(Integer, primary_key=True)
    item      = relationship("Raw_Item", back_populates='allergens')
    item_id   = Column(Integer, ForeignKey('raw_items.id'))
    #specifications
    egg       = Column(Boolean)
    soy       = Column(Boolean)
    wheat     = Column(Boolean)
    fish      = Column(Boolean)
    milk      = Column(Boolean)
    treenut   = Column(Boolean)
    peanut    = Column(Boolean)
    shellfish = Column(Boolean)
    
    def __repr__(self):
        line1 = "Raw_Allergens(item_id: %s)" % self.item_id
        line2 = "Columns(egg: %s, soy: %s, wheat: %s, fish: %s, milk: %s, treenut: %s, peanut: %s, shellfish: %s)" % \
        (self.egg, self.soy, self.wheat, self.fish, self.milk, self.treenut, self.peanut, self.shellfish)
        return line1 + "\n" + line2
    
#-----------------------------------------------------------------------------#    

class Raw_Pesticides(Base):
    __tablename__ = 'raw_pesticides'
   
    #identifiers
    id       = Column(Integer, primary_key=True)
    item     = relationship("Raw_Item", back_populates='pesticides')
    item_id  = Column(Integer, ForeignKey('raw_items.id'))
    #specification
    standard = Column(String(32))   
    
    def __repr__(self):
        line1 = "Raw_Pesticides(item_id: %s)" % self.item_id
        line2 = "Columns(standard: %s)" % \
        (self.standard)
        return line1 + "\n" + line2
        
#-----------------------------------------------------------------------------#

class Raw_Microbes(Base):
    __tablename__ = 'raw_microbes'
    
    #identifiers
    id      = Column(Integer, primary_key=True)
    item    = relationship("Raw_Item", back_populates='microbes')
    item_id = Column(Integer, ForeignKey('raw_items.id'))
    #specifications
    tpc_min = Column(Integer)
    ym_min  = Column(Integer)
    tpc_max = Column(Integer)
    ym_max  = Column(Integer)
      
    def __repr__(self):
        line1 = "Raw_Microbes(item_id: %s)" % self.item_id
        line2 = "Columns(tpc_min: %s, ym_min: %s, tpc_max: %s, ym_max: %s)" % \
        (self.tpc_min, self.ym_min, self.tpc_max, self.ym_max)
        return line1 + "\n" + line2
            
#-----------------------------------------------------------------------------#

class Raw_Pathogens(Base):
    __tablename__ = 'raw_pathogens'
    
    #identifiers
    id         = Column(Integer, primary_key=True)
    item       = relationship("Raw_Item", back_populates='pathogens')
    item_id    = Column(Integer, ForeignKey('raw_items.id'))
    #specifications
    ecoli      = Column(Boolean)
    salmonella = Column(Boolean)
    staph      = Column(Boolean)
 
    def __repr__(self):
        line1 = "Raw_Pathogens(item_id: %s)" % self.item_id
        line2 = "Columns(ecoli: %s, salmonella: %s, staph: %s)" % \
        (self.ecoli, self.salmonella, self.staph)
        return line1 + "\n" + line2

#-----------------------------------------------------------------------------# 

class Raw_Organoleptics(Base):
    __tablename__ = 'raw_organoleptics'
    
    #identifiers
    id         = Column(Integer, primary_key=True)
    item       = relationship("Raw_Item", back_populates='organoleptics')
    item_id    = Column(Integer, ForeignKey('raw_items.id'))
    #specifications
    color      = Column(String(64))
    odor       = Column(String(64))
    appearance = Column(String(64))
    
    def __repr__(self):
        line1 = "Raw_Organoleptics(item_id: %s)" % self.item_id
        line2 = "Columns(color: %s, odor: %s, appearance: %s)" % \
        (self.color, self.odor, self.appearance)
        return line1 + "\n" + line2

#-----------------------------------------------------------------------------#

class Raw_Moisture(Base):
    __tablename__ = 'raw_moistures'
    
    #identifiers
    id          = Column(Integer, primary_key=True)
    item = relationship("Raw_Item", back_populates='moisture')
    item_id = Column(Integer, ForeignKey('raw_items.id'))
    #specifications
    lower_bound = Column(String(16))
    upper_bound = Column(String(16))
   
    def __repr__(self):
        line1 = "Raw_Moisture(item_id: %s)" % self.item_id
        line2 = "Columns(lower_bound: %s, upper_bound: %s)" % \
        (self.lower_bound, self.upper_bound)
        return line1 + "\n" + line2

#-----------------------------------------------------------------------------#

class Raw_Density(Base):
    __tablename__ = 'raw_densities'
    
    #identifiers
    id       = Column(Integer, primary_key=True)
    item     = relationship("Raw_Item", back_populates='density')
    item_id  = Column(Integer, ForeignKey('raw_items.id'))
    #specifications
    flow_min = Column(String(16))
    flow_max = Column(String(16))
    tap_min  = Column(String(16))
    tap_max  = Column(String(16))

    def __repr__(self):
        line1 = "Raw_Density(item_id: %s)" % self.item_id
        line2 = "Columns(flow_min: %s, flow_max: %s, tap_min: %s, tap_max: %s)" % \
        (self.flow_min, self.flow_max, self.tap_min, self.tap_max)
        return line1 + "\n" + line2

#-----------------------------------------------------------------------------#

class Raw_Avgwt(Base):
    __tablename__ = 'raw_avgwts'
    
    #identifiers
    id          = Column(Integer, primary_key=True)
    item = relationship("Raw_Item", back_populates='average_weight')
    item_id = Column(Integer, ForeignKey('raw_items.id'))
    #specifications
    lower_bound = Column(String(16))
    upper_bound = Column(String(16))    
        
    def __repr__(self):
        line1 = "Raw_Average_Weight(item_id: %s)" % self.item_id
        line2 = "Columns(lower_bound: %s, upper_bound: %s)" % \
        (self.lower_bound, self.upper_bound)
        return line1 + "\n" + line2

#-----------------------------------------------------------------------------#

class Raw_Rancidity(Base):
    __tablename__ = 'raw_rancidities'
    
    #identifiers
    id            = Column(Integer, primary_key=True)
    item          = relationship("Raw_Item", back_populates='rancidity')
    item_id       = Column(Integer, ForeignKey('raw_items.id'))
    #specifications
    peroxide_max  = Column(String(16))
    anisidine_max = Column(String(16))
    oxidation_max = Column(String(16))  

    def __repr__(self):
        line1 = "Raw_Rancidity(item_id: %s)" % self.item_id
        line2 = "Columns(peroxide_max: %s, anisidine_max: %s, oxidation_max: %s)" % \
        (self.peroxide_max, self.anisidine_max, self.oxidation_max)
        return line1 + "\n" + line2
        
#-----------------------------------------------------------------------------#