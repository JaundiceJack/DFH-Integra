import datetime
from PyQt5.QtWidgets import QDialog, QDialogButtonBox

from interfaces.Dialog_NewItem import Ui_Dialog as new_item_ui
from interfaces.Dialog_NewLot import Ui_Dialog as new_lot_ui
from interfaces.Dialog_BasicSpec import Ui_Dialog as basic_spec_ui
from interfaces.Dialog_AssaySpec import Ui_Dialog as assay_spec_ui
from interfaces.Dialog_ChemSpec import Ui_Dialog as chem_spec_ui
from interfaces.Dialog_HMSpec import Ui_Dialog as hm_spec_ui
from interfaces.Dialog_MicroSpec import Ui_Dialog as micro_spec_ui
from interfaces.Dialog_OrganolepticSpec import Ui_Dialog as organoleptic_spec_ui
from interfaces.Dialog_PesticideSpec import Ui_Dialog as pesticide_spec_ui
from interfaces.Dialog_PhysicalSpec import Ui_Dialog as physical_spec_ui
from interfaces.Dialog_PlantSpec import Ui_Dialog as plant_spec_ui

from interfaces.Dialog_TextOnly import Ui_Dialog as textonly_ui

#from LotGeneration import NewLot
from InterfaceElements import LineEdit, ComboBox, CheckBox, PlainText
from DataInteraction_Leaves import Assay_Names, Chem_Names
from SessionOpener import OpenSession
#-----------------------------------------------------------------------------#

class SimpleDialog(QDialog):
    """BasicDialog sets up a dialog box with the supplied user interface.
    Extracts basic functionality into an inheritable class"""    
    def __init__(self, ui):
        #Run setup on the given user interface
        super().__init__()
        self.ui = ui
        self.ui.setupUi(self)
        #Connect the Ok and Cancel dialog buttons to accept or reject entries
        self.ui.acceptB.button(QDialogButtonBox.Ok).clicked.connect(self.ok_click)
        self.ui.acceptB.button(QDialogButtonBox.Cancel).clicked.connect(self.cancel_click)
        #Track whether the dialog's Ok button was pressed
        self.dialog_accepted = False

    def popup(self):
        """Show the popup and return True if accepted, False if canceled."""
        return self.exec_() == QDialog.Accepted

    def enable_ok(self):
        self.ui.acceptB.button(QDialogButtonBox.Ok).setEnabled(True)   
        
    def disable_ok(self):
        self.ui.acceptB.button(QDialogButtonBox.Ok).setEnabled(False)

    #connect dialog signals
    def ok_click(self):
        self.dialog_accepted = True
        self.accept()
    def cancel_click(self):
        self.reject()
     

#-----------------------------------------------------------------------------#

class TextDialog(SimpleDialog):
    def __init__(self, text = None):
        super().__init__(textonly_ui())
        self.text = text
        self.set_text()
        
    def set_text(self):
        if self.text is not None:
            self.ui.warningL.setText(self.text)
        
#-----------------------------------------------------------------------------#            

class NewLotDialog(SimpleDialog):
    def __init__(self):
        super().__init__(new_lot_ui())    
        self.label_entries()
        self.disable_ok() 
        self.basic_entries['lot_number'].line_edit.\
        textChanged.connect(self.validate_input)
        
    def label_entries(self):
        self.basic_entries = \
        {'item_id':    LineEdit(self.ui.item_numberLE),
         'lot_number': LineEdit(self.ui.lot_numberLE),
         'vendor':     LineEdit(self.ui.vendorLE),
         'vendor_lot': LineEdit(self.ui.vendor_lotLE),
         'lot_note':   PlainText(self.ui.lot_notePT),
         'units':      ComboBox(self.ui.lot_unitsCombo)}
        
        self.receiving_entries = \
        {'amount': LineEdit(self.ui.amount_receivedLE, restrict_to = 'float'),
         'po':     LineEdit(self.ui.receiving_poLE)}
        
        self.location_entries = \
        {'facility': ComboBox(self.ui.facilityCombo),
         'wh_code':  LineEdit(self.ui.wh_codeLE)}
        
  
    def validate_input(self):       
        if self.basic_entries['lot_number'].line_edit.text() != '':
            self.enable_ok()
        else:
            self.disable_ok()     

    def popup(self, item):
        self.fill_in_item_id(item)
        with OpenSession() as session:
            if self.exec_():
                self.create_from_input(session, item)

    def fill_in_item_id(self, item):
        self.basic_entries['item_id'].fill_with(item.item_number)

    def create_from_input(self, session, item):
        self.parse_input()
        self.new_lot(session, item)

    def parse_input(self):        
        for key,entry in self.basic_entries.items():
            entry.parse_input()            
        for key,entry in self.receiving_entries.items():
            entry.parse_input()
        for key,entry in self.location_entries.items():
            entry.parse_input()

    def new_lot(self, session, item):       
        new_lot = self.basic_entries['lot_number'].parsed_entry
        item.query(session)
        lot_key = item.lots.new(session, item, new_lot)
        item.lots.specific[lot_key].update(session,
            units      = self.basic_entries['units'].parsed_entry,
            vendor     = self.basic_entries['vendor'].parsed_entry,
            vendor_lot = self.basic_entries['vendor_lot'].parsed_entry,
            lot_note   = self.basic_entries['lot_note'].parsed_entry)
        
        item.lots.specific[lot_key].receiving.new(session)
        item.lots.specific[lot_key].receiving.update(session,
            po = self.receiving_entries['po'].parsed_entry,
            date = datetime.datetime.now(),
            amount = self.receiving_entries['amount'].parsed_entry)
        
        item.lots.specific[lot_key].location.new(session)
        item.lots.specific[lot_key].location.update(session,
            facility = self.location_entries['facility'].parsed_entry,
            wh_code = self.location_entries['wh_code'].parsed_entry)

