from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from Declarative_Base import Base

from Declarative_Labs import Lab

#-----------------------------------------------------------------------------#

class Raw_Lot(Base):
    __tablename__ = 'raw_lots'
    
    #lot data
    id                    = Column(Integer, primary_key=True)
    lot_number            = Column(String(64))
    units                 = Column(String(32))
    vendor                = Column(String(64))
    vendor_lot            = Column(String(64))  
    expected_release_date = Column(Date)
    actual_release_date   = Column(Date)    
    lot_note              = Column(String(256))
    delay_note            = Column(String(256))     
    
    #relationships:
    item    = relationship("Raw_Item", back_populates='lots')
    item_id = Column(Integer, ForeignKey('raw_items.id'))  
    #array relations
    chem_id_results  = relationship("Raw_Chem_ID_Result", back_populates='lot')
    plant_id_results = relationship("Raw_Plant_ID_Result", back_populates='lot')
    assay_results    = relationship("Raw_Assay_Result", back_populates='lot')
    #scalar relations: lot data
    location       = relationship("Raw_Lot_Location", uselist=False, back_populates='lot')
    receiving_data = relationship("Raw_Lot_Receiving_Data", uselist=False, back_populates='lot')
    sage_data      = relationship("Raw_Lot_Sage_Data", uselist=False, back_populates='lot')
    #scalar relations: result data
    hm_result            = relationship("Raw_HM_Result", uselist=False, back_populates='lot')
    allergens_result     = relationship("Raw_Allergens_Result", uselist=False, back_populates='lot')
    pesticides_result    = relationship("Raw_Pesticides_Result", uselist=False, back_populates='lot')        
    organoleptics_result = relationship("Raw_Organoleptics_Result", uselist=False, back_populates='lot')   
    moisture_result      = relationship("Raw_Moisture_Result", uselist=False, back_populates='lot')
    density_result       = relationship("Raw_Density_Result", uselist=False, back_populates='lot')
    avgwt_result         = relationship("Raw_Avgwt_Result", uselist=False, back_populates='lot')    
    microbes_result      = relationship("Raw_Microbes_Result", uselist=False, back_populates='lot')
    pathogens_result     = relationship("Raw_Pathogens_Result", uselist=False, back_populates='lot')   
    rancidity_result     = relationship("Raw_Rancidity_Result", uselist=False, back_populates='lot')
    
    #duplicate prevention
    UniqueConstraint(item_id, lot_number)
                
    def __repr__(self):
        return "Raw_Lot(lot number: %s)" % (self.lot_number)

#-----------------------------------------------------------------------------#

class Raw_Lot_Location(Base):
    __tablename__ = 'raw_lot_locations'
    
    #location data
    id             = Column(Integer, primary_key='True')
    facility       = Column(String(16)) #LVN, AMM, CT, or FL
    wh_code        = Column(String(16))
    
    #relationships:
    lot_id = Column(Integer, ForeignKey('raw_lots.id'))
    lot = relationship("Raw_Lot", uselist=False, back_populates='location') 
  
    def __repr__(self):
        line1 = "Raw_Lot_Location(lot_number: %s)" % self.lot_number
        line2 = "Columns(facility: %s, warehouse_code: %s)" % \
        (self.facility, self.warehouse_code)
        return line1 + "\n" + line2

#-----------------------------------------------------------------------------#

class Raw_Lot_Sage_Data(Base):
    __tablename__ = 'raw_lot_sage_data'
    
    #the id is factless
    id           = Column(Integer, primary_key='True')
    total_amount = Column(String(16))
    amount_in_a  = Column(String(16))
    amount_in_r  = Column(String(16))
    amount_in_q  = Column(String(16))
    amount_in_ac = Column(String(16))    
    
    #relationships:
    lot = relationship("Raw_Lot", uselist=False, back_populates='sage_data')    
    lot_id = Column(Integer, ForeignKey('raw_lots.id'))
    
    def __repr__(self):
        line1 = "Raw_Lot_Sage_Data(lot_number: %s)" % self.lot_number
        line2 = "Columns(total_amount: %s, amount_in_a: %s, amount_in_r: %s, amount_in_q: %s, amount_in_ac: %s)" % \
        (self.total_amount, self.amount_in_a, self.amount_in_r, self.amount_in_q, self.amount_in_ac)
        return line1 + "\n" + line2

