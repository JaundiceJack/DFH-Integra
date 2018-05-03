from DataInteraction_Leaves import *

from DataInteraction_Trunk import Basis
from DataInteraction_Trunk import OTMSpec

from Declarative_RawItems import Raw_Item
from Declarative_RawLots import Raw_Lot
from SessionOpener import OpenSession  

class Interactive_RawItem(Basis):
    def __init__(self):
        super().__init__(Raw_Item)
        self.item_number = None
        self.update_attributes = ['name', 'note', 'fridge']
        self.data_access_dict.update({'id': self.item_number})
        
        self.lots      = Interactive_RawLots()
        self.assays    = Interactive_RawAssays()
        self.chem_ids  = Interactive_RawChemIDs()
        self.plant_ids = Interactive_RawPlantIDs()
        
        self.hm            = Interactive_RawHM()
        self.pesticides    = Interactive_RawPesticides()
        self.allergens     = Interactive_RawAllergens()
        self.organoleptics = Interactive_RawOrganoleptics()
        self.moisture      = Interactive_RawMoisture()
        self.density       = Interactive_RawDensity()
        self.avgwt         = Interactive_RawAvgwt()
        self.microbes      = Interactive_RawMicrobes()
        self.pathogens     = Interactive_RawPathogens()
        self.rancidity     = Interactive_RawRancidity()

    def select_item_number(self, new_item_number):
        """update the item number for all associations and run a query"""
        self.item_number = new_item_number
        self.data_access_dict['id'] = new_item_number
        self.lots.         select_item_number(self.item_number)
        self.assays.       select_item_number(self.item_number)
        self.chem_ids.     select_item_number(self.item_number)
        self.plant_ids.    select_item_number(self.item_number)
        self.hm.           select_item_number(self.item_number)
        self.pesticides.   select_item_number(self.item_number)
        self.allergens.    select_item_number(self.item_number)
        self.organoleptics.select_item_number(self.item_number)
        self.moisture.     select_item_number(self.item_number)
        self.density.      select_item_number(self.item_number)
        self.avgwt.        select_item_number(self.item_number)
        self.microbes.     select_item_number(self.item_number)
        self.pathogens.    select_item_number(self.item_number)
        self.rancidity.    select_item_number(self.item_number)
        with OpenSession() as session:
            self.query(session)
        
    def update_relations(self, session):
        self.lots.         query(session)
        self.assays.       query(session)      
        self.chem_ids.     query(session)
        self.plant_ids.    query(session)       
        self.hm.           query(session)
        self.pesticides.   query(session)
        self.allergens.    query(session)
        self.organoleptics.query(session)
        self.moisture.     query(session)        
        self.density.      query(session)        
        self.avgwt.        query(session)
        self.microbes.     query(session)
        self.pathogens.    query(session)   
        self.rancidity.    query(session)

    def has_ids(self, func_name):
        has_item_number = False
        if self.item_number is not None:
            has_item_number = True
        else:
            print("No item number provided to %s %s." % \
                  (func_name, self.table_class.__name__))
        return has_item_number
    
    def access(self, session):
        if self.has_ids('access'):
            return self.basis_access(session)
        else:
            return False
    
    def fridge_string(self):
        cold_string = ""
        if self.data is not None:
            if self.data.fridge:
                cold_string = "Yes"
            else:
                cold_string = "No"
        else:
            cold_string = "No Spec"
        return cold_string

    def update(self, session, **updates):
        if self.has_ids('update') and self.access(session):
            self.basis_update(session, **updates)           
    
    def query(self, session):
        if self.has_ids('query'):
            self.basis_query(session)
            self.update_relations(session)
    
    def new(self, session):
        if self.has_ids('create new') and not self.access(session):
            self.basis_new(session)
            self.update_relations(session)
    
    def remove(self, session):
        """remove the item and all associated specifications"""
        if self.has_ids('remove') and self.access(session):          
            self.lots.remove(session)
            self.assays.remove(session)
            self.chem_ids.remove(session)
            self.plant_ids.remove(session)
            self.hm.remove(session)
            self.pesticides.remove(session)
            self.allergens.remove(session)
            self.organoleptics.remove(session)
            self.moisture.remove(session)
            self.density.remove(session)
            self.avgwt.remove(session)
            self.microbes.remove(session)
            self.pathogens.remove(session)
            self.rancidity.remove(session)
            self.basis_remove(session)

class Interactive_RawLots(OTMSpec):
    def __init__(self):
        super().__init__(Raw_Lot, Interactive_RawLot, 'lot_number')

    def update_singlets(self):
        for key, singlet in self.specific.items():
            singlet.select_lot(self.item_number, key)

    def new(self, session, item, lot_number):
        if self.has_ids('create new'):
            lot_key = self.otm_new(session,
                         item_id = self.item_number,
                         lot_number = lot_number)
            self.update_singlets()
            self.specific[lot_key].generate_new(session, item)   
            return lot_key

