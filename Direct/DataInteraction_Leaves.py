from Declarative_Common import Assay_Name, Chem_ID_Name

from Declarative_RawItems import Raw_Allergens, Raw_HM, Raw_Microbes
from Declarative_RawItems import Raw_Pathogens, Raw_Organoleptics, Raw_Density
from Declarative_RawItems import Raw_Moisture, Raw_Avgwt, Raw_Chem_ID
from Declarative_RawItems import Raw_Plant_ID, Raw_Assay, Raw_Rancidity
from Declarative_RawItems import Raw_Pesticides

from Declarative_RawLots import Raw_Chem_ID_Result, Raw_Plant_ID_Result, Raw_Assay_Result
from Declarative_RawLots import Raw_HM_Result, Raw_Allergens_Result, Raw_Pesticides_Result
from Declarative_RawLots import Raw_Organoleptics_Result, Raw_Moisture_Result, Raw_Density_Result
from Declarative_RawLots import Raw_Avgwt_Result, Raw_Microbes_Result, Raw_Pathogens_Result
from Declarative_RawLots import Raw_Rancidity_Result, Raw_Lot_Location, Raw_Lot_Receiving_Data
from Declarative_RawLots import Raw_Lot_Sage_Data
from Declarative_RawLots import Raw_Lot_Spec_Chem_ID, Raw_Lot_Spec_Plant_ID, Raw_Lot_Spec_Assay
from Declarative_RawLots import Raw_Lot_Spec_HM, Raw_Lot_Spec_Allergens, Raw_Lot_Spec_Pesticides
from Declarative_RawLots import Raw_Lot_Spec_Organoleptics, Raw_Lot_Spec_Moisture
from Declarative_RawLots import Raw_Lot_Spec_Density, Raw_Lot_Spec_Avgwt, Raw_Lot_Spec_Microbes
from Declarative_RawLots import Raw_Lot_Spec_Pathogens, Raw_Lot_Spec_Rancidity

#from DataInteraction_Bases import Interactive_RawLot
from DataInteraction_Trunk import OTOSpec, OTMSpec, OTMSpec_Singlet
from DataInteraction_Trunk import OTOLotData, OTOResult, OTMResult, OTMResult_Singlet

#-----------------------------------------------------------------------------#

class RangeText:
    def __init__(self, lower_bound = None, upper_bound = None, units = None):
        self.low = lower_bound
        self.low_text = ''
        self.high = upper_bound
        self.high_text = ''
        self.units = units
        self.units_text = ''
        self.range_text = ''
        self.range_good = True
        self.check_range()
        self.make_range_text()
    
    def check_range(self):
        if self.low is not None and self.high is not None:
            if self.low >= self.high:
                self.range_good = False
        
    def make_range_text(self):
        if self.range_good:
            if self.units is not None:
                self.units_text = ' ' + str(self.units)
            if self.low is not None and self.high is not None:
                self.low_text = str(self.low)
                self.high_text = str(self.high)
                self.range_text = \
                self.low_text + ' - ' + self.high_text + self.units_text
            elif self.low is not None and self.high is None:
                self.low_text = str(self.low)
                self.range_text = \
                '> ' + self.low_text + self.units_text
            elif self.low is None and self.high is not None:
                self.high_text = str(self.high)
                self.range_text = \
                '< ' + self.high_text + self.units_text
            else:
                self.range_text = 'N/A'
        else:
            self.range_text = "Bad Range"

#-----------------------------------------------------------------------------#
#Name conformance classes-----------------------------------------------------#
#-----------------------------------------------------------------------------#

class Assay_Names:
    def __init__(self):
        self.names = []
    def get_names(self, session):
        self.names = []
        names = session.query(Assay_Name.name).all()
        for name in names:
            self.names.append(name[0])
    def add_name(self, session, name):
        session.add(Assay_Name(name = name))
        session.commit()
        
class Chem_Names:
    def __init__(self):
        self.names = []
    def get_names(self, session):
        self.names = []
        names = session.query(Chem_ID_Name.name).all()
        for name in names:
            self.names.append(name[0])
    def add_name(self, session, name):
        session.add(Chem_ID_Name(name = name))
        session.commit()
          
def update_name_list(session, names_class, name):
    namelist = names_class()
    namelist.get_names(session)
    names = namelist.names
    if name not in names:
        namelist.add_name(session, name)


#-------------------------------------------------------------------------------#
#Raw Item Interactive Items-----------------------------------------------------#
#-------------------------------------------------------------------------------#

#OTMSpec Children################################################################
            