#-----------------------------------------------------------------------------#

class Raw_Lot_Receiving_Data(Base):
    __tablename__ = 'raw_lot_receiving_data'
    
    #the id is factless
    id     = Column(Integer, primary_key='True')
    po     = Column(Integer)
    date   = Column(Date)
    amount = Column(String(16))
    
    
    #relationships:
    lot_id = Column(Integer, ForeignKey('raw_lots.id'))
    lot = relationship("Raw_Lot", back_populates='receiving_data')

    def __repr__(self):
        line1 = "Raw_Lot_Receiving_Data(lot_number: %s)" % self.lot.lot_number
        line2 = "Columns(po: %s, date: %s, amount: %s)" % \
        (self.po, self.date, self.amount)
        return line1 + "\n" + line2 
   
#-----------------------------------------------------------------------------#

class Raw_Assay_Result(Base):
    __tablename__ = 'raw_assay_results'

    #identifiers
    id     = Column(Integer, primary_key=True)
    lot    = relationship("Raw_Lot", uselist=False, back_populates='assay_results')
    lot_id = Column(Integer, ForeignKey('raw_lots.id'))
    
#You're getting multiple unwanted results because you only query for the lot,
#but there might be multiple different results under the same lot number for different items
#change the lot_number above to lot_id instead and obtain the lot number through lot like you're supposed to,
#no need to add an item_id relation here
    
    #external data
    spec  = relationship("Raw_Lot_Spec_Assay", uselist=False,
                         lazy='joined', back_populates='result')
    tests = relationship("Raw_Assay_Test", back_populates='result')
    #result
    result = Column(String(32))
    
    def __repr__(self):
        line1 = "Raw_Assay_Result(lot_number: %s)" % self.lot_number
        line2 = "Columns(result: %s)" % \
        (self.result)
        return line1 + "\n" + line2

#-----------------------------------------------------------------------------#

class Raw_Chem_ID_Result(Base):
    __tablename__ = 'raw_chem_id_results'
    
    #identifiers
    id     = Column(Integer, primary_key='True')
    lot    = relationship("Raw_Lot", uselist=False, back_populates='chem_id_results')
    lot_id = Column(Integer, ForeignKey('raw_lots.id'))
    #external data
    spec  = relationship("Raw_Lot_Spec_Chem_ID", uselist=False,
                         lazy='joined', back_populates='result')
    tests = relationship("Raw_Chem_ID_Test", back_populates='result')
    #result
    result = Column(Boolean) 
    
    def __repr__(self):
        line1 = "Raw_Chem_ID_Result(lot_number: %s)" % self.lot_number
        line2 = "Columns(result: %s)" % \
        (self.result)
        return line1 + "\n" + line2
    
#-----------------------------------------------------------------------------#

class Raw_Plant_ID_Result(Base):
    __tablename__ = 'raw_plant_id_results'
    
    #identifiers
    id     = Column(Integer, primary_key=True)
    lot    = relationship("Raw_Lot", uselist=False, back_populates='plant_id_results')
    lot_id = Column(Integer, ForeignKey('raw_lots.id'))
    #external data
    spec  = relationship("Raw_Lot_Spec_Plant_ID", uselist=False,
                         lazy='joined', back_populates='result')
    tests = relationship("Raw_Plant_ID_Test", back_populates='result')
    #result: complies, genus_id_only, or id_failure
    result = Column(String(64)) 

    def __repr__(self):
        line1 = "Raw_Plant_ID_Result(lot_number: %s)" % self.lot_number
        line2 = "Columns(result: %s)" % \
        (self.result)
        return line1 + "\n" + line2

#-----------------------------------------------------------------------------#

class Raw_HM_Result(Base):
    __tablename__ = 'raw_hm_results'

    #identifiers
    id     = Column(Integer, primary_key=True)
    lot    = relationship("Raw_Lot", uselist=False, back_populates='hm_result')
    lot_id = Column(Integer, ForeignKey('raw_lots.id'))
    #external data
    spec  = relationship("Raw_Lot_Spec_HM", uselist=False,
                         lazy='joined', back_populates='result')
    tests = relationship("Raw_HM_Test", back_populates='result')
    #results
    arsenic_result = Column(String(16))
    cadmium_result = Column(String(16))
    lead_result    = Column(String(16))
    mercury_result = Column(String(16))    
    
    def __repr__(self):
        line1 = "Raw_HM_Result(lot_number: %s)" % self.lot_number
        line2 = "Columns(arsenic_result: %s, cadmium_result: %s, lead_result: %s, mercury_result: %s)" % \
        (self.arsenic_result, self.cadmium_result, self.lead_result, self.mercury_result)
        return line1 + "\n" + line2