#-----------------------------------------------------------------------------#

class NewItemDialog(SimpleDialog):
    def __init__(self):
        #set up the user interface
        super().__init__(new_item_ui())
        self.label_entries()
        self.set_hm_unit_display()       
        #disable the ok button until item number and name are entered
        self.ui.acceptB.button(QDialogButtonBox.Ok).setEnabled(False) 
        self.item_entries['id'].line_edit.\
        textChanged.connect(self.validate_input)
        self.item_entries['name'].line_edit.\
        textChanged.connect(self.validate_input)
        #update heavy metal unit display when different units are selected
        self.hm_entries['units'].combobox.\
        currentIndexChanged.connect(self.set_hm_unit_display) 
    
    def label_entries(self):
        self.item_entries = \
        {'id':     LineEdit(self.ui.is_item_numberLE, restrict_to = 'int'),
         'name':   LineEdit(self.ui.is_item_nameLE),
         'note':   PlainText(self.ui.is_item_notePT),
         'fridge': CheckBox(self.ui.is_fridgeCB)}
        
        self.allergen_entries = \
        {'egg':       CheckBox(self.ui.is_eggCB),
         'peanut':    CheckBox(self.ui.is_peanutCB),
         'soy':       CheckBox(self.ui.is_soyCB),
         'shellfish': CheckBox(self.ui.is_shellfishCB),
         'fish':      CheckBox(self.ui.is_fishCB),
         'wheat':     CheckBox(self.ui.is_wheatCB),
         'milk':      CheckBox(self.ui.is_milkCB),
         'treenut':   CheckBox(self.ui.is_treenutCB)}
        
        self.hm_entries = \
        {'units':       ComboBox(self.ui.is_unitCombo),
         'arsenic_max': LineEdit(self.ui.is_asLE, restrict_to = 'float'),
         'cadmium_max': LineEdit(self.ui.is_cdLE, restrict_to = 'float'),
         'lead_max':    LineEdit(self.ui.is_pbLE, restrict_to = 'float'),
         'mercury_max': LineEdit(self.ui.is_hgLE, restrict_to = 'float')}
        
        self.microbe_entries = \
        {'tpc_min': LineEdit(self.ui.is_tpc_minLE, restrict_to = 'int'),
         'tpc_max': LineEdit(self.ui.is_tpc_maxLE, restrict_to = 'int'),
         'ym_min':  LineEdit(self.ui.is_ym_minLE,  restrict_to = 'int'),
         'ym_max':  LineEdit(self.ui.is_ym_maxLE,  restrict_to = 'int')}
       
        self.pathogen_entries = \
        {'ecoli':      ComboBox(self.ui.is_ecoliCombo,
                                combo_type = 'true_false_none'),
         'salmonella': ComboBox(self.ui.is_salmonellaCombo,
                                combo_type = 'true_false_none'),
         'staph':      ComboBox(self.ui.is_staphCombo,
                                combo_type = 'true_false_none')}
        for key, patho in self.pathogen_entries.items():
            patho.set_true_false_indices(true_index = 2,
                                         false_index = 0,
                                         none_index = 1)

    #TODO make this pretty
    def validate_input(self):
        if self.item_entries['id'].line_edit.text() != '':
            try:
                item_number = int(self.item_entries['id'].line_edit.text())
                if item_number > 10000 and item_number < 20000 \
                and self.item_entries['name'].line_edit.text() != '':
                    self.enable_ok()
                else:
                    self.disable_ok()
            except ValueError:
                self.disable_ok()
            except Exception as ex:
                raise
        else:
            self.disable_ok()
                  
    def set_hm_unit_display(self):
        units = str(self.hm_entries['units'].combobox.currentText())
        self.ui.is_unitL1.setText(units)
        self.ui.is_unitL2.setText(units)
        self.ui.is_unitL3.setText(units)
        self.ui.is_unitL4.setText(units)
    
    def popup(self, item):
        if self.exec_():
            with OpenSession() as session:
                self.create_from_input(session, item)
    
    def create_from_input(self, session, item):
        self.parse_input()
        self.new_item(session, item)
        self.new_allergens(session, item)
        self.new_hm(session, item)
        self.new_microbes(session, item)
        self.new_pathogens(session, item)
    
    def parse_input(self):
        for key,entry in self.item_entries.items():
            entry.parse_input()
        for key,entry in self.allergen_entries.items():
            entry.parse_input()
        for key,entry in self.hm_entries.items():
            entry.parse_input()
        for key,entry in self.microbe_entries.items():
            entry.parse_input()
        for key,entry in self.pathogen_entries.items():
            entry.parse_input()
    
    def new_item(self, session, item):
        item.select_item_number(self.item_entries['id'].parsed_entry)
        item.new(session)
        item.query(session)
        item.update(session,
            name   = self.item_entries['name'].parsed_entry,
            note   = self.item_entries['note'].parsed_entry,
            fridge = self.item_entries['fridge'].parsed_entry)
    
    def new_allergens(self, session, item):
        item.allergens.new(session)
        item.allergens.update(session,
            egg       = self.allergen_entries['egg'].parsed_entry,
            soy       = self.allergen_entries['soy'].parsed_entry,
            peanut    = self.allergen_entries['peanut'].parsed_entry,
            wheat     = self.allergen_entries['wheat'].parsed_entry,
            milk      = self.allergen_entries['milk'].parsed_entry,
            shellfish = self.allergen_entries['shellfish'].parsed_entry,
            fish      = self.allergen_entries['fish'].parsed_entry,
            treenut   = self.allergen_entries['treenut'].parsed_entry)        

    def new_hm(self, session, item):
        item.hm.new(session)
        item.hm.update(session,
            units       = self.hm_entries['units'].parsed_entry,
            arsenic_max = self.hm_entries['arsenic_max'].parsed_entry,
            cadmium_max = self.hm_entries['cadmium_max'].parsed_entry,
            lead_max    = self.hm_entries['lead_max'].parsed_entry,
            mercury_max = self.hm_entries['mercury_max'].parsed_entry)
        
    def new_microbes(self, session, item):
        item.microbes.new(session)
        item.microbes.update(session,
            tpc_min = self.microbe_entries['tpc_min'].parsed_entry,
            tpc_max = self.microbe_entries['tpc_max'].parsed_entry,
            ym_min  = self.microbe_entries['ym_min'].parsed_entry,
            ym_max  = self.microbe_entries['ym_max'].parsed_entry,)
    
    def new_pathogens(self, session, item):
        item.pathogens.new(session)
        item.pathogens.update(session,
            ecoli      = self.pathogen_entries['ecoli'].parsed_entry,
            salmonella = self.pathogen_entries['salmonella'].parsed_entry,
            staph      = self.pathogen_entries['staph'].parsed_entry)

