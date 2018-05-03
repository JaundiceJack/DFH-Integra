from PyQt5.QtWidgets import QTableWidgetItem, QListWidgetItem
from InterfaceElements import Label, Table, PlainText, List

class Display:
    def __init__(self, user_interface):
        self.lot_display = LotInterfaces(user_interface)
        self.item_display = ItemInterfaces(user_interface)
        
    def display_item(self, item):
        self.item_display.clear_all()
        self.item_display.show_all(item)


class LotInterfaces(Display):
    def __init__(self, user_interface):
        self.ui = user_interface
        self.classify_interfaces()
        
    def classify_interfaces(self):
        self.displays = \
        {'lot_number':       Label(self.ui.il_lot_numberL),
         'vendor':           Label(self.ui.il_vendorL),
         'vendor_lot':       Label(self.ui.il_vendor_lotL),
         'lot_note':         PlainText(self.ui.il_lot_notePT),
         'delay_note':       PlainText(self.ui.il_lot_delayPT),
         'expected_release': Label(self.ui.il_expected_dateL,
                             none_msg = 'Unknown'),
         'actual_release':   Label(self.ui.il_final_dateL,
                             none_msg = 'Not yet released'),
         'amount':           Label(self.ui.il_amount_recL),
         'date':             Label(self.ui.il_date_recL,
                             none_msg = 'Unknown'),
         'po':               Label(self.ui.il_rec_poL,
                             none_msg = 'Unknown'),
         'facility':         Label(self.ui.il_facilityL),
         'warehouse':        Label(self.ui.il_wh_codeL),
         'assays':           List(self.ui.il_assay_resultList),
         'spec':             Label(self.ui.il_assay_specL),
         'result':           Label(self.ui.il_assay_resultL,
                             none_msg = "No result yet")}
        self.buttons = \
        {'edit_lot': "not yet implemented"}
                  
    def clear_display(self):
        for key, display in self.displays:
            display.fill_with(None)