#-----------------------------------------------------------------------------#

class Raw_Allergens_Result(Base):
    __tablename__ = 'raw_allergens_results'
    
    #identifiers
    id     = Column(Integer, primary_key=True)
    lot    = relationship("Raw_Lot", uselist=False, back_populates='allergens_result')
    lot_id = Column(Integer, ForeignKey('raw_lots.id'))
    #external data
    spec  = relationship("Raw_Lot_Spec_Allergens", uselist=False,
                         lazy='joined', back_populates='result')
    tests = relationship("Raw_Allergens_Test", back_populates='result')
    #results
    egg_result       = Column(String(16))
    soy_result       = Column(String(16))
    wheat_result     = Column(String(16))
    fish_result      = Column(String(16))
    milk_result      = Column(String(16))
    treenut_result   = Column(String(16))
    peanut_result    = Column(String(16))
    shellfish_result = Column(String(16))
    
    def __repr__(self):
        line1 = "Raw_Allergens_Result(lot_number: %s)" % self.lot_number
        line2 = "Columns(egg_result: %s, soy_result: %s, wheat_result: %s, fish_result: %s," % \
        (self.egg_result, self.soy_result, self.wheat_result, self.fish_result)
        line3 = "milk_result: %s, treenut_result: %s, peanut_result: %s, shellfish_result: %s)" % \
        (self.milk_result, self.treenut_result, self.peanut_result, self.shellfish_result)
        return line1 + "\n" + line2 + "\n" + line3        

#-----------------------------------------------------------------------------#       

class Raw_Pesticides_Result(Base):
    __tablename__ = 'raw_pesticides_results'

    #identifiers
    id     = Column(Integer, primary_key=True)
    lot    = relationship("Raw_Lot", uselist=False, back_populates='pesticides_result')
    lot_id = Column(Integer, ForeignKey('raw_lots.id'))
    #external data
    spec  = relationship("Raw_Lot_Spec_Pesticides", uselist=False,
                         lazy='joined', back_populates='result')
    tests = relationship("Raw_Pesticides_Test", back_populates='result')
    #result
    result = Column(Boolean)
 
    def __repr__(self):
        line1 = "Raw_Pesticides_Result(lot_number: %s)" % self.lot_number
        line2 = "Columns(result: %s)" % \
        (self.result)
        return line1 + "\n" + line2
      
#-----------------------------------------------------------------------------#

class Raw_Microbes_Result(Base):
    __tablename__ = 'raw_microbes_results'
    
    #identifiers
    id     = Column(Integer, primary_key=True)
    lot    = relationship("Raw_Lot", uselist=False, back_populates='microbes_result')
    lot_id = Column(Integer, ForeignKey('raw_lots.id'))
    #external data
    spec  = relationship("Raw_Lot_Spec_Microbes", uselist=False,
                         lazy='joined', back_populates='result')
    tests = relationship("Raw_Microbes_Test", back_populates='result')
    #results
    tpc_result = Column(String(16))
    ym_result  = Column(String(16)) 

    def __repr__(self):
        line1 = "Raw_Microbe_Result(lot_number: %s)" % self.lot_number
        line2 = "Columns(tpc_result: %s, ym_result: %s)" % \
        (self.tpc_result, self.ym_result)
        return line1 + "\n" + line2

#-----------------------------------------------------------------------------#

class Raw_Pathogens_Result(Base):
    __tablename__ = 'raw_pathogens_results'
    
    #identifiers
    id     = Column(Integer, primary_key=True)
    lot    = relationship("Raw_Lot", uselist=False, back_populates='pathogens_result')
    lot_id = Column(Integer, ForeignKey('raw_lots.id'))
    #external data
    spec  = relationship("Raw_Lot_Spec_Pathogens", uselist=False,
                         lazy='joined', back_populates='result')
    tests = relationship("Raw_Pathogens_Test", back_populates='result')
    #results
    ecoli_result      = Column(Boolean)
    salmonella_result = Column(Boolean)
    staph_result      = Column(Boolean)
    
    def __repr__(self):
        line1 = "Raw_Pathogens_Result(lot_number: %s)" % self.lot_number
        line2 = "Columns(ecoli_result: %s, salmonella_result: %s, staph_result: %s)" % \
        (self.ecoli_result, self.salmonella_result, self.staph_result)
        return line1 + "\n" + line2
    