class Interactive_RawLot(Basis):
    def __init__(self):
        super().__init__(Raw_Lot)
        self.item_number = None
        self.lot_number = None
        self.update_attributes = ['units', 'vendor', 'vendor_lot',
                                  'expected_release_date', 'actual_release_date',
                                  'lot_note', 'delay_note']
        self.data_access_dict.update({'item_id': self.item_number})
        self.data_access_dict.update({'lot_number': self.lot_number})

        self.location  = Interactive_RawLocation()
        self.receiving = Interactive_RawReceiving()
        self.sage_data = Interactive_RawSageData()
        
        self.chem_id_results  = Interactive_RawChemIDResults()
        self.plant_id_results = Interactive_RawPlantIDResults()
        self.assay_results    = Interactive_RawAssayResults()
        
        self.hm_result            = Interactive_RawHMResult()
        self.allergens_result     = Interactive_RawAllergensResult()
        self.pesticides_result    = Interactive_RawPesticidesResult()
        self.organoleptics_result = Interactive_RawOrganolepticsResult()  
        self.moisture_result      = Interactive_RawMoistureResult()
        self.density_result       = Interactive_RawDensityResult()
        self.avgwt_result         = Interactive_RawAvgwtResult()
        self.microbes_result      = Interactive_RawMicrobesResult()
        self.pathogens_result     = Interactive_RawPathogensResult()
        self.rancidity_result     = Interactive_RawRancidityResult()
        
    def select_lot(self, new_item_number, new_lot_number):
        """update the lot number for all associations and run a query"""
        self.item_number = new_item_number
        self.data_access_dict['item_id'] = new_item_number
        self.lot_number = new_lot_number
        self.data_access_dict['lot_number'] = new_lot_number
        with OpenSession() as session:
            self.basis_query(session)
        
        #sequester this in a function to check ids
        new_lot_id = self.data.id
        self.location.            select_item_number(new_item_number)
        self.receiving.           select_item_number(new_item_number)
        self.sage_data.           select_item_number(new_item_number)
        self.chem_id_results.     select_item_number(new_item_number)
        self.plant_id_results.    select_item_number(new_item_number)
        self.assay_results.       select_item_number(new_item_number)
        self.hm_result.           select_item_number(new_item_number)
        self.allergens_result.    select_item_number(new_item_number)
        self.pesticides_result.   select_item_number(new_item_number)
        self.organoleptics_result.select_item_number(new_item_number)
        self.moisture_result.     select_item_number(new_item_number)
        self.density_result.      select_item_number(new_item_number)
        self.avgwt_result.        select_item_number(new_item_number)
        self.microbes_result.     select_item_number(new_item_number)
        self.pathogens_result.    select_item_number(new_item_number)
        self.rancidity_result.    select_item_number(new_item_number)
        self.location.            select_lot_id(new_lot_id)
        self.receiving.           select_lot_id(new_lot_id)
        self.sage_data.           select_lot_id(new_lot_id)
        self.chem_id_results.     select_lot_id(new_lot_id)
        self.plant_id_results.    select_lot_id(new_lot_id)
        self.assay_results.       select_lot_id(new_lot_id)
        self.hm_result.           select_lot_id(new_lot_id)
        self.allergens_result.    select_lot_id(new_lot_id)
        self.pesticides_result.   select_lot_id(new_lot_id)
        self.organoleptics_result.select_lot_id(new_lot_id)
        self.moisture_result.     select_lot_id(new_lot_id)
        self.density_result.      select_lot_id(new_lot_id)
        self.avgwt_result.        select_lot_id(new_lot_id)
        self.microbes_result.     select_lot_id(new_lot_id)
        self.pathogens_result.    select_lot_id(new_lot_id)
        self.rancidity_result.    select_lot_id(new_lot_id)

    
    def update_relations(self, session):
        self.location.            query(session)
        self.receiving.           query(session)
        self.sage_data.           query(session)
        self.chem_id_results.     query(session)
        self.plant_id_results.    query(session)        
        self.assay_results.       query(session)     
        self.hm_result.           query(session)  
        self.allergens_result.    query(session)
        self.pesticides_result.   query(session) 
        self.organoleptics_result.query(session)          
        self.moisture_result.     query(session)
        self.density_result.      query(session)
        self.avgwt_result.        query(session)        
        self.microbes_result.     query(session)   
        self.pathogens_result.    query(session)       
        self.rancidity_result.    query(session)
 
    def generate_new(self, session, item):
        generator = LotGenerator(self.item_number, self.data.id)
        generator.gen_hm(session,        item.hm,        self.hm_result)
        generator.gen_assays(session,    item.assays,    self.assay_results)
        generator.gen_chem_ids(session,  item.chem_ids,  self.chem_id_results)
        generator.gen_plant_ids(session, item.plant_ids, self.plant_id_results)
        generator.gen_allergens(session, item.allergens, self.allergens_result)
        generator.gen_pesticides(session,item.pesticides,self.pesticides_result)
        generator.gen_organoleptics(session, item.organoleptics, self.organoleptics_result)
        generator.gen_moisture(session,  item.moisture,  self.moisture_result)
        generator.gen_density(session,   item.density,   self.density_result)
        generator.gen_avgwt(session,     item.avgwt,     self.avgwt_result)
        generator.gen_microbes(session,  item.microbes,  self.microbes_result)
        generator.gen_pathogens(session, item.pathogens, self.pathogens_result)
        generator.gen_rancidity(session, item.rancidity, self.rancidity_result)

    def has_ids(self, func_name):
        has_item_number = False
        has_lot_number = False
        if self.item_number is not None:
            has_item_number = True
        else:
            print("No item number provided to %s %s." % \
                  (func_name, self.table_class.__name__))
        if self.lot_number is not None:
            has_lot_number = True
        else:
            print("No lot number provided to %s %s." % \
                  (func_name, self.table_class.__name__))
        return has_item_number and has_lot_number
    
    def access(self, session):
        if self.has_ids('access'):
            return self.basis_access(session)
        else:
            return False
        
    def update(self, session, **updates):
        if self.has_ids('update') and self.access(session):
            self.basis_update(session, **updates) 
            
    def query(self, session):
        if self.has_ids('query'):
            self.basis_query(session)
            self.update_relations(session)
    
    def new(self, session, item):
        if self.has_ids('create new'): #and not self.access(session):
            self.basis_new(session)
            self.update_relations(session)
            #self.query(session)
            self.generate_new(session, item)
    
    def remove(self, session):
        """Remove the lot and all associated results and data."""
        if self.has_ids('remove') and self.access(session):           
            self.location.            remove(session)
            self.receiving.           remove(session)
            self.sage_data.           remove(session)
            self.chem_id_results.     remove(session)
            self.plant_id_results.    remove(session)        
            self.assay_results.       remove(session)     
            self.hm_result.           remove(session)  
            self.allergens_result.    remove(session)
            self.pesticides_result.   remove(session) 
            self.organoleptics_result.remove(session)          
            self.moisture_result.     remove(session)
            self.density_result.      remove(session)
            self.avgwt_result.        remove(session)        
            self.microbes_result.     remove(session)   
            self.pathogens_result.    remove(session)       
            self.rancidity_result.    remove(session)
            self.basis_remove(session)
        