#-----------------------------------------------------------------------------#
       
class BasicSpecDialog(SimpleDialog):
    def __init__(self):
        super().__init__(basic_spec_ui())
        self.label_entries()
        self.item_entries['name'].line_edit.textChanged.connect(self.check_requirements)
    
    def check_requirements(self):
        try:
            if self.item_entries['name'].line_edit.text() != '':
                self.enable_ok()
            else:
                self.disable_ok()           
        except Exception as ex:
            self.disable_ok()
            raise
            
    def label_entries(self):
        self.item_entries = \
        {'id':     LineEdit(self.ui.is_item_numberLE, restrict_to = 'int'),
         'name':   LineEdit(self.ui.is_item_nameLE),
         'note':   PlainText(self.ui.is_item_notePT),
         'fridge': CheckBox(self.ui.is_fridgeCB)}
        
        self.allergen_entries = \
        {'egg':       CheckBox(self.ui.is_eggCB),
         'peanut':    CheckBox(self.ui.is_peanutCB),
         'soy':       CheckBox(self.ui.is_soyCB),
         'shellfish': CheckBox(self.ui.is_shellfishCB),
         'fish':      CheckBox(self.ui.is_fishCB),
         'wheat':     CheckBox(self.ui.is_wheatCB),
         'milk':      CheckBox(self.ui.is_milkCB),
         'treenut':   CheckBox(self.ui.is_treenutCB)}

    def popup(self, item):
        #check for existing data and fill entries with it
        with OpenSession() as session:
            item.query(session)
            item.allergens.query(session)
        if item.data is not None:
            self.fill_basic(item)
        if item.allergens.data is not None:
            self.fill_allergens(item.allergens)
        #show the dialog and transfer input to the database
        if self.exec_():
            with OpenSession() as session:
                self.create_from_input(session, item)
    
    def fill_basic(self, item):
        self.item_entries['id'].fill_with(item.data.id)
        self.item_entries['name'].fill_with(item.data.name)
        self.item_entries['note'].fill_with(item.data.note)
        self.item_entries['fridge'].fill_with(item.data.fridge)
    def fill_allergens(self, allergens):
        self.allergen_entries['egg'].fill_with(allergens.data.egg)
        self.allergen_entries['soy'].fill_with(allergens.data.soy)
        self.allergen_entries['milk'].fill_with(allergens.data.milk)
        self.allergen_entries['peanut'].fill_with(allergens.data.peanut)
        self.allergen_entries['treenut'].fill_with(allergens.data.treenut)
        self.allergen_entries['shellfish'].fill_with(allergens.data.shellfish)
        self.allergen_entries['fish'].fill_with(allergens.data.fish)
        self.allergen_entries['wheat'].fill_with(allergens.data.wheat)
    
    def create_from_input(self, session, item):
        self.parse_input()
        self.edit_item(session, item)
        self.edit_allergens(session, item)
    
    def parse_input(self):
        for key,entry in self.item_entries.items():
            entry.parse_input()
        for key,entry in self.allergen_entries.items():
            entry.parse_input()
        
    def edit_item(self, session, item):
        item.query(session)
        item.update(session,
            name   = self.item_entries['name'].parsed_entry,
            note   = self.item_entries['note'].parsed_entry,
            fridge = self.item_entries['fridge'].parsed_entry)
    
    def edit_allergens(self, session, item):
        item.allergens.query(session)
        if item.allergens.data is None:
            item.allergens.new(session)        
        item.allergens.update(session,
            egg       = self.allergen_entries['egg'].parsed_entry,
            soy       = self.allergen_entries['soy'].parsed_entry,
            peanut    = self.allergen_entries['peanut'].parsed_entry,
            wheat     = self.allergen_entries['wheat'].parsed_entry,
            milk      = self.allergen_entries['milk'].parsed_entry,
            shellfish = self.allergen_entries['shellfish'].parsed_entry,
            fish      = self.allergen_entries['fish'].parsed_entry,
            treenut   = self.allergen_entries['treenut'].parsed_entry)  
        
