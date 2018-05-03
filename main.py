from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QApplication

import sys
sys.path.append(".\\DataBase")
sys.path.append(".\\Direct")
sys.path.append(".\\UI")

#Import the primary user interface
from interfaces.Window_Main import Ui_MainWindow
#Import a module to display information in the UI
from Displayer import Display
#Import button functions
from Buttons import SearchButton
#Import dialog popups
from Dialogs import NewItemDialog, HeavyMetalsDialog, MicroDialog, NewAssayDialog, EditAssayDialog
from Dialogs import TextDialog, OrganolepticDialog, PhysicalDialog, NewChemIDDialog, EditChemIDDialog
from Dialogs import NewPlantIDDialog, EditPlantIDDialog, PesticidesDialog, BasicSpecDialog, NewLotDialog
#Import database interactability
from DataInteraction_Branches import Interactive_RawItem, Interactive_RawLot
from SessionOpener import OpenSession      

class DFH_Integra(QMainWindow):
    """Initializes the Integra interface and connects UI elements to their functions."""
    def __init__(self):
        #initiate the user interface
        super().__init__()
        self.ui = Ui_MainWindow()        
        self.ui.setupUi(self)
        
        #get and send data from the database
        self.item = Interactive_RawItem()
        self.lot = Interactive_RawLot()
        
        #Create a display handler
        self.display = Display(self.ui)
        self.display.disable_item_entry()
        
        #connect the ui elements to their functions         
        self.connect_buttons()
        self.connect_actions()
        self.connect_new_menus()
        self.connect_edit_menus()
        self.connect_remove_menus()
        self.connect_key_presses()
        self.connect_list_clicks()
        self.connect_table_clicks()
        
        #place the UI on the screen
        self.show()
    
    def connect_buttons(self):
        self.ui.searchB.clicked\
        .connect(self.search_click)
              
        #self.ui.is_save_noteB.clicked\
        #.connect(self.save_note_click)               
    
    def connect_actions(self):
        #conditonally enable buttons for table interaction
        self.ui.is_assayList.currentItemChanged\
        .connect(lambda: self.display.enable_assay_entry(self.item))
        
        self.ui.is_chemList.currentItemChanged\
        .connect(lambda: self.display.enable_chem_entry(self.item))
        
        self.ui.is_plantList.currentItemChanged\
        .connect(lambda: self.display.enable_plant_entry(self.item))
    
    def connect_new_menus(self):
        self.ui.menu_newItem_2.triggered\
        .connect(lambda: self.standard_dialog(NewItemDialog))
        
        self.ui.menu_newLot.triggered\
        .connect(lambda: self.standard_dialog(NewLotDialog))

        self.ui.menu_newAssay.triggered\
        .connect(lambda: self.standard_dialog(NewAssayDialog))

        self.ui.menu_newChem.triggered\
        .connect(lambda: self.standard_dialog(NewChemIDDialog))

        self.ui.menu_newPlant.triggered\
        .connect(lambda: self.standard_dialog(NewPlantIDDialog))
    
    def connect_edit_menus(self):
        self.ui.menu_editBasic_2.triggered\
        .connect(lambda: self.standard_dialog(BasicSpecDialog))

        self.ui.menu_editHM.triggered\
        .connect(lambda: self.standard_dialog(HeavyMetalsDialog))

        self.ui.menu_editMicrobes.triggered\
        .connect(lambda: self.standard_dialog(MicroDialog))

        self.ui.menu_editOrganoleptics.triggered\
        .connect(lambda: self.standard_dialog(OrganolepticDialog))

        self.ui.menu_editPhysicals.triggered\
        .connect(lambda: self.standard_dialog(PhysicalDialog))

        self.ui.menu_editPesticides.triggered\
        .connect(lambda: self.standard_dialog(PesticidesDialog))

        self.ui.menu_editAssay_2.triggered\
        .connect(self.edit_assay_click)

        self.ui.menu_editChem_2.triggered\
        .connect(self.edit_chem_click)

        self.ui.menu_editPlant_2.triggered\
        .connect(self.edit_plant_click)

    def connect_remove_menus(self):
        self.ui.menu_removeAssay.triggered\
        .connect(self.remove_assay_click)

        self.ui.menu_removeChem.triggered\
        .connect(self.remove_chem_click)

        self.ui.menu_removePlant.triggered\
        .connect(self.remove_plant_click)
    
    def connect_list_clicks(self):
        self.ui.il_lotList.clicked\
        .connect(self.lot_selected)
        
        self.ui.il_assay_resultList.clicked\
        .connect(self.lot_assay_selected)
        
        self.ui.il_chem_id_resultList.clicked\
        .connect(self.lot_chem_id_selected)

        self.ui.is_assayList.clicked\
        .connect(lambda: self.display.assay_selected(self.item.assays))

        self.ui.is_chemList.clicked\
        .connect(lambda: self.display.chem_selected(self.item.chem_ids))

        self.ui.is_plantList.clicked\
        .connect(lambda: self.display.plant_selected(self.item.plant_ids))
 
    def connect_table_clicks(self):
        self.ui.il_plant_id_resultTable.clicked\
        .connect(self.lot_plant_id_selected)
    
    def connect_key_presses(self):
        self.ui.searchT.returnPressed\
        .connect(self.search_click)
        