#-----------------------------------------------------------------------------#

class Raw_Organoleptics_Result(Base):
    __tablename__ = 'raw_organoleptics_results'

    #identifiers
    id     = Column(Integer, primary_key=True)
    lot    = relationship("Raw_Lot", uselist=False, back_populates='organoleptics_result')
    lot_id = Column(Integer, ForeignKey('raw_lots.id'))
    #external data
    spec  = relationship("Raw_Lot_Spec_Organoleptics", uselist=False,
                         lazy='joined', back_populates='result')
    tests = relationship("Raw_Organoleptics_Test", back_populates='result')
    #results
    color_result      = Column(String(64))
    odor_result       = Column(String(64))
    appearance_result = Column(String(64))    
        
    def __repr__(self):
        line1 = "Raw_Organoleptics_Result(lot_number: %s)" % self.lot_number
        line2 = "Columns(color_result: %s, odor_result: %s, appearance_result: %s)" % \
        (self.color_result, self.odor_result, self.appearance_result)
        return line1 + "\n" + line2   

#-----------------------------------------------------------------------------#

class Raw_Moisture_Result(Base):
    __tablename__ = 'raw_moisture_results'
    
    #identifiers
    id     = Column(Integer, primary_key=True)
    lot    = relationship("Raw_Lot", uselist=False, back_populates='moisture_result')
    lot_id = Column(Integer, ForeignKey('raw_lots.id'))
    #external data
    spec  = relationship("Raw_Lot_Spec_Moisture", uselist=False,
                         lazy='joined', back_populates='result')
    tests = relationship("Raw_Moisture_Test", back_populates='result')
    #result
    result = Column(String(16))
    
    def __repr__(self):
        line1 = "Raw_Moisture_Result(lot_number: %s)" % self.lot_number
        line2 = "Columns(result: %s)" % \
        (self.result)
        return line1 + "\n" + line2       

#-----------------------------------------------------------------------------#

class Raw_Density_Result(Base):
    __tablename__ = 'raw_density_results'

    #identifiers
    id     = Column(Integer, primary_key=True)
    lot    = relationship("Raw_Lot", uselist=False, back_populates='density_result')
    lot_id = Column(Integer, ForeignKey('raw_lots.id'))
    #external data
    spec  = relationship("Raw_Lot_Spec_Density", uselist=False,
                         lazy='joined', back_populates='result')
    tests = relationship("Raw_Density_Test", back_populates='result')
    #result
    tap_result  = Column(String(16))
    flow_result = Column(String(16))  

    def __repr__(self):
        line1 = "Raw_Density_Result(lot_number: %s)" % self.lot_number
        line2 = "Columns(flow_result: %s, tap_result: %s)" % \
        (self.flow_result, self.tap_result)
        return line1 + "\n" + line2

#-----------------------------------------------------------------------------#

class Raw_Avgwt_Result(Base):
    __tablename__ = 'raw_avgwt_results'
    
    #identifiers 
    id     = Column(Integer, primary_key=True)
    lot    = relationship("Raw_Lot", uselist=False, back_populates='avgwt_result')
    lot_id = Column(Integer, ForeignKey('raw_lots.id'))
    #external data
    spec  = relationship("Raw_Lot_Spec_Avgwt", uselist=False,
                         lazy='joined', back_populates='result')
    tests = relationship("Raw_Avgwt_Test", back_populates='result')
    #results (The measurements are optional record-keeping)
    measurement_01 = Column(String(16))
    measurement_02 = Column(String(16))
    measurement_03 = Column(String(16))
    measurement_04 = Column(String(16))
    measurement_05 = Column(String(16))
    measurement_06 = Column(String(16))
    measurement_07 = Column(String(16))
    measurement_08 = Column(String(16))
    measurement_09 = Column(String(16))
    measurement_10 = Column(String(16))
    measurement_11 = Column(String(16))
    measurement_12 = Column(String(16))
    measurement_13 = Column(String(16))
    measurement_14 = Column(String(16))
    measurement_15 = Column(String(16))
    measurement_16 = Column(String(16))
    measurement_17 = Column(String(16))
    measurement_18 = Column(String(16))
    measurement_19 = Column(String(16))
    measurement_20 = Column(String(16))
    result         = Column(String(16)) 
    
    def __repr__(self):
        line1 = "Raw_Avgwt_Result(lot_number: %s)" % self.lot_number
        line2 = "Columns(result: %s)" % \
        (self.result)
        return line1 + "\n" + line2    