class Interactive_RawPlantIDs(OTMSpec):
    def __init__(self):
        super().__init__(Raw_Plant_ID, Interactive_RawPlantID, 'genus_species') 

    def update_singlets(self):
        for key, singlet in self.specific.items():
            singlet.select_item_number(self.item_number)
            singlet.select_name(key)

###
     
class Interactive_RawChemIDs(OTMSpec):
    def __init__(self):
        super().__init__(Raw_Chem_ID, Interactive_RawChemID, 'name')

    def update_singlets(self):
        for key, singlet in self.specific.items():
            singlet.select_item_number(self.item_number)
            singlet.select_name(key)
            
###

class Interactive_RawAssays(OTMSpec):
    def __init__(self):
        super().__init__(Raw_Assay, Interactive_RawAssay, 'name')
        
    def update_singlets(self):
        for key, singlet in self.specific.items():
            singlet.select_item_number(self.item_number)
            singlet.select_name(key)

#OTMSpec_Singlet Children########################################################

class Interactive_RawChemID(OTMSpec_Singlet):
    def __init__(self):
        super().__init__(Raw_Chem_ID)
        self.identifier_is_called = 'chemical name'
        self.update_attributes = ['name', 'method', 'presence']
        self.data_access_dict.update({'name': self.identifier})  
    
    def select_name(self, new_name):
        self.identifier = new_name
        self.data_access_dict['name'] = new_name
        
    def presence_string(self):
        pres_str = ""
        if self.data is not None:
            if self.data.presence:
                pres_str = "Positive"
            else:
                pres_str = "Negative"
        else:
            pres_str = "No Spec"
        return pres_str
   
###
             
class Interactive_RawPlantID(OTMSpec_Singlet):
    def __init__(self):
        super().__init__(Raw_Plant_ID)
        self.identifier_is_called = 'genus and species'
        self.update_attributes = ['genus_species', 'method',
                                  'part', 'solvent']
        self.data_access_dict.update({'genus_species': self.identifier})
        
    def select_name(self, new_name):
        self.identifier = new_name
        self.data_access_dict['genus_species'] = new_name

    def genus_string(self):
        g_string = ""
        if self.data is not None:
            if self.data.genus_species is not None:
                genus,species = self.data.genus_species.split(' ')
                g_string = genus
        return g_string
        
    def species_string(self):
        s_string = ""
        if self.data is not None:
            if self.data.genus_species is not None:
                genus,species = self.data.genus_species.split(' ')
                s_string = species
        return s_string

###
         
class Interactive_RawAssay(OTMSpec_Singlet):
    def __init__(self):
        super().__init__(Raw_Assay)
        self.identifier_is_called = 'assay name'
        self.update_attributes = ['name', 'method',
                                  'lower_bound', 'upper_bound',
                                  'units', 'dry_basis']
        self.data_access_dict.update({'name': self.identifier})

    def select_name(self, new_name):
        self.identifier = new_name
        self.data_access_dict['name'] = new_name

    def dry_basis_string(self):
        db_string = "Unknown"
        if self.data is not None:
            if self.data.dry_basis:
                db_string = "Yes"
            else:
                db_string = "No"
        return db_string
       
    def assay_range(self):
        if self.data is not None:
            assy_rng = RangeText(self.data.lower_bound,
                                 self.data.upper_bound, self.data.units)
            return assy_rng.range_text
        else:
            return 'N/A'
            
#OTOSpec Children################################################################

class Interactive_RawHM(OTOSpec):
    def __init__(self):
        super().__init__(Raw_HM)
        self.update_attributes = ['units', 'arsenic_max',
                                  'cadmium_max', 'lead_max',
                                  'mercury_max']

###

class Interactive_RawAllergens(OTOSpec):
    def __init__(self):
        super().__init__(Raw_Allergens)
        self.update_attributes = ['egg', 'soy',
                                  'wheat', 'fish',
                                  'milk', 'treenut',
                                  'peanut', 'shellfish']
    
    def allergen_string(self):
        if self.data is None:
            return "None"
        else:
            allergens = ['egg', 'soy', 'wheat', 'fish',
             'milk', 'treenut', 'peanut', 'shellfish']
            string_list = []
            for allergen in allergens:
                current = getattr(self.data, allergen)
                if current:
                    string_list.append(allergen.capitalize())
            allergen_string = ', '.join(string_list)
            if allergen_string == '':
                allergen_string = "None."
            return allergen_string
            
###   
     
class Interactive_RawPesticides(OTOSpec):
    def __init__(self):
        super().__init__(Raw_Pesticides)
        self.update_attributes = ['standard']
            
###      
            