#-----------------------------------------------------------------------------#
       
class HeavyMetalsDialog(SimpleDialog):
    def __init__(self):
        #set up the user interface
        super().__init__(hm_spec_ui())     
        self.label_entries()
        self.set_hm_unit_display()
        #update heavy metal unit display when different units are selected
        self.entries['units'].combobox.\
        currentIndexChanged.connect(self.set_hm_unit_display) 
        
    def label_entries(self):
        self.entries = \
        {'units':       ComboBox(self.ui.is_unitCombo),
         'arsenic_max': LineEdit(self.ui.is_asLE, restrict_to = 'float'),
         'cadmium_max': LineEdit(self.ui.is_cdLE, restrict_to = 'float'),
         'lead_max':    LineEdit(self.ui.is_pbLE, restrict_to = 'float'),
         'mercury_max': LineEdit(self.ui.is_hgLE, restrict_to = 'float')}

    def set_hm_unit_display(self):
        """Fill the heavy metal unit labels with the selected unit."""
        units = str(self.entries['units'].combobox.currentText())
        self.ui.is_unitL1.setText(units)
        self.ui.is_unitL2.setText(units)
        self.ui.is_unitL3.setText(units)
        self.ui.is_unitL4.setText(units)

    def popup(self, item):
        #check for existing data and fill entries with it
        with OpenSession() as session:
            item.hm.query(session)
        if item.hm.data is not None:
            self.fill_hm(item.hm)
        #show the dialog and transfer input to the database
        if self.exec_():
            with OpenSession() as session:
                self.create_from_input(session, item)

    def fill_hm(self, hm):
        self.entries['units'].fill_with(hm.data.units)
        self.entries['arsenic_max'].fill_with(hm.data.arsenic_max)
        self.entries['cadmium_max'].fill_with(hm.data.cadmium_max)
        self.entries['lead_max'].fill_with(hm.data.lead_max)
        self.entries['mercury_max'].fill_with(hm.data.mercury_max)
    
    def create_from_input(self, session, item):
        self.parse_input()
        self.new_hm(session, item)
    
    def parse_input(self):
        for key,entry in self.entries.items():
            entry.parse_input()
            
    def new_hm(self, session, item):
        if item.hm.data is None:
            item.hm.new(session)
        item.hm.query(session)
        item.hm.update(session,
            units       = self.entries['units'].parsed_entry,
            arsenic_max = self.entries['arsenic_max'].parsed_entry,
            cadmium_max = self.entries['cadmium_max'].parsed_entry,
            lead_max    = self.entries['lead_max'].parsed_entry,
            mercury_max = self.entries['mercury_max'].parsed_entry)

#-----------------------------------------------------------------------------#

class MicroDialog(SimpleDialog):
    def __init__(self):
        #set up the user interface
        super().__init__(micro_spec_ui())
        self.label_entries()
       
    def label_entries(self):
        self.microbe_entries = \
        {'tpc_min': LineEdit(self.ui.is_tpc_minLE, restrict_to = 'int'),
         'tpc_max': LineEdit(self.ui.is_tpc_maxLE, restrict_to = 'int'),
         'ym_min':  LineEdit(self.ui.is_ym_minLE,  restrict_to = 'int'),
         'ym_max':  LineEdit(self.ui.is_ym_maxLE,  restrict_to = 'int')}
       
        self.pathogen_entries = \
        {'ecoli':      ComboBox(self.ui.is_ecoliCombo,
                                combo_type = 'true_false_none'),
         'salmonella': ComboBox(self.ui.is_salmonellaCombo,
                                combo_type = 'true_false_none'),
         'staph':      ComboBox(self.ui.is_staphCombo,
                                combo_type = 'true_false_none')}
        for key, combo in self.pathogen_entries.items():
            combo.set_true_false_indices(true_index = 2,
                                         false_index = 0,
                                         none_index = 1)      
   
    def popup(self, item):
        #check for existing data and fill entries with it
        with OpenSession() as session:
            item.microbes.query(session)
            item.pathogens.query(session)
        if item.microbes.data is not None:
            self.fill_microbes(item.microbes)
        if item.pathogens.data is not None:
            self.fill_pathogens(item.pathogens)
        #show the dialog and transfer input to the database
        if self.exec_():
            with OpenSession() as session:
                self.create_from_input(session, item)        

    def fill_microbes(self, microbes):
        self.microbe_entries['tpc_max'].fill_with(microbes.data.tpc_max)
        self.microbe_entries['tpc_min'].fill_with(microbes.data.tpc_min)
        self.microbe_entries['ym_max'].fill_with(microbes.data.ym_max)
        self.microbe_entries['ym_min'].fill_with(microbes.data.ym_min)
        
    def fill_pathogens(self, pathogens):
        self.pathogen_entries['ecoli'].fill_with(pathogens.data.ecoli)
        self.pathogen_entries['salmonella'].fill_with(pathogens.data.salmonella)
        self.pathogen_entries['staph'].fill_with(pathogens.data.staph)
    
    def create_from_input(self, session, item):
        self.parse_input()
        self.new_microbes(session, item)
        self.new_pathogens(session, item)
                   
    def parse_input(self):
        for key,entry in self.microbe_entries.items():
            entry.parse_input()
        for key,entry in self.pathogen_entries.items():
            entry.parse_input()
    
    def new_microbes(self, session, item):
        if item.microbes.data is None:
            item.microbes.new(session)
        item.microbes.query(session)
        item.microbes.update(session,
            tpc_min = self.microbe_entries['tpc_min'].parsed_entry,
            tpc_max = self.microbe_entries['tpc_max'].parsed_entry,
            ym_min  = self.microbe_entries['ym_min'].parsed_entry,
            ym_max  = self.microbe_entries['ym_max'].parsed_entry)
                             
    def new_pathogens(self, session, item):
        if item.pathogens.data is None:
            item.pathogens.new(session)
        item.pathogens.query(session)
        item.pathogens.update(session,
            ecoli      = self.pathogen_entries['ecoli'].parsed_entry,
            salmonella = self.pathogen_entries['salmonella'].parsed_entry,
            staph      = self.pathogen_entries['staph'].parsed_entry)        