#-----------------------------------------------------------------------------#     

class Raw_Rancidity_Result(Base):
    __tablename__ = 'raw_rancidity_results'
    
    #identifiers
    id     = Column(Integer, primary_key=True)  
    lot    = relationship("Raw_Lot", uselist=False, back_populates='rancidity_result')
    lot_id = Column(Integer, ForeignKey('raw_lots.id'))
    #external data
    spec  = relationship("Raw_Lot_Spec_Rancidity", uselist=False,
                         lazy='joined', back_populates='result')
    tests = relationship("Raw_Rancidity_Test", back_populates='result')
    #results
    peroxide_result  = Column(String(16)) 
    anisidine_result = Column(String(16))
    oxidation_result = Column(String(16))
    
    def __repr__(self):
        line1 = "Raw_Rancidity_Result(lot_number: %s)" % self.lot_number
        line2 = "Columns(peroxide_result: %s, anisidine_result: %s, oxidation_result: %s)" % \
        (self.peroxide_result, self.anisidine_result, self.oxidation_result)
        return line1 + "\n" + line2 

#-----------------------------------------------------------------------------#    
  
class Raw_Lot_Spec_Chem_ID(Base):
    __tablename__ = 'raw_lot_spec_chem_id'
    
    #identifiers
    id        = Column(Integer, primary_key=True)
    result    = relationship("Raw_Chem_ID_Result", back_populates='spec')
    result_id = Column(Integer, ForeignKey('raw_chem_id_results.id'))
    #copied from the specification at creation
    name     = Column(String(64), ForeignKey('chem_id_names.name'))
    method   = Column(String(64))   
    presence = Column(Boolean)  
    
        
class Raw_Lot_Spec_Plant_ID(Base):
    __tablename__ = 'raw_lot_spec_plant_id'
    
    #identifiers
    id        = Column(Integer, primary_key=True)
    result    = relationship("Raw_Plant_ID_Result", back_populates='spec')
    result_id = Column(Integer, ForeignKey('raw_plant_id_results.id'))
    #copied from the specification at creation
    genus_species = Column(String(64))
    method    = Column(String(64))    
    part    = Column(String(64))
    solvent = Column(String(64))
    
class Raw_Lot_Spec_Assay(Base):
    __tablename__ = 'raw_lot_spec_assay'
    
    #identifiers
    id        = Column(Integer, primary_key=True)
    result    = relationship("Raw_Assay_Result", back_populates='spec')
    result_id = Column(Integer, ForeignKey('raw_assay_results.id'))
    #copied from the specification at creation
    name      = Column(String(64), ForeignKey('assay_names.name'))    
    method    = Column(String(64))    
    lower_bound = Column(String(16))
    upper_bound = Column(String(16))
    units       = Column(String(32))
    dry_basis   = Column(Boolean) 
    
class Raw_Lot_Spec_HM(Base):
    __tablename__ = 'raw_lot_spec_hm'
    
    #identifiers
    id        = Column(Integer, primary_key=True)
    result    = relationship("Raw_HM_Result", back_populates='spec')
    result_id = Column(Integer, ForeignKey('raw_hm_results.id'))
    #copied from the specification at creation
    units       = Column(String(32))
    arsenic_max = Column(String(16))
    cadmium_max = Column(String(16))
    lead_max    = Column(String(16))
    mercury_max = Column(String(16)) 
        
class Raw_Lot_Spec_Allergens(Base):
    __tablename__ = 'raw_lot_spec_allergens'
    
    #identifiers
    id        = Column(Integer, primary_key=True)
    result    = relationship("Raw_Allergens_Result", back_populates='spec')
    result_id = Column(Integer, ForeignKey('raw_allergens_results.id'))
    #copied from the specification at creation
    egg       = Column(Boolean)
    soy       = Column(Boolean)
    wheat     = Column(Boolean)
    fish      = Column(Boolean)
    milk      = Column(Boolean)
    treenut   = Column(Boolean)
    peanut    = Column(Boolean)
    shellfish = Column(Boolean)
    