class Interactive_RawOrganoleptics(OTOSpec):
    def __init__(self):
        super().__init__(Raw_Organoleptics)
        self.update_attributes = ['color', 'odor', 'appearance']          
            
###

class Interactive_RawMoisture(OTOSpec):
    def __init__(self):
        super().__init__(Raw_Moisture)
        self.update_attributes = ['lower_bound', 'upper_bound']
    
    def moisture_range(self):
        if self.data is not None:
            mois_range = RangeText(self.data.lower_bound, self.data.upper_bound, '%')
            return mois_range.range_text
        else:
            return "N/A"
        
### 
           
class Interactive_RawDensity(OTOSpec):
    def __init__(self):
        super().__init__(Raw_Density)
        self.update_attributes = ['flow_min', 'flow_max',
                                  'tap_min', 'tap_max']
    
    def flow_range(self):
        if self.data is not None:
            flow_rng = RangeText(self.data.flow_min, self.data.flow_max, 'g/mL')
            return flow_rng.range_text
        else:
            return 'N/A'
        
    def tap_range(self):
        if self.data is not None:
            tap_rng = RangeText(self.data.tap_min, self.data.tap_max, 'g/mL')
            return tap_rng.range_text
        else:
            return 'N/A'
        
###

class Interactive_RawAvgwt(OTOSpec):
    def __init__(self):
        super().__init__(Raw_Avgwt)
        self.update_attributes = ['lower_bound', 'upper_bound']
            
    def avgwt_range(self):
        if self.data is not None:
            wt_rng = RangeText(self.data.lower_bound, self.data.upper_bound, 'grams')
            return wt_rng.range_text
        else:
            return 'N/A'
        
###
    
class Interactive_RawMicrobes(OTOSpec):
    def __init__(self):
        super().__init__(Raw_Microbes)
        self.update_attributes = ['tpc_min', 'tpc_max',
                                  'ym_min', 'ym_max']
            
    def tpc_range(self):
        if self.data is not None:
            tpc_rng = RangeText(self.data.tpc_min, self.data.tpc_max, 'CFU/g')
            return tpc_rng.range_text
        else:
            return 'N/A'
        
    def ym_range(self):
        if self.data is not None:
            ym_rng = RangeText(self.data.ym_min, self.data.ym_max, 'CFU/g')
            return ym_rng.range_text
        else:
            return 'N/A'
        
###  
      
class Interactive_RawPathogens(OTOSpec):
    def __init__(self):
        super().__init__(Raw_Pathogens)
        self.update_attributes = ['ecoli', 'salmonella', 'staph']
    
    def status_text(self, patho):
        status_text = ""
        if self.data is not None:
            pathogen = getattr(self.data, patho)
            if pathogen is None:
                status_text = "Not Tested"
            elif not pathogen:
                status_text = "Negative"
            else:
                status_text = "Positive"
        else:
            status_text = "Not Tested"
        return status_text        
    
    def ecoli_status_string(self):
        return self.status_text('ecoli')
        
    def salmonella_status_string(self):
        return self.status_text('salmonella')
           
    def staph_status_string(self):
        return self.status_text('staph')     
                   
###        

class Interactive_RawRancidity(OTOSpec):
    def __init__(self):
        super().__init__(Raw_Rancidity)
        self.update_attributes = ['peroxide_max', 'anisidine_max',
                                  'oxidation_max']
        
#-------------------------------------------------------------------------------#
#Raw Lot Interactive Items------------------------------------------------------#
#-------------------------------------------------------------------------------#

#OTOLotData Children#############################################################

class Interactive_RawLocation(OTOLotData):
    def __init__(self):
        super().__init__(Raw_Lot_Location)
        self.update_attributes = ['facility', 'wh_code']

###
        
class Interactive_RawSageData(OTOLotData):
    def __init__(self):
        super().__init__(Raw_Lot_Sage_Data)
        self.update_attributes = ['total_amount', 'amount_in_a',
                                  'amount_in_r', 'amount_in_q',
                                  'amount_in_ac']

###
        
class Interactive_RawReceiving(OTOLotData):
    def __init__(self):
        super().__init__(Raw_Lot_Receiving_Data)
        self.update_attributes = ['po', 'date', 'amount']
        
    def date_string(self):
        dat_str = "Unknown"
        if self.data is not None and self.data.date is not None:
            dat_str = self.data.date.strftime('%m/%d/%y')
        return dat_str
    
    def amount_string(self):
        amt_str = "Unknown"
        if self.data is not None and self.data.amount is not None:
            amt_str = str(self.data.amount)
            if self.data.lot.units is not None:
                amt_str += " "
                amt_str += str(self.data.lot.units)
        return amt_str        