class Display:
    """Display handles presenting information on the screen's user interface.
    Most of its methods display some part of an Item object."""
    def __init__(self, user_interface):
        self.ui = user_interface
        self.classify_interfaces()
        
    def classify_interfaces(self):
        ####################################################
        self.basic_display = \
        {'item_number': Label(self.ui.is_item_numberL,
                        none_msg = "Item not found."),
         'name'       : Label(self.ui.is_item_nameL),
         'fridge'     : Label(self.ui.is_fridgeL),
         'note'       : PlainText(self.ui.is_item_notePT)}
        ####################################################
        self.allergens_display = Label(self.ui.is_allergensL,
                                 none_msg = "None")
        ####################################################
        self.pesticides_display = Label(self.ui.is_pesticideL,
                                  none_msg = "No Spec")
        ####################################################
        self.hm_display = \
        {'arsenic': Label(self.ui.is_as_maxL,
                    none_msg = "N/A"),
         'cadmium': Label(self.ui.is_cd_maxL,
                    none_msg = "N/A"),
         'lead':    Label(self.ui.is_pb_maxL,
                    none_msg = "N/A"),
         'mercury': Label(self.ui.is_hg_maxL,
                    none_msg = "N/A"),
         'arsenic_units': Label(self.ui.is_as_unitL),
         'cadmium_units': Label(self.ui.is_cd_unitL),
         'lead_units':    Label(self.ui.is_pb_unitL),
         'mercury_units': Label(self.ui.is_hg_unitL),}
        ####################################################
        self.organo_display = \
        {'color':      Label(self.ui.is_colorL,
                       none_msg = "N/A"),
         'odor':       Label(self.ui.is_odorL,
                       none_msg = "N/A"),
         'appearance': Label(self.ui.is_appearanceL,
                       none_msg = "N/A")}        
        ####################################################
        self.density_display = \
        {'flow': Label(self.ui.is_flow_densityL,
                 none_msg = "N/A"),
         'tap':  Label(self.ui.is_tap_densityL,
                 none_msg = "N/A")}
        #################################################### 
        self.avgwt_display = Label(self.ui.is_avgwtL,
                             none_msg = "N/A")
        ####################################################
        self.moisture_display = Label(self.ui.is_moistureL,
                                none_msg = "N/A")
        ####################################################
        self.microbes_display = \
        {'tpc': Label(self.ui.is_tpcL,
                none_msg = "N/A"),
        'ym':   Label(self.ui.is_ymL,
                none_msg = "N/A")}
        ####################################################
        self.pathogens_display = \
        {'ecoli':      Label(self.ui.is_ecoliL,
                       none_msg = "Not Tested."),
         'salmonella': Label(self.ui.is_salmonellaL,
                       none_msg = "Not Tested."),
         'staph':      Label(self.ui.is_staphL,
                       none_msg = "Not Tested.")}
        ####################################################
        self.assay_display = \
        {'assays':    List(self.ui.is_assayList),
         'spec':      Label(self.ui.is_assay_specL),
         'method':    Label(self.ui.is_assay_methodL),
         'dry_basis': Label(self.ui.is_dbL)}
        ####################################################
        self.chem_display = \
        {'chems':    List(self.ui.is_chemList),
         'method':   Label(self.ui.is_chem_methodL),
         'presence': Label(self.ui.is_chem_presenceL)}
        ####################################################
        self.plant_display = \
        {'plants':  List(self.ui.is_plantList),
         'part':    Label(self.ui.is_plant_partL),
         'solvent': Label(self.ui.is_plant_solventL),
         'method':  Label(self.ui.is_plant_methodL)}
        ####################################################
        self.lot_display = List(self.ui.il_lotList)
        ####################################################
        self.lot_basics_display = \
        {'lot_number': Label(self.ui.il_lot_numberL),
         'vendor':     Label(self.ui.il_vendorL),
         'vendor_lot': Label(self.ui.il_vendor_lotL),
         'lot_note':   PlainText(self.ui.il_lot_notePT),
         'delay_note': PlainText(self.ui.il_lot_delayPT),
         'expected':   Label(self.ui.il_expected_dateL,
                             none_msg = 'Unknown'),
         'actual':     Label(self.ui.il_final_dateL,
                             none_msg = 'Not yet released')}
        ####################################################
        self.lot_receiving_display = \
        {'amount': Label(self.ui.il_amount_recL),
         'date':   Label(self.ui.il_date_recL,
                         none_msg = 'Unknown'),
         'po':     Label(self.ui.il_rec_poL,
                         none_msg = 'Unknown')}
        ####################################################
        self.lot_location_display = \
        {'facility':  Label(self.ui.il_facilityL),
         'warehouse': Label(self.ui.il_wh_codeL)}
        ####################################################
        self.lot_assay_display = \
        {'assays': List(self.ui.il_assay_resultList),
         'spec':   Label(self.ui.il_assay_specL),
         'result': Label(self.ui.il_assay_resultL,
                         none_msg = "No result yet")}
        ####################################################
        self.lot_chem_id_display = \
        {'chem_ids': List(self.ui.il_chem_id_resultList),
         'spec':     Label(self.ui.il_chem_id_specL),
         'result':   Label(self.ui.il_chem_id_resultL,
                           none_msg = 'No result yet.')}
        ####################################################
        self.lot_plant_display = \
        {'plants': Table(self.ui.il_plant_id_resultTable),
         'spec' :  Label(self.ui.il_plant_id_specL),
         'result': Label(self.ui.il_plant_id_resultL,
                         none_msg = 'No result yet.')}
        ####################################################
        self.lot_micro_display = \
        {'micro': Table(self.ui.il_microTable)}
        ####################################################
        self.lot_hm_display = \
        {'hm': Table(self.ui.il_hmTable)}
        ####################################################
        self.lot_pest_display = \
        {'table': Table(self.ui.il_pesticideTable)}
        ####################################################
    
    def show_item(self, item):
        self.run_item_displays(item)
        self.disable_item_entry()
        self.enable_assay_entry(item.assays)
        self.enable_chem_entry(item.chem_ids)
        self.enable_plant_entry(item.plant_ids)
        self.enable_other_button_entry(item)
    
    def show_lot(self, lot):
        self.run_lot_displays(lot)
    
    def run_item_displays(self, item):
        self.display_basic(item)
        self.display_chem_ids(item.chem_ids)
        self.display_plant_ids(item.plant_ids)
        self.display_assays(item.assays)        
        self.display_allergens(item.allergens)
        self.display_organoleptics(item.organoleptics)
        self.display_moisture(item.moisture)
        self.display_density(item.density)
        self.display_avgwt(item.avgwt)
        self.display_microbes(item.microbes)
        self.display_pathogens(item.pathogens)
        self.display_heavy_metals(item.hm)
        self.display_pesticides(item.pesticides)
        self.display_lots(item.lots)
    
    def run_lot_displays(self, lot):
        self.display_lot_basic(lot)
        self.display_lot_receiving(lot.receiving)
        self.display_lot_location(lot.location)
        self.display_lot_assays(lot.assay_results)
        self.display_lot_chems(lot.chem_id_results)
        self.display_lot_plants(lot.plant_id_results)
        self.display_lot_micros(lot.microbes_result, lot.pathogens_result)
        self.display_lot_hm(lot.hm_result)
        self.display_lot_pesticides(lot.pesticides_result)
    
    def disable_item_entry(self):
        pass
        """
        self.ui.is_edit_hmB.setEnabled(False)
        self.ui.is_edit_microbeB.setEnabled(False)
        self.ui.is_edit_organolepticB.setEnabled(False)
        self.ui.is_edit_physicalB.setEnabled(False)
        self.ui.is_edit_pesticideB.setEnabled(False)
        self.ui.is_edit_basicB.setEnabled(False)
        #new
        self.ui.is_new_chem_idB.setEnabled(False)
        self.ui.is_new_plant_idB.setEnabled(False)
        self.ui.is_new_assayB.setEnabled(False)
        #edit
        self.ui.is_edit_chem_idB.setEnabled(False)
        self.ui.is_edit_plant_idB.setEnabled(False)
        self.ui.is_edit_assayB.setEnabled(False)
        #remove
        self.ui.is_remove_chem_idB.setEnabled(False)
        self.ui.is_remove_plant_idB.setEnabled(False)
        self.ui.is_remove_assayB.setEnabled(False)
        """
 
    #TODO for these functions, place a search_found variable in Interactive_RawItem
    #enable or disable these according to if it was found in the SearchButton
    #sequester the table functions in that class
    def enable_assay_entry(self, assays):
        pass
        """
        if assays.data is not None:
            self.ui.is_new_assayB.setEnabled(True)
            selected_assay = self.ui.is_assayTable.currentRow()
            if selected_assay != -1:                
                self.ui.is_edit_assayB.setEnabled(True)
                self.ui.is_remove_assayB.setEnabled(True)
        """
        
    def enable_chem_entry(self, chem_ids):
        pass
        """
        if chem_ids.data is not None:
            self.ui.is_new_chem_idB.setEnabled(True)
            selected_chem = self.ui.is_chem_idTable.currentRow()
            if selected_chem != -1:
                self.ui.is_edit_chem_idB.setEnabled(True)
                self.ui.is_remove_chem_idB.setEnabled(True)
        """
    
    def enable_plant_entry(self, plant_ids):
        pass
        """
        if plant_ids.data is not None:
            self.ui.is_new_plant_idB.setEnabled(True)
            selected_plant = self.ui.is_plant_idTable.currentRow()
            if selected_plant != -1:
                self.ui.is_edit_plant_idB.setEnabled(True)
                self.ui.is_remove_plant_idB.setEnabled(True)
        """
    
    def enable_other_button_entry(self, item):
        pass
        """
        if item.data is not None:
            self.ui.is_edit_hmB.setEnabled(True)
            self.ui.is_edit_microbeB.setEnabled(True)
            self.ui.is_edit_organolepticB.setEnabled(True)
            self.ui.is_edit_physicalB.setEnabled(True)
            self.ui.is_edit_pesticideB.setEnabled(True)
            self.ui.is_edit_basicB.setEnabled(True)
        """    

    def blank_all(self, interface_dict):
        for key, item in interface_dict.items():
            item.fill_with(None)
    
    #def display_basic(self, basic_data, basic_displays *args):
    #    if basic_data is not None:
    #        for display in basic_displays:
    #            filler = getattr(basic_data, arg)
    #            display.fill_with(filler)
    
    def display_basic(self, basic):
        if basic is not None and basic.data is not None:
            self.basic_display['item_number'].fill_with(basic.data.id)
            self.basic_display['name'].       fill_with(basic.data.name)
            self.basic_display['fridge'].     fill_with(basic.fridge_string())
            self.basic_display['note'].       fill_with(basic.data.note)       
        else:
            self.blank_all(self.basic_display)
    
    def display_allergens(self, allergens):
        if allergens.data is not None:
            self.allergens_display.fill_with(allergens.allergen_string())
        else:
            self.allergens_display.fill_with(None)       
            
    def display_pesticides(self, pesticides):
        if pesticides.data is not None:
            self.pesticides_display.fill_with(pesticides.data.standard)
        else:
            self.pesticides_display.fill_with(None)

    def display_heavy_metals(self, heavy_metals):
        if heavy_metals.data is not None:
            self.hm_display['arsenic'].fill_with(heavy_metals.data.arsenic_max)
            self.hm_display['cadmium'].fill_with(heavy_metals.data.cadmium_max)
            self.hm_display['lead'].fill_with(heavy_metals.data.lead_max)
            self.hm_display['mercury'].fill_with(heavy_metals.data.mercury_max)
            self.hm_display['arsenic_units'].fill_with(heavy_metals.data.units)
            self.hm_display['cadmium_units'].fill_with(heavy_metals.data.units)
            self.hm_display['lead_units'].fill_with(heavy_metals.data.units)
            self.hm_display['mercury_units'].fill_with(heavy_metals.data.units)
        else:
            self.blank_all(self.hm_display)
            
    def display_organoleptics(self, organoleptics):
        if organoleptics.data is not None:
            self.organo_display['color'].\
            fill_with(organoleptics.data.color)
            self.organo_display['odor'].\
            fill_with(organoleptics.data.odor)
            self.organo_display['appearance'].\
            fill_with(organoleptics.data.appearance)
        else:
            self.blank_all(self.organo_display)         

    def display_density(self, density):
        if density.data is not None:
            self.density_display['flow'].fill_with(density.flow_range())
            self.density_display['tap'].fill_with(density.tap_range())
        else:
            self.blank_all(self.density_display)
        
    def display_moisture(self, moisture):
        if moisture.data is not None:
            self.moisture_display.fill_with(moisture.moisture_range())
        else:
            self.moisture_display.fill_with(None)
        
    def display_avgwt(self, avgwt):
        if avgwt is not None:
            self.avgwt_display.fill_with(avgwt.avgwt_range())
        else:
            self.avgwt_display.fill_with(None)

    def display_microbes(self, microbes):
        if microbes.data is not None:
            self.microbes_display['tpc'].fill_with(microbes.tpc_range())
            self.microbes_display['ym'].fill_with(microbes.ym_range())
        else:
            self.blank_all(self.microbes_display)
        
    def display_pathogens(self, pathogens):
        if pathogens.data is not None:
            self.pathogens_display['ecoli'].\
            fill_with(pathogens.ecoli_status_string())
            self.pathogens_display['salmonella'].\
            fill_with(pathogens.salmonella_status_string())
            self.pathogens_display['staph'].\
            fill_with(pathogens.staph_status_string())
        else:
            self.blank_all(self.pathogens_display)

    def display_assays(self, assays):
        if assays.data is not None:
            self.assay_display['assays'].clear()
            for key, assay in assays.specific.items():
                self.assay_display['assays'].fill_with(key)
        else:
            self.blank_all(self.assay_display)

    def assay_selected(self, assays):
        key = self.assay_display['assays'].current_item()
        if key is not None:
            self.assay_display['spec'].fill_with(assays.specific[key].assay_range())
            self.assay_display['method'].fill_with(assays.specific[key].data.method)
            self.assay_display['dry_basis'].fill_with(assays.specific[key].dry_basis_string())

    def display_chem_ids(self, chem_ids):
        if chem_ids.data is not None:
            self.chem_display['chems'].clear()
            for key, chem in chem_ids.specific.items():
                self.chem_display['chems'].fill_with(key)
        else:
            self.blank_all(self.chem_display)

    def chem_selected(self, chem_ids):
        key = self.chem_display['chems'].current_item()
        if key is not None:
            self.chem_display['method'].fill_with(chem_ids.specific[key].data.method)
            self.chem_display['presence'].fill_with(chem_ids.specific[key].presence_string())

    def display_plant_ids(self, plant_ids):
        if plant_ids.data is not None:
            self.plant_display['plants'].clear()
            for key, plant in plant_ids.specific.items():
                self.plant_display['plants'].fill_with(key)
        else:
            self.blank_all(self.plant_display)

    def plant_selected(self, plant_ids):
        key = self.plant_display['plants'].current_item()
        if key is not None:
            self.plant_display['part'].fill_with(plant_ids.specific[key].data.part)
            self.plant_display['solvent'].fill_with(plant_ids.specific[key].data.solvent)
            self.plant_display['method'].fill_with(plant_ids.specific[key].data.method)
                    
    def display_lots(self, lots):
        if lots is not None and lots.data is not None:
            self.lot_display.clear()
            for key, lot in lots.specific.items():
                self.lot_display.fill_with(key)

                                                        
    #display these only when a lot is selected
    def display_lot_basic(self, basics):
        if basics.data is not None:
            self.lot_basics_display['lot_number'].\
            fill_with(basics.data.lot_number)
            self.lot_basics_display['vendor'].\
            fill_with(basics.data.vendor)
            self.lot_basics_display['vendor_lot'].\
            fill_with(basics.data.vendor_lot)
            self.lot_basics_display['lot_note'].\
            fill_with(basics.data.lot_note)
            self.lot_basics_display['delay_note'].\
            fill_with(basics.data.delay_note)
            self.lot_basics_display['expected'].\
            fill_with(basics.data.expected_release_date)
            self.lot_basics_display['actual'].\
            fill_with(basics.data.actual_release_date)
        else:
            self.blank_all(self.lot_basics_display)
            
    def display_lot_receiving(self, receiving):
        if receiving.data is not None:
            self.lot_receiving_display['amount'].\
            fill_with(receiving.amount_string())
            self.lot_receiving_display['date'].\
            fill_with(receiving.date_string())
            self.lot_receiving_display['po'].\
            fill_with(receiving.data.po)
        else:
            self.blank_all(self.lot_receiving_display)
            
    def display_lot_location(self, location):
        if location.data is not None:
            self.lot_location_display['facility'].\
            fill_with(location.data.facility)
            self.lot_location_display['warehouse'].\
            fill_with(location.data.wh_code)
        else:
            self.blank_all(self.lot_location_display)

    def display_lot_plants(self, plant_ids):
        self.lot_plant_display['plants'].clear()
        if plant_ids.specific:
            for result_id, result in plant_ids.specific.items():
                if result.data is not None and result.data.spec is not None:
                    self.lot_plant_display['plants'].\
                    fill_with(result.genus_string(), result.species_string())
        self.lot_plant_display['spec'].fill_with('Select plant ID')
        self.lot_plant_display['result'].fill_with('Select plant ID')
 
    def lot_plant_id_selected(self, plant_ids, plant_name):
        for result_id, plant_result in plant_ids.specific.items():
            if plant_result.data is not None \
            and plant_result.data.spec is not None \
            and plant_result.data.spec.genus_species == plant_name:
                self.lot_plant_display['spec'].\
                fill_with("Positive")
                self.lot_plant_display['result'].\
                fill_with(plant_result.data.result)
                break
        else:
            print("Warning: No spec for %s plant ID found." % plant_name)

    def display_lot_assays(self, assays):
        self.lot_assay_display['assays'].clear()
        if assays.specific:
            print("had an assay")
            for result_id, result in assays.specific.items():
                if result.data is not None and result.data.spec is not None:
                    self.lot_assay_display['assays'].\
                    fill_with(result.data.spec.name)
        else:
            print("did no have an assay")
        self.lot_assay_display['spec'].fill_with("Select assay")
        self.lot_assay_display['result'].fill_with("Select assay")
                    
    
    def lot_assay_selected(self, assays, assay_name):
        for result_id, assay_result in assays.specific.items():
            if assay_result.data is not None \
            and assay_result.data.spec is not None \
            and assay_result.data.spec.name == assay_name:
                self.lot_assay_display['spec'].\
                fill_with(assay_result.assay_range())
                self.lot_assay_display['result'].\
                fill_with(assay_result.data.result)
                break
        else:
            print("Warning: No spec for %s assay found." % assay_name)

    def display_lot_chems(self, chem_ids):
        self.lot_chem_id_display['chem_ids'].clear()
        if chem_ids.specific:
            for result_id, result in chem_ids.specific.items():
                if result.data.spec is not None:
                    self.lot_chem_id_display['chem_ids'].\
                    fill_with(result.data.spec.name)
        self.lot_chem_id_display['spec'].\
        fill_with("Select chem ID")
        self.lot_chem_id_display['result'].\
        fill_with("Select chem ID")
        
    def lot_chem_id_selected(self, chem_ids, chem_name):
        for result_id, chem_result in chem_ids.specific.items():
            if chem_result.data is not None \
            and chem_result.data.spec is not None \
            and chem_result.data.spec.name == chem_name:
                self.lot_chem_id_display['spec'].\
                fill_with(chem_result.presence_string())
                self.lot_chem_id_display['result'].\
                fill_with(chem_result.data.result)
                break
        else:
            print("Warning: No spec for %s ID found." % chem_name)            

    def display_lot_micros(self, microbes_result, pathogens_result):
        self.lot_micro_display['micro'].table.clearContents()
        self.lot_micro_display['micro'].\
        fill_vertical(microbes_result.tpc_result_string(),
                      microbes_result.ym_result_string())
        self.lot_micro_display['micro'].\
        fill_vertical(pathogens_result.ecoli_result_string(),
                      pathogens_result.salmonella_result_string(),
                      pathogens_result.staph_result_string(),
                      start_row = 2)
        
    def display_lot_hm(self, hm_result):
        self.lot_hm_display['hm'].table.clearContents()
        self.lot_hm_display['hm'].\
        fill_vertical(hm_result.arsenic_result_string(),
                      hm_result.cadmium_result_string(),
                      hm_result.lead_result_string(),
                      hm_result.mercury_result_string())
    
    def display_lot_pesticides(self, pesticides_result):
        self.lot_pest_display['table'].table.clearContents()
        self.lot_pest_display['table'].\
        fill_vertical(pesticides_result.standard_string(),
                      pesticides_result.result_string())