class Raw_Lot_Spec_Pesticides(Base):
    __tablename__ = 'raw_lot_spec_pesticides'
    
    #identifiers
    id        = Column(Integer, primary_key=True)
    result    = relationship("Raw_Pesticides_Result", back_populates='spec')
    result_id = Column(Integer, ForeignKey('raw_pesticides_results.id'))
    #copied from the specification at creation
    standard = Column(String(32))    
    
class Raw_Lot_Spec_Organoleptics(Base):
    __tablename__ = 'raw_lot_spec_organoleptics'
    
    #identifiers
    id        = Column(Integer, primary_key=True)
    result    = relationship("Raw_Organoleptics_Result", back_populates='spec')
    result_id = Column(Integer, ForeignKey('raw_organoleptics_results.id'))
    #copied from the specification at creation
    color      = Column(String(64))
    odor       = Column(String(64))
    appearance = Column(String(64))
    
class Raw_Lot_Spec_Moisture(Base):
    __tablename__ = 'raw_lot_spec_moisture'
    
    #identifiers
    id          = Column(Integer, primary_key=True)
    result = relationship("Raw_Moisture_Result", back_populates='spec')
    result_id = Column(Integer, ForeignKey('raw_moisture_results.id'))
    
    lower_bound = Column(String(16))
    upper_bound = Column(String(16))
    
class Raw_Lot_Spec_Density(Base):
    __tablename__ = 'raw_lot_spec_density'
    
    #identifiers
    id        = Column(Integer, primary_key=True)
    result    = relationship("Raw_Density_Result", back_populates='spec')
    result_id = Column(Integer, ForeignKey('raw_density_results.id'))
    #copied from the specification at creation
    flow_min  = Column(String(16))
    flow_max  = Column(String(16))
    tap_min   = Column(String(16))
    tap_max   = Column(String(16))  
       
class Raw_Lot_Spec_Avgwt(Base):
    __tablename__ = 'raw_lot_spec_avgwt'
    
    #identifiers
    id        = Column(Integer, primary_key=True)
    result    = relationship("Raw_Avgwt_Result", back_populates='spec')
    result_id = Column(Integer, ForeignKey('raw_avgwt_results.id'))
    #copied from the specification at creation
    lower_bound = Column(String(16))
    upper_bound = Column(String(16)) 
    
class Raw_Lot_Spec_Microbes(Base):
    __tablename__ = 'raw_lot_spec_microbes'
    
    #identifiers
    id        = Column(Integer, primary_key=True)
    result    = relationship("Raw_Microbes_Result", back_populates='spec')
    result_id = Column(Integer, ForeignKey('raw_microbes_results.id'))
    #copied from the specification at creation
    tpc_min = Column(Integer)
    ym_min  = Column(Integer)
    tpc_max = Column(Integer)
    ym_max  = Column(Integer)
    
class Raw_Lot_Spec_Pathogens(Base):
    __tablename__ = 'raw_lot_spec_pathogens'
    
    #identifiers
    id        = Column(Integer, primary_key=True)
    result    = relationship("Raw_Pathogens_Result", back_populates='spec')
    result_id = Column(Integer, ForeignKey('raw_pathogens_results.id'))
    #copied from the specification at creation
    ecoli      = Column(Boolean)
    salmonella = Column(Boolean)
    staph      = Column(Boolean)
      
class Raw_Lot_Spec_Rancidity(Base):
    __tablename__ = 'raw_lot_spec_rancidity'
    
    #identifiers
    id        = Column(Integer, primary_key=True)
    result    = relationship("Raw_Rancidity_Result", back_populates='spec')
    result_id = Column(Integer, ForeignKey('raw_rancidity_results.id'))
    #copied from the specification at creation
    peroxide_max  = Column(String(16))
    anisidine_max = Column(String(16))
    oxidation_max = Column(String(16))
    
#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#