#OTOResult Children #############################################################

class Interactive_RawHMResult(OTOResult):
    def __init__(self):
        super().__init__(Raw_HM_Result, Raw_Lot_Spec_HM)
        self.update_attributes = ['arsenic_result', 'cadmium_result',
                                  'lead_result', 'mercury_result']
        self.spec_update_attributes = ['units', 'arsenic_max', 'cadmium_max',
                                       'lead_max', 'mercury_max']

    def arsenic_result_string(self):
        arsenic = 'No result'
        if self.data is None:
            arsenic = 'Not tested'
        elif self.data is not None and self.data.arsenic_result is not None:
            arsenic = str(self.data.arsenic_result)
        return arsenic
    def cadmium_result_string(self):
        cadmium = 'No result'
        if self.data is None:
            cadmium = 'Not tested'
        elif self.data is not None and self.data.cadmium_result is not None:
            cadmium = str(self.data.cadmium_result)
        return cadmium    
    def lead_result_string(self):
        lead = 'No result'
        if self.data is None:
            lead = 'Not tested'
        elif self.data is not None and self.data.lead_result is not None:
            lead = str(self.data.lead_result)
        return lead
    def mercury_result_string(self):
        mercury = 'No result'
        if self.data is None:
            mercury = 'Not tested'
        elif self.data is not None and self.data.mercury_result is not None:
            mercury = str(self.data.mercury_result)
        return mercury    
###

class Interactive_RawAllergensResult(OTOResult):
    def __init__(self):
        super().__init__(Raw_Allergens_Result, Raw_Lot_Spec_Allergens)
        self.update_attributes = ['egg_result', 'soy_result',
                                  'wheat_result', 'fish_result',
                                  'milk_result', 'treenut_result',
                                  'peanut_result', 'shellfish_result'] 
        self.spec_update_attributes = ['egg', 'soy', 'fish', 'wheat',
                                       'peanut', 'treenut', 'shellfish', 'milk']             

###
            
class Interactive_RawPesticidesResult(OTOResult):
    def __init__(self):
        super().__init__(Raw_Pesticides_Result, Raw_Lot_Spec_Pesticides)
        self.update_attributes = ['result']
        self.spec_update_attributes = ['standard']

    def standard_string(self):
        stdstr = 'No standard'
        if self.data is not None:
            if self.data.spec is not None:
                if self.data.spec.standard is not None:
                    stdstr = str(self.data.spec.standard)
        return stdstr
        
    def result_string(self):        
        resstr = 'No result'
        if self.data is None:
            resstr = 'Not tested'
        elif self.data is not None and self.data.result is not None:
            resstr = str(self.data.result)
        return resstr
###
            
class Interactive_RawOrganolepticsResult(OTOResult):
    def __init__(self):
        super().__init__(Raw_Organoleptics_Result,
                         Raw_Lot_Spec_Organoleptics)
        self.update_attributes = ['color_result', 'odor_result',
                                  'appearance_result']
        self.spec_update_attributes = ['color', 'odor', 'appearance']

###

class Interactive_RawMoistureResult(OTOResult):
    def __init__(self):
        super().__init__(Raw_Moisture_Result, Raw_Lot_Spec_Moisture)
        self.update_attributes = ['result']
        self.spec_update_attributes = ['lower_bound', 'upper_bound']

###

class Interactive_RawDensityResult(OTOResult):
    def __init__(self):
        super().__init__(Raw_Density_Result, Raw_Lot_Spec_Density)
        self.update_attributes = ['flow_result', 'tap_result']
        self.spec_update_attributes = ['flow_min', 'flow_max',
                                       'tap_min', 'tap_max']            

###

class Interactive_RawAvgwtResult(OTOResult):
    def __init__(self):
        super().__init__(Raw_Avgwt_Result, Raw_Lot_Spec_Avgwt)
        self.update_attributes = ['result', 'measurement01',
                                  'measurement02', 'measurement03',
                                  'measurement04', 'measurement05',
                                  'measurement06', 'measurement07',
                                  'measurement08', 'measurement09',
                                  'measurement10', 'measurement11',
                                  'measurement12', 'measurement13',
                                  'measurement14', 'measurement15',
                                  'measurement16', 'measurement17',
                                  'measurement18', 'measurement19',
                                  'measurement20']
        self.spec_update_attributes = ['lower_bound', 'upper_bound']

###