#-----------------------------------------------------------------------------#

class OrganolepticDialog(SimpleDialog):
    def __init__(self):
        #set up the user interface
        super().__init__(organoleptic_spec_ui())
        self.label_entries()
        
    def label_entries(self):
        self.entries = \
        {'color':      LineEdit(self.ui.is_colorLE),
         'odor':       LineEdit(self.ui.is_odorLE),
         'appearance': LineEdit(self.ui.is_appearanceLE)}

    def popup(self, item):
        #check for existing data and fill entries with it
        with OpenSession() as session:
            item.organoleptics.query(session)
        if item.organoleptics.data is not None:
            self.fill_organoleptics(item.organoleptics)
        #show the dialog and transfer input to the database
        if self.exec_():
            with OpenSession() as session:
                self.create_from_input(session, item)   
    
    def fill_organoleptics(self, organoleptics):
        self.entries['color'].fill_with(organoleptics.data.color)
        self.entries['odor'].fill_with(organoleptics.data.odor)
        self.entries['appearance'].fill_with(organoleptics.data.appearance)
     
    def create_from_input(self, session, item):
        self.parse_input()
        self.new_organoleptics(session, item)
        
    def parse_input(self):
        for key,entry in self.entries.items():
            entry.parse_input()
            
    def new_organoleptics(self, session, item):
        if item.organoleptics.data is None:
            item.organoleptics.new(session)
        item.organoleptics.query(session)
        item.organoleptics.update(session,
            color      = self.entries['color'].parsed_entry,
            odor       = self.entries['odor'].parsed_entry,
            appearance = self.entries['appearance'].parsed_entry)   
        
#-----------------------------------------------------------------------------#

class PhysicalDialog(SimpleDialog):
    def __init__(self):
        #set up the user interface
        super().__init__(physical_spec_ui())
        self.label_entries()
        
    def label_entries(self):
        self.moisture_entries = \
        {'lower_bound': LineEdit(self.ui.is_moisture_minLE, restrict_to = 'float'),
         'upper_bound': LineEdit(self.ui.is_moisture_maxLE, restrict_to = 'float')}
        
        self.density_entries = \
        {'flow_min': LineEdit(self.ui.is_flow_density_minLE, restrict_to = 'float'),
         'flow_max': LineEdit(self.ui.is_flow_density_maxLE, restrict_to = 'float'),
         'tap_min':  LineEdit(self.ui.is_tap_density_minLE,  restrict_to = 'float'),
         'tap_max':  LineEdit(self.ui.is_tap_density_maxLE,  restrict_to = 'float')}
        
        self.avgwt_entries = \
        {'lower_bound': LineEdit(self.ui.is_avgwt_minLE, restrict_to = 'float'),
         'upper_bound': LineEdit(self.ui.is_avgwt_maxLE, restrict_to = 'float')}
     
    def popup(self, item):
        #check for existing data and fill entries with it
        with OpenSession() as session:
            item.moisture.query(session)
            item.density.query(session)
            item.avgwt.query(session)
        if item.moisture.data is not None:
            self.fill_moisture(item.moisture)
        if item.density.data is not None:
            self.fill_density(item.density)
        if item.avgwt.data is not None:
            self.fill_avgwt(item.avgwt)
        #show the dialog and transfer input to the database
        if self.exec_():
            with OpenSession() as session:
                self.create_from_input(session, item)            
        
    def fill_moisture(self, moisture):
        self.moisture_entries['lower_bound'].fill_with(moisture.data.lower_bound)
        self.moisture_entries['upper_bound'].fill_with(moisture.data.upper_bound)
        
    def fill_density(self, density):
        self.density_entries['flow_min'].fill_with(density.data.flow_min)
        self.density_entries['flow_max'].fill_with(density.data.flow_max)
        self.density_entries['tap_min'].fill_with(density.data.tap_min)
        self.density_entries['tap_max'].fill_with(density.data.tap_max)
            
    def fill_avgwt(self, avgwt):
        self.avgwt_entries['lower_bound'].fill_with(avgwt.data.lower_bound)
        self.avgwt_entries['upper_bound'].fill_with(avgwt.data.upper_bound)
    
    def create_from_input(self, session, item):
        self.parse_input()
        self.new_moisture(session, item.moisture)
        self.new_density(session, item.density)
        self.new_avgwt(session, item.avgwt)
        
    def parse_input(self):
        for key,entry in self.moisture_entries.items():
            entry.parse_input()
        for key,entry in self.density_entries.items():
            entry.parse_input()
        for key,entry in self.avgwt_entries.items():
            entry.parse_input()
            
    def new_moisture(self, session, moisture):
        if moisture.data is None:
            moisture.new(session)
        moisture.query(session)
        moisture.update(session,
            lower_bound = self.moisture_entries['lower_bound'].parsed_entry,
            upper_bound = self.moisture_entries['upper_bound'].parsed_entry)
    
    def new_density(self, session, density):
        if density.data is None:
            density.new(session)
        density.query(session)
        density.update(session,
            flow_min = self.density_entries['flow_min'].parsed_entry,
            flow_max = self.density_entries['flow_max'].parsed_entry,
            tap_min = self.density_entries['tap_min'].parsed_entry,
            tap_max = self.density_entries['tap_max'].parsed_entry)
    
    def new_avgwt(self, session, avgwt):
        if avgwt.data is None:
            avgwt.new(session)
        avgwt.query(session)
        avgwt.update(session,
            lower_bound = self.avgwt_entries['lower_bound'].parsed_entry,
            upper_bound = self.avgwt_entries['upper_bound'].parsed_entry)
        