class Raw_Assay_Test(Base):
    __tablename__ = 'raw_assay_tests'
    
    #data
    id            = Column(Integer, primary_key=True)       
    po            = Column(Integer) 
    tracking      = Column(String(64))
    sent_date     = Column(Date)
    expected_date = Column(Date)
    result_date   = Column(Date)

    lab = relationship("Lab", back_populates='raw_assays_tested')    
    lab_id = Column(Integer, ForeignKey('labs.id'))
    
    result_id = Column(Integer, ForeignKey('raw_assay_results.id'))
    result = relationship("Raw_Assay_Result", uselist=False, back_populates='tests')
    
#-----------------------------------------------------------------------------#
    
class Raw_Chem_ID_Test(Base):
    __tablename__ = 'raw_chem_id_tests'
    
    #data
    id            = Column(Integer, primary_key=True)       
    po            = Column(Integer) 
    tracking      = Column(String(64))
    sent_date     = Column(Date)
    expected_date = Column(Date)
    result_date   = Column(Date)

    lab_id = Column(Integer, ForeignKey('labs.id'))
    lab = relationship("Lab", back_populates='raw_chem_ids_tested')    
    result_id = Column(Integer, ForeignKey('raw_chem_id_results.id'))
    result = relationship("Raw_Chem_ID_Result", uselist=False, back_populates='tests')
    
#-----------------------------------------------------------------------------#

class Raw_Plant_ID_Test(Base):
    __tablename__ = 'raw_plant_id_tests'
    
    #data
    id            = Column(Integer, primary_key=True)       
    po            = Column(Integer) 
    tracking      = Column(String(64))
    sent_date     = Column(Date)
    expected_date = Column(Date)
    result_date   = Column(Date)

    lab_id = Column(Integer, ForeignKey('labs.id'))
    lab = relationship("Lab", back_populates='raw_plant_ids_tested')    
    result_id = Column(Integer, ForeignKey('raw_plant_id_results.id'))
    result = relationship("Raw_Plant_ID_Result", uselist=False, back_populates='tests')    
    
#-----------------------------------------------------------------------------#

class Raw_HM_Test(Base):
    __tablename__ = 'raw_hm_tests'
    
    #data
    id            = Column(Integer, primary_key=True)       
    po            = Column(Integer) 
    tracking      = Column(String(64))
    sent_date     = Column(Date)
    expected_date = Column(Date)
    result_date   = Column(Date)

    lab_id = Column(Integer, ForeignKey('labs.id'))
    lab = relationship("Lab", back_populates='raw_hms_tested')    
    result_id = Column(Integer, ForeignKey('raw_hm_results.id'))
    result = relationship("Raw_HM_Result", uselist=False, back_populates='tests')

#-----------------------------------------------------------------------------#

class Raw_Pesticides_Test(Base):
    __tablename__ = 'raw_pesticides_tests'
    
    #data
    id            = Column(Integer, primary_key=True)       
    po            = Column(Integer) 
    tracking      = Column(String(64))
    sent_date     = Column(Date)
    expected_date = Column(Date)
    result_date   = Column(Date)

    lab_id = Column(Integer, ForeignKey('labs.id'))
    lab = relationship("Lab", back_populates='raw_pesticides_tested')    
    result_id = Column(Integer, ForeignKey('raw_pesticides_results.id'))
    result = relationship("Raw_Pesticides_Result", uselist=False, back_populates='tests')

#-----------------------------------------------------------------------------#

class Raw_Allergens_Test(Base):
    __tablename__ = 'raw_allergens_tests'
    
    #data
    id            = Column(Integer, primary_key=True)       
    po            = Column(Integer) 
    tracking      = Column(String(64))
    sent_date     = Column(Date)
    expected_date = Column(Date)
    result_date   = Column(Date)

    lab_id = Column(Integer, ForeignKey('labs.id'))
    lab = relationship("Lab", back_populates='raw_allergens_tested')    
    result_id = Column(Integer, ForeignKey('raw_allergens_results.id'))
    result = relationship("Raw_Allergens_Result", uselist=False, back_populates='tests')
 
#-----------------------------------------------------------------------------#
    
class Raw_Microbes_Test(Base):
    __tablename__ = 'raw_microbes_tests'
    
    #data
    id            = Column(Integer, primary_key=True)       
    po            = Column(Integer) 
    tracking      = Column(String(64))
    sent_date     = Column(Date)
    expected_date = Column(Date)
    result_date   = Column(Date)

    lab_id = Column(Integer, ForeignKey('labs.id'))
    lab = relationship("Lab", back_populates='raw_microbes_tested')    
    result_id = Column(Integer, ForeignKey('raw_microbes_results.id'))
    result = relationship("Raw_Microbes_Result", uselist=False, back_populates='tests')