class Interactive_RawMicrobesResult(OTOResult):
    def __init__(self):
        super().__init__(Raw_Microbes_Result, Raw_Lot_Spec_Microbes)
        self.update_attributes = ['tpc_result', 'ym_result']
        self.spec_update_attributes = ['tpc_min', 'tpc_max',
                                       'ym_min', 'ym_max']
        
    def tpc_result_string(self):
        tpc = 'No result'
        if self.data is None:
            tpc = 'Not tested'
        elif self.data is not None and self.data.tpc_result is not None:
            tpc = str(self.data.tpc_result)
        return tpc
    def ym_result_string(self):
        ym = 'No result'
        if self.data is None:
            ym = 'Not tested'
        elif self.data is not None and self.data.ym_result is not None:
            ym = str(self.data.ym_result)
        return ym

###
            
class Interactive_RawPathogensResult(OTOResult):
    def __init__(self):
        super().__init__(Raw_Pathogens_Result, Raw_Lot_Spec_Pathogens)
        self.update_attributes = ['ecoli_result', 'salmonella_result',
                                  'staph_result']
        self.spec_update_attributes = ['ecoli', 'salmonella', 'staph']          

    def ecoli_result_string(self):
        ecoli = 'No result'
        if self.data is not None and self.data.ecoli_result is not None:
            ecoli = str(self.data.ecoli_result)
        return ecoli
    def salmonella_result_string(self):
        salmonella = 'No result'
        if self.data is not None and self.data.salmonella_result is not None:
            salmonella = str(self.data.salmonella_result)
        return salmonella
    def staph_result_string(self):
        staph = 'No result'
        if self.data is not None and self.data.staph_result is not None:
            staph = str(self.data.staph_result)
        return staph

###
            
class Interactive_RawRancidityResult(OTOResult):
    def __init__(self):
        super().__init__(Raw_Rancidity_Result, Raw_Lot_Spec_Rancidity)
        self.update_attributes = ['peroxide_result',
                                  'anisidine_result',
                                  'oxidation_result']
        self.spec_update_attributes = ['peroxide_max',
                                       'anisidine_max',
                                       'oxidation_max']


#OTMResult_Singlet Children #####################################################

class Interactive_RawPlantIDResult(OTMResult_Singlet):
    def __init__(self):
        super().__init__(Raw_Plant_ID_Result, Raw_Lot_Spec_Plant_ID)
        self.update_attributes = ['result']
        self.spec_update_attributes = ['genus_species', 'method',
                                       'solvent', 'part']

    def genus_string(self):
        g_string = ""
        if self.data is not None and self.data.spec is not None:
            if self.data.spec.genus_species is not None:
                genus,species = self.data.spec.genus_species.split(' ')
                g_string = genus
        return g_string
        
    def species_string(self):
        s_string = ""
        if self.data is not None and self.data.spec is not None:
            if self.data.spec.genus_species is not None:
                genus,species = self.data.spec.genus_species.split(' ')
                s_string = species
        return s_string

###

class Interactive_RawChemIDResult(OTMResult_Singlet):
    def __init__(self):
        super().__init__(Raw_Chem_ID_Result, Raw_Lot_Spec_Chem_ID)
        self.update_attributes = ['result']
        self.spec_update_attributes = ['name', 'method', 'presence']

    def presence_string(self):
        if self.data is not None and self.data.spec is not None:
            if self.data.spec.presence is None:
                return "No presence spec"
            elif self.data.spec.presence:
                return "Positive"
            else:
                return "Negative"

###

class Interactive_RawAssayResult(OTMResult_Singlet):
    def __init__(self):
        super().__init__(Raw_Assay_Result, Raw_Lot_Spec_Assay)
        self.update_attributes = ['result']
        self.spec_update_attributes = ['name', 'method',
                                       'lower_bound', 'upper_bound',
                                       'dry_basis', 'units']
        
    def assay_range(self):
        if self.data is not None and self.data.spec is not None:
            assy_rng = RangeText(self.data.spec.lower_bound,
                                 self.data.spec.upper_bound,
                                 self.data.spec.units)
            return assy_rng.range_text
        else:
            return 'N/A'

#OTMResult Children #############################################################

class Interactive_RawPlantIDResults(OTMResult):
    def __init__(self):
        super().__init__(Raw_Plant_ID_Result, Interactive_RawPlantIDResult, 'id')

###
            
class Interactive_RawChemIDResults(OTMResult):
    def __init__(self):
        super().__init__(Raw_Chem_ID_Result, Interactive_RawChemIDResult, 'id')    

###
                
class Interactive_RawAssayResults(OTMResult):
    def __init__(self):
        super().__init__(Raw_Assay_Result, Interactive_RawAssayResult, 'id')