#-----------------------------------------------------------------------------#

class PesticidesDialog(SimpleDialog):
    def __init__(self):
        super().__init__(pesticide_spec_ui())
        self.label_entries()
        
    def label_entries(self):
        self.entries = \
        {'standard': LineEdit(self.ui.is_standardLE)}
    
    def popup(self, item):
        #check for existing data and fill entries with it
        with OpenSession() as session:
            item.pesticides.query(session)
        if item.pesticides.data is not None:
            self.fill_pesticides(item.pesticides)
        #show the dialog and transfer input to the database
        if self.exec_():
            with OpenSession() as session:
                self.create_from_input(session, item)
    
    def fill_pesticides(self, pesticides):
        self.entries['standard'].fill_with(pesticides.data.standard)

    def create_from_input(self, session, item):
        self.parse_input()
        self.new_pesticides(session, item)

    def parse_input(self):
        for key,entry in self.entries.items():
            entry.parse_input()
        
    def new_pesticides(self, session, item):
        if item.pesticides.data is None:
            item.pesticides.new(session)
        item.pesticides.query(session)
        item.pesticides.update(session,
                               standard = self.entries['standard'].parsed_entry)

#-----------------------------------------------------------------------------#

class AssayDialog(SimpleDialog):
    def __init__(self):
        #set up the user interface
        super().__init__(assay_spec_ui())
        self.label_entries()
        self.assay_names = []
        self.populate_names()
        self.validate_entry()
        self.entries['name_option'].combobox.\
        currentIndexChanged.connect(self.validate_entry)
        self.entries['name_typed'].line_edit.\
        textChanged.connect(self.validate_entry)
        
    def populate_names(self):
        #populate the assay names combobox
        with OpenSession() as session:
            names = Assay_Names()
            names.get_names(session)                
            self.assay_names = names.names
            self.entries['name_option'].populate(self.assay_names) 

    def validate_entry(self):
        if self.entries['name_typed'].line_edit.text() == '' \
        and self.entries['name_option'].not_listed():
            self.disable_ok()
        else:
            self.enable_ok()
        
        if self.entries['name_option'].not_listed():
            self.entries['name_typed'].enable()
            self.entries['name_typed'].focus()
        else:
            self.entries['name_typed'].disable()

    def label_entries(self):
        self.entries = \
        {'name_option': ComboBox(self.ui.is_assay_nameCombo),
         'name_typed':  LineEdit(self.ui.is_assay_nameLE),
         'lower_bound': LineEdit(self.ui.is_assay_minLE, restrict_to = 'float'),
         'upper_bound': LineEdit(self.ui.is_assay_maxLE, restrict_to = 'float'),
         'units':       ComboBox(self.ui.is_unitCombo),
         'method':      ComboBox(self.ui.is_methodCombo),
         'dry_basis':   CheckBox(self.ui.is_dbCB)}
        
    def parse_input(self):
        for key,entry in self.entries.items():
            entry.parse_input()
            
    def get_entered_name(self):
        new_assay_name = ''
        if self.entries['name_typed'].parsed_entry is not None:
            new_assay_name = self.entries['name_typed'].parsed_entry
        else:
            new_assay_name = self.entries['name_option'].parsed_entry        
        return new_assay_name

    def update_name_list(self, name):
        if name == '':
            return False
        if name not in self.assay_names:
            with OpenSession() as session:
                names = Assay_Names()
                names.add_name(session, name)
        return True        
            
    