#-----------------------------------------------------------------------------#

class Raw_Pathogens_Test(Base):
    __tablename__ = 'raw_pathogens_tests'
    
    #data
    id            = Column(Integer, primary_key=True)       
    po            = Column(Integer) 
    tracking      = Column(String(64))
    sent_date     = Column(Date)
    expected_date = Column(Date)
    result_date   = Column(Date)

    lab_id = Column(Integer, ForeignKey('labs.id'))
    lab = relationship("Lab", back_populates='raw_pathogens_tested')    
    result_id = Column(Integer, ForeignKey('raw_pathogens_results.id'))
    result = relationship("Raw_Pathogens_Result", uselist=False, back_populates='tests')    
 
#-----------------------------------------------------------------------------#    
    
class Raw_Organoleptics_Test(Base):
    __tablename__ = 'raw_organoleptics_tests'
    
    #data
    id            = Column(Integer, primary_key=True)       
    po            = Column(Integer) 
    tracking      = Column(String(64))
    sent_date     = Column(Date)
    expected_date = Column(Date)
    result_date   = Column(Date)

    lab_id = Column(Integer, ForeignKey('labs.id'))
    lab = relationship("Lab", back_populates='raw_organoleptics_tested')    
    result_id = Column(Integer, ForeignKey('raw_organoleptics_results.id'))
    result = relationship("Raw_Organoleptics_Result", uselist=False, back_populates='tests')
 
#-----------------------------------------------------------------------------#    
    
class Raw_Density_Test(Base):
    __tablename__ = 'raw_density_tests'
    
    #data
    id            = Column(Integer, primary_key=True)       
    po            = Column(Integer) 
    tracking      = Column(String(64))
    sent_date     = Column(Date)
    expected_date = Column(Date)
    result_date   = Column(Date)

    lab_id = Column(Integer, ForeignKey('labs.id'))
    lab = relationship("Lab", back_populates='raw_densities_tested')    
    result_id = Column(Integer, ForeignKey('raw_density_results.id'))
    result = relationship("Raw_Density_Result", uselist=False, back_populates='tests')

#-----------------------------------------------------------------------------#

class Raw_Moisture_Test(Base):
    __tablename__ = 'raw_moisture_tests'
    
    #data
    id            = Column(Integer, primary_key=True)       
    po            = Column(Integer) 
    tracking      = Column(String(64))
    sent_date     = Column(Date)
    expected_date = Column(Date)
    result_date   = Column(Date)

    lab_id = Column(Integer, ForeignKey('labs.id'))
    lab = relationship("Lab", back_populates='raw_moistures_tested')    
    result_id = Column(Integer, ForeignKey('raw_moisture_results.id'))
    result = relationship("Raw_Moisture_Result", uselist=False, back_populates='tests')

#-----------------------------------------------------------------------------#
    
class Raw_Avgwt_Test(Base):
    __tablename__ = 'raw_avgwt_tests'
    
    #data
    id            = Column(Integer, primary_key=True)       
    po            = Column(Integer) 
    tracking      = Column(String(64))
    sent_date     = Column(Date)
    expected_date = Column(Date)
    result_date   = Column(Date)

    lab_id = Column(Integer, ForeignKey('labs.id'))
    lab = relationship("Lab", back_populates='raw_avgwts_tested')    
    result_id = Column(Integer, ForeignKey('raw_avgwt_results.id'))
    result = relationship("Raw_Avgwt_Result", uselist=False, back_populates='tests')

#-----------------------------------------------------------------------------#

class Raw_Rancidity_Test(Base):
    __tablename__ = 'raw_rancidity_tests'
    
    #data
    id            = Column(Integer, primary_key=True)       
    po            = Column(Integer) 
    tracking      = Column(String(64))
    sent_date     = Column(Date)
    expected_date = Column(Date)
    result_date   = Column(Date)

    lab_id = Column(Integer, ForeignKey('labs.id'))
    lab = relationship("Lab", back_populates='raw_rancidities_tested')    
    result_id = Column(Integer, ForeignKey('raw_rancidity_results.id'))
    result = relationship("Raw_Rancidity_Result", uselist=False, back_populates='tests')