#------------------------------------------------------------------------------#

    def standard_dialog(self, dialog):
        """Creates a dialog for item data entry and displays the result."""
        editor = dialog()
        editor.popup(self.item)
        self.display.show_item(self.item)
    
    def standard_button(self, button, button_method, ui_element = None):
        button_instance = button(ui_element)
        button_instance.button_method(self.item)
        self.display.show_item(self.item)
  
    def lot_selected(self):
        selected_index = self.ui.il_lotList.currentRow()
        if selected_index != -1:
            lot_number = self.ui.il_lotList.item(selected_index).text()
            try:
                self.lot.select_lot(self.item.item_number, lot_number)
                self.display.show_lot(self.lot)
            except Exception as ex:
                print(ex)
                raise

    def lot_plant_id_selected(self):
        selected_row = self.ui.il_plant_id_resultTable.currentRow()
        if selected_row != -1:
            plant_names = []
            plant_names.append(self.fetch_table_text(self.ui.il_plant_id_resultTable, 0))
            plant_names.append(self.fetch_table_text(self.ui.il_plant_id_resultTable, 1))
            selected_plant_name = ' '.join(plant_names)
            self.display.lot_plant_id_selected(self.lot.plant_id_results, selected_plant_name)
                    
    def lot_assay_selected(self):
        selected_index = self.ui.il_assay_resultList.currentRow()
        if selected_index != -1:
            assay_name = self.ui.il_assay_resultList.item(selected_index).text()            
            self.display.lot_assay_selected(self.lot.assay_results, assay_name)

    def lot_chem_id_selected(self):
        selected_index = self.ui.il_chem_id_resultList.currentRow()
        if selected_index != -1:
            chem_name = self.ui.il_chem_id_resultList.item(selected_index).text()
            self.display.lot_chem_id_selected(self.lot.chem_id_results, chem_name)
    
    def search_click(self):
        """Create a search button, call search, get the search result, and display it."""
        search_button = SearchButton(self.ui.searchT)
        search_button.search(self.item)
        self.display.show_item(self.item)
        #renew the lot display
        self.lot = Interactive_RawLot()
        self.display.show_lot(self.lot)
        
    def save_note_click(self):
        if self.item.data is not None:
            new_note = self.ui.is_item_notePT.toPlainText()
            with OpenSession() as session:
                self.item.update(session, note = new_note)
        else:
            print("Warning: Load item data to save it's note.")  

    def fetch_table_text(self, table, info_column):
        row = table.currentRow()
        table_text = ""
        if row != -1:
            table_text = table.item(row, info_column).text()
        return table_text
        
    #TODO: move these towards a display class
    #that has the assay table defined as an object
    
    def edit_assay_click(self):
        selected_assay_name = self.fetch_table_text(self.ui.is_assayTable, 0)
        dialog = EditAssayDialog()
        if selected_assay_name is not None and selected_assay_name != '':
            dialog.popup(self.item, selected_assay_name)
            self.display.show_item(self.item)
    def remove_assay_click(self):
        selected_assay_name = self.fetch_table_text(self.ui.is_assayTable, 0)        
        if selected_assay_name is not None and selected_assay_name != '':
            text = "Are you sure you want to remove the selected assay?"
            dialog = TextDialog(text)
            if dialog.exec_():                        
                with OpenSession() as session:
                    self.item.assays.query(session)
                    self.item.assays.specific[selected_assay_name].\
                    remove(session)
                    self.item.assays.query(session)
            self.display.show_item(self.item)
            """
                try:
                    self.item.assays.access()
                    self.item.assays.specific[selected_assay_name].remove()
                except AttributeError:
                    print("Selected assay not in database.")
                except:
                    raise
            """
  
    def edit_chem_click(self):
        selected_chem_name = self.fetch_table_text(self.ui.is_chem_idTable, 0)
        dialog = EditChemIDDialog()
        if selected_chem_name is not None and selected_chem_name != '':
            dialog.popup(self.item, selected_chem_name)
            self.display.show_item(self.item)                  
    def remove_chem_click(self):
        selected_chem_name = self.fetch_table_text(self.ui.is_chem_idTable, 0)      
        if selected_chem_name is not None and selected_chem_name != '':
            text = "Are you sure you want to remove the selected chemical ID?"
            dialog = TextDialog(text)
            if dialog.exec_():
                with OpenSession() as session:
                    self.item.chem_ids.query(session)
                    self.item.chem_ids.specific[selected_chem_name].\
                    remove(session)
                    self.item.chem_ids.query(session)
            self.display.show_item(self.item)  
   
    def edit_plant_click(self):
        plant_names = []
        plant_names.append(self.fetch_table_text(self.ui.is_plant_idTable, 0))
        plant_names.append(self.fetch_table_text(self.ui.is_plant_idTable, 1))
        selected_plant_name = ' '.join(plant_names)
        dialog = EditPlantIDDialog()
        if selected_plant_name is not None and selected_plant_name != '':
            dialog.popup(self.item, selected_plant_name)
            self.display.show_item(self.item)
    def remove_plant_click(self):
        plant_names = []
        plant_names.append(self.fetch_table_text(self.ui.is_plant_idTable, 0))
        plant_names.append(self.fetch_table_text(self.ui.is_plant_idTable, 1))
        selected_plant_name = ' '.join(plant_names)
        if selected_plant_name is not None and selected_plant_name != '':
            text = "Are you sure you want to remove the selected botanical ID?"
            dialog = TextDialog(text)            
            if dialog.exec_():
                with OpenSession() as session:
                    self.item.plant_ids.query(session)
                    self.item.plant_ids.specific[selected_plant_name].\
                    remove(session)
                    self.item.plant_ids.query(session)
            self.display.show_item(self.item) 
                
#------------------------------------------------------------------------------#

#start the program        
if __name__ == '__main__':
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
        
    prog = DFH_Integra()
    
    sys.exit(app.exec_())