class NewAssayDialog(AssayDialog):
    def __init__(self):
        super().__init__()
        
    def popup(self, item):        
            #show the dialog and transfer input to the database
            if self.exec_():
                with OpenSession() as session:
                    self.create_from_input(session, item)
                
    def create_from_input(self, session, item):
        self.parse_input()
        self.new_assay(session, item)

    def new_assay(self, session, item, selected_assay_name = None):
        new_assay_name = self.get_entered_name()
        if self.update_name_list(new_assay_name):
            item.assays.new(session, name = new_assay_name)
            item.assays.specific[new_assay_name].query(session)
            item.assays.specific[new_assay_name].update(session,
                method      = self.entries['method'].parsed_entry,
                lower_bound = self.entries['lower_bound'].parsed_entry,
                upper_bound = self.entries['upper_bound'].parsed_entry,
                units       = self.entries['units'].parsed_entry,
                dry_basis   = self.entries['dry_basis'].parsed_entry)                

class EditAssayDialog(AssayDialog):
    def __init__(self):
        super().__init__()
        self.entries['name_option'].disable()
        
    def popup(self, item, selected_assay_name):
        #check for existing data and fill entries with it
        #with OpenSession() as session:
         #   item.assays.specific[selected_assay_name].query(session, selected_assay_name)
        if item.assays.specific[selected_assay_name].data is not None:                
            self.fill_assay(item.assays.specific[selected_assay_name])
        #show the dialog and transfer input to the database
        if self.exec_():
            with OpenSession() as session:
                self.create_from_input(session, item, selected_assay_name)
                    
    def fill_assay(self, assay):
        self.entries['name_option'].fill_with(assay.data.name)
        #self.entries['name_typed'].fill_with(assay.data.name)
        self.entries['lower_bound'].fill_with(assay.data.lower_bound)
        self.entries['upper_bound'].fill_with(assay.data.upper_bound)
        self.entries['units'].fill_with(assay.data.units)
        self.entries['dry_basis'].fill_with(assay.data.dry_basis)
                
    def create_from_input(self, session, item, selected_assay_name):
        self.parse_input()
        self.edit_assay(session, item, selected_assay_name)

    def edit_assay(self, session, item, selected_assay_name):
        new_assay_name = self.get_entered_name()
        if self.update_name_list(new_assay_name):
            item.assays.specific[selected_assay_name].query(session)
            item.assays.specific[selected_assay_name].update(session,
                name        = new_assay_name,
                method      = self.entries['method'].parsed_entry,
                lower_bound = self.entries['lower_bound'].parsed_entry,
                upper_bound = self.entries['upper_bound'].parsed_entry,
                units       = self.entries['units'].parsed_entry,
                dry_basis   = self.entries['dry_basis'].parsed_entry)
            #rerun the query to update the name-key in assays
            item.assays.query(session)

#TODO finagle a way to pop up a warning if adding assay that already exists        
        
#-----------------------------------------------------------------------------#

class ChemIDDialog(SimpleDialog):
    def __init__(self):
        #set up the user interface
        super().__init__(chem_spec_ui())
        self.label_entries()
        self.chem_names = []
        self.populate_names()        
        self.validate_entry()
        self.entries['name_option'].combobox.\
        currentIndexChanged.connect(self.validate_entry)
        self.entries['name_typed'].line_edit.\
        textChanged.connect(self.validate_entry)

    def populate_names(self):
        #populate the assay names combobox
        with OpenSession() as session:
            names = Chem_Names()
            names.get_names(session)                
            self.chem_names = names.names
            self.entries['name_option'].populate(self.chem_names)        

    def validate_entry(self):
        if self.entries['name_typed'].line_edit.text() == '' \
        and self.entries['name_option'].not_listed():
            self.disable_ok()
        else:
            self.enable_ok()
                
        if self.entries['name_option'].not_listed():
            self.entries['name_typed'].enable()
            self.entries['name_typed'].focus()
        else:
            self.entries['name_typed'].disable()        
    
    def label_entries(self):
        self.entries = \
        {'name_option' : ComboBox(self.ui.is_chem_nameCombo),
          'name_typed' : LineEdit(self.ui.is_chem_nameLE),
              'method' : ComboBox(self.ui.is_methodCombo),
            'presence' : ComboBox(self.ui.is_presenceCombo,
                              combo_type = 'true_false')}
        self.entries['presence'].\
        set_true_false_indices(true_index = 0, false_index = 1)
        
    def parse_input(self):
        for key,entry in self.entries.items():
            entry.parse_input()

    def get_entered_name(self):
        new_chem_name = ''
        if self.entries['name_typed'].parsed_entry is not None:
            new_chem_name = self.entries['name_typed'].parsed_entry
        else:
            new_chem_name = self.entries['name_option'].parsed_entry   
        return new_chem_name

    def update_name_list(self, name):
        if name == '':
            return False
        if name not in self.chem_names:
            with OpenSession() as session:
                names = Chem_Names()
                names.add_name(session, name)
        return True

class NewChemIDDialog(ChemIDDialog):
    def __init__(self):
        super().__init__()
        
    def popup(self, item):
        #show the dialog and transfer input to the database
        if self.exec_():
            with OpenSession() as session:
                self.create_from_input(session, item)
                
    def create_from_input(self, session, item):
        self.parse_input()
        self.new_chem(session, item)
    
    
    def new_chem(self, session, item):
        new_chem_name = self.get_entered_name()
        if self.update_name_list(new_chem_name):
            item.chem_ids.new(session, name = new_chem_name)
            item.chem_ids.specific[new_chem_name].query(session)
            item.chem_ids.specific[new_chem_name].update(session,
                method      = self.entries['method'].parsed_entry,
                presence    = self.entries['presence'].parsed_entry)