class LotGenerator:
    def __init__(self, item_number, lot_id):
        self.item_number = item_number
        self.lot_id = lot_id
    
    def has_spec_data(self, spec):
        """Make sure there is a specification for the given property"""
        return spec.data is not None
   
    def gen_assays(self, session, assay_specs, assay_results):
        for name, assay_spec in assay_specs.specific.items():
            if assay_spec is not None:
                result_id = assay_results.new(session)
                assay_results.specific[result_id].select_item_number(self.item_number)
                assay_results.specific[result_id].select_lot_id(self.lot_id)
                if result_id != "" and result_id != "not generated":
                    assay_results.specific[result_id].select_result_id(result_id)
                    assay_results.specific[result_id].new_spec(session)                    
                    assay_results.specific[result_id].update_spec(session,
                                name        = assay_spec.data.name,    
                                method      = assay_spec.data.method,    
                                lower_bound = assay_spec.data.lower_bound,  
                                upper_bound = assay_spec.data.upper_bound,  
                                units       = assay_spec.data.units,  
                                dry_basis   = assay_spec.data.dry_basis)
                    
    def gen_chem_ids(self, session, chem_specs, chem_results):
        for name, chem_spec in chem_specs.specific.items():
            if self.has_spec_data(session, chem_spec):
                result_id = chem_results.new(session)
                chem_results.specific[result_id].select_item_number(self.item_number)
                chem_results.specific[result_id].select_lot_id(self.lot_id)
                if result_id != "" and result_id != 'not generated':
                    chem_results.specific[result_id].select_result_id(result_id)
                    chem_results.specific[result_id].new_spec(session)                   
                    chem_results.specific[result_id].update_spec(session,
                                         name = chem_spec.data.name,
                                         method = chem_spec.data.method,
                                         presence = chem_spec.data.presence)
                    
    def gen_plant_ids(self, session, plant_specs, plant_results):
        for name, plant_spec in plant_specs.specific.items():
            if self.has_spec_data(session, plant_spec):
                result_id = plant_results.new(session)
                plant_results.specific[result_id].select_item_number(self.item_number)
                plant_results.specific[result_id].select_lot_id(self.lot_id)
                if result_id != "" and result_id != "not generated":
                    plant_results.specific[result_id].select_result_id(result_id)
                    plant_results.specific[result_id].new_spec(session)                   
                    plant_results.specific[result_id].update_spec(session,
                                          genus_species = plant_spec.data.genus_species,
                                          method = plant_spec.data.method,
                                          solvent = plant_spec.data.solvent,
                                          part = plant_spec.data.part)


    def gen_(self, session, spec, result):
        if spec.data is not None:
            result.select_item_number(self.item_number)
            result.select_lot_id(self.lot_id)
            result.new(session)
            result.new_spec(session)
            return True
        else:
            return False
    
    def gen_hm(self, session, hm_spec, hm_result):
        if self.gen_(session, hm_spec, hm_result):
            hm_result.update_spec(session,
                                  units       = hm_spec.data.units,
                                  arsenic_max = hm_spec.data.arsenic_max,
                                  cadmium_max = hm_spec.data.cadmium_max,
                                  lead_max    = hm_spec.data.lead_max,
                                  mercury_max = hm_spec.data.mercury_max)
            
    def gen_allergens(self, session, allergens_spec, allergen_result):
        if self.gen_(session, allergens_spec, allergen_result):
            allergen_result.update_spec(session,
                                        egg       = allergens_spec.data.egg,
                                        soy       = allergens_spec.data.soy,
                                        wheat     = allergens_spec.data.wheat,
                                        fish      = allergens_spec.data.fish,
                                        milk      = allergens_spec.data.milk,
                                        treenut   = allergens_spec.data.treenut,
                                        peanut    = allergens_spec.data.peanut,
                                        shellfish = allergens_spec.data.shellfish)
    
    def gen_pesticides(self, session, pesticides_spec, pesticides_result):
        if self.gen_(session, pesticides_spec, pesticides_result):
            pesticides_result.update_spec(session,
                                          standard = pesticides_spec.data.standard)        
            
    def gen_organoleptics(self, session, organo_spec, organo_result):
        if self.gen_(session, organo_spec, organo_result):
            organo_result.update_spec(session,
                                      color = organo_spec.data.color,
                                      odor = organo_spec.data.odor,
                                      appearance = organo_spec.data.appearance)
            
    def gen_moisture(self, session, mois_spec, mois_result):
        if self.gen_(session, mois_spec, mois_result):
            mois_result.update_spec(session,
                                    lower_bound = mois_spec.data.lower_bound,
                                    upper_bound = mois_spec.data.upper_bound)
            
    def gen_density(self, session, dens_spec, dens_result):
        if self.gen_(session, dens_spec, dens_result):
            dens_result.update_spec(session,
                                    flow_min = dens_spec.data.flow_min,
                                    flow_max = dens_spec.data.flow_max,
                                    tap_min = dens_spec.data.tap_min,
                                    tap_max = dens_spec.data.tap_max)
            
    def gen_avgwt(self, session, wt_spec, wt_result):
        if self.gen_(session, wt_spec, wt_result):
            wt_result.update_spec(session,
                                  lower_bound = wt_spec.data.lower_bound,
                                  upper_bound = wt_spec.data.upper_bound)
    
    def gen_microbes(self, session, microbe_spec, microbe_result):
        if self.gen_(session, microbe_spec, microbe_result):
            microbe_result.update_spec(session,
                                       tpc_min = microbe_spec.data.tpc_min,
                                       tpc_max = microbe_spec.data.tpc_max,
                                       ym_min = microbe_spec.data.ym_min,
                                       ym_max = microbe_spec.data.ym_max)
    
    def gen_pathogens(self, session, pathogen_spec, pathogen_result):
        if self.gen_(session, pathogen_spec, pathogen_result):
            pathogen_result.update_spec(session,
                                        ecoli = pathogen_spec.data.ecoli,
                                        salmonella = pathogen_spec.data.salmonella,
                                        staph = pathogen_spec.data.staph)
            
    def gen_rancidity(self, session, ranc_spec, ranc_result):
        if self.gen_(session, ranc_spec, ranc_result):
            ranc_result.update_spec(session,
                                    peroxide_max  = ranc_spec.data.peroxide_max,
                                    anisidine_max = ranc_spec.data.anisidine_max,
                                    oxidation_max = ranc_spec.data.oxidation_max)