class EditChemIDDialog(ChemIDDialog):
    def __init(self):
        super().__init__()


    def popup(self, item, selected_chem_name):
        #check for existing data and fill entries with it
        #with OpenSession() as session:
         #   item.chem_ids.specific[selected_chem_name].query(session, selected_chem_name)
        if item.chem_ids.specific[selected_chem_name].data is not None:                
            self.fill_chem(item.chem_ids.specific[selected_chem_name])
        #show the dialog and transfer input to the database
        if self.exec_():
            with OpenSession() as session:
                self.create_from_input(session, item, selected_chem_name)
        
    def fill_chem(self, chem):
        self.entries['name_option'].fill_with(chem.data.name)
        self.entries['name_option'].disable()
        self.entries['method'].fill_with(chem.data.method)
        self.entries['presence'].fill_with(chem.data.presence)
   
    def create_from_input(self, session, item, selected_chem_name):
        self.parse_input()
        self.edit_chem(session, item, selected_chem_name)

    def edit_chem(self, session, item, selected_chem_name):
        new_chem_name = self.get_entered_name()
        if self.update_name_list(new_chem_name):
            item.chem_ids.specific[selected_chem_name].query(session)
            item.chem_ids.specific[selected_chem_name].\
            update(session,
                   name        = new_chem_name,
                   method      = self.entries['method'].parsed_entry,
                   presence    = self.entries['presence'].parsed_entry)
            #rerun the query to update the name-key in chem_ids
            item.chem_ids.query(session)
    
#-----------------------------------------------------------------------------#

class PlantIDDialog(SimpleDialog):
    def __init__(self):
        super().__init__(plant_spec_ui())
        self.label_entries()
        self.validate_entry()
        self.entries['genus'].line_edit.textChanged.connect(self.validate_entry)
        
    def validate_entry(self):
        if self.entries['genus'].line_edit.text() == "":
            self.disable_ok()
        else:
            self.enable_ok()
    
    def label_entries(self):
        self.entries = \
        {'genus':  LineEdit(self.ui.is_genusLE),
        'species': LineEdit(self.ui.is_speciesLE),
        'part':    LineEdit(self.ui.is_partLE),
        'solvent': ComboBox(self.ui.is_solventCombo),
        'method':  ComboBox(self.ui.is_methodCombo)}  


    def parse_input(self):
        for key,entry in self.entries.items():
            entry.parse_input()

    def get_entered_name(self):
        new_genus_species = []
        genus_entry = self.entries['genus'].parsed_entry  
        species_entry = self.entries['species'].parsed_entry
        bad_species = ['spp', 'spp.', 'genus only', 'genus']
        if species_entry is None or species_entry in bad_species:
            species_entry = "sp."
        if genus_entry is not None:
            new_genus_species.append(genus_entry)
        if species_entry is not None:
            new_genus_species.append(species_entry)
        return ' '.join(new_genus_species) 

class NewPlantIDDialog(PlantIDDialog):
    def __init__(self):
        super().__init__()        
        
    def popup(self, item):
        #show the dialog and transfer input to the database
        if self.exec_():
            with OpenSession() as session:
                self.create_from_input(session, item)
                
    def create_from_input(self, session, item):
        self.parse_input()
        self.new_plant(session, item)
        
    def new_plant(self, session, item):
        new_plant_name = self.get_entered_name()
        item.plant_ids.new(session, genus_species = new_plant_name)
        item.plant_ids.specific[new_plant_name].query(session)
        item.plant_ids.specific[new_plant_name].update(session,
            part = self.entries['part'].parsed_entry,
            solvent = self.entries['solvent'].parsed_entry,
            method        = self.entries['method'].parsed_entry)
        
class EditPlantIDDialog(PlantIDDialog):
    def __init__(self):
        super().__init__()
        self.entries['genus'].disable()
        self.entries['species'].disable()
            
    def popup(self, item, selected_genus_species):    
        #check for existing data and fill entries with it
        #with OpenSession() as session:
            #Idea: change specific to current, don't use dictionary to select specific things
            #use a select method to point to the desired one held in the plant_ids/assays
            #item.plant_ids.specific[selected_genus_species].select_name()
            #item.plant_ids.specific[selected_genus_species].query(session, selected_genus_species)
        if item.plant_ids.specific[selected_genus_species].data is not None:                
            self.fill_plant(item.plant_ids.specific[selected_genus_species])
        #show the dialog and transfer input to the database
        if self.exec_():
            with OpenSession() as session:
                self.create_from_input(session, item, selected_genus_species) 
            
    def fill_plant(self, plant):
        self.entries['genus'].fill_with(plant.genus_string())
        self.entries['species'].fill_with(plant.species_string())
        self.entries['part'].fill_with(plant.data.part)
        self.entries['solvent'].fill_with(plant.data.solvent)
        self.entries['method'].fill_with(plant.data.method)
    
    def create_from_input(self, session, item, selected_genus_species):
        self.parse_input()
        self.edit_plant(session, item, selected_genus_species)

    def edit_plant(self, session, item, selected_genus_species):
        new_plant_name = self.get_entered_name()          
        item.plant_ids.specific[selected_genus_species].query(session)
        item.plant_ids.specific[selected_genus_species].update(session,
            genus_species = new_plant_name,
            part = self.entries['part'].parsed_entry,
            solvent = self.entries['solvent'].parsed_entry,
            method        = self.entries['method'].parsed_entry)
        #rerun the query to update the name-key in plant_ids
        item.plant_ids.query(session)        