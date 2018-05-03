from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QTableWidgetItem, QListWidgetItem
#-----------------------------------------------------------------------------#
  
#display classes
class List:
    def __init__(self, ui_element):
        self.list = ui_element
    
    def clear(self):
        self.list.clear()
    
    def fill_with(self, word):
        if word is None:
            pass
        elif type(word) == str:
            self.list.addItem(QListWidgetItem(word))
        else:
            self.list.addItem(QListWidgetItem(str(word)))

    def current_item(self):
        ind = self.list.currentRow()
        if ind != -1:
            return self.list.item(ind).text() 
        else:
            return None

class Label:
    def __init__(self, ui_element, none_msg = ""):
        self.label = ui_element
        self.none_msg = none_msg

    def fill_with(self, words):
        if words is None:
            self.label.setText(self.none_msg)
        elif type(words) == str:
            self.label.setText(words)
        else:
            self.label.setText(str(words))

class Table:
    def __init__(self, ui_element):
        self.table = ui_element
    
    def clear(self):
        self.table.clearContents()
        self.table.setRowCount(0)
    
    def fill_with(self, *args):
        """Creates rows and fills horizontally"""
        col_count = 0
        row_pos = self.table.rowCount()
        self.table.insertRow(row_pos)
        for arg in args:
            self.table.setItem(row_pos, col_count, QTableWidgetItem(arg))
            col_count += 1           

    def fill_vertical(self, *args, start_row = 0, start_col = 0):
        """Fills vertically down already created table rows"""
        row_pos = start_row
        for arg in args:
            self.table.setItem(row_pos, start_col, QTableWidgetItem(arg))
            row_pos += 1
            
    def fill_horizontal(self, *args, start_row = 0, start_col = 0):
        """Fills horizontally accross already created table columns"""
        col_pos = start_col
        for arg in args:
            self.table.setItem(start_row, col_pos, QTableWidgetItem(arg))
            col_pos += 1
#Input classes

#toying with idea of collecting all entry fields in one manager class
class InputCollection:
    def __init__(self):
        self.entries = {}

class ComboBox:
    def __init__(self, ui_element, combo_type = None):
        self.combobox = ui_element
        self.combo_type = combo_type
        self.parsed_entry = None

    def enable(self):
        self.combobox.setEnabled(True)
    def disable(self):
        self.combobox.setEnabled(False)

    def set_true_false_indices(self, true_index = None,
                               false_index = None,
                               none_index = None):
        if true_index is not None:
            self.true_index = true_index
        if false_index is not None:
            self.false_index = false_index
        if none_index is not None:
            self.none_index = none_index

    def parse_input(self):
        if self.combo_type is None:
            self.parsed_entry =  self.standard()
        elif self.combo_type == 'true_false_none' \
        or self.combo_type == 'true_false':
            self.parsed_entry = self.tfn()
        else:
            print("Combobox type %s not handled in parse_input()." % \
                  self.combo_type)
            print("None will be given.")
            self.parsed_entry = None
    
    def populate(self, option_list):
        if self.combo_type is None:           
            self.combobox.clear()
            self.combobox.addItems(option_list)
            self.combobox.addItem("Not listed")
    
    def not_listed(self):
        return self.combobox.currentText() == "Not listed"
    
    def fill_with(self, filler):
        if self.combo_type is None:
            index = self.combobox.findText(filler)
            if index != -1:
                self.combobox.setCurrentIndex(index)
            else:
                print("Unable to set combobox. Text not found.")
        elif self.combo_type == 'true_false_none':
            if filler is None:
                self.combobox.setCurrentIndex(self.none_index)
            elif filler:
                self.combobox.setCurrentIndex(self.true_index)
            elif not filler:
                self.combobox.setCurrentIndex(self.false_index)
        elif self.combo_type == 'true_false':
            if filler:
                self.combobox.setCurrentIndex(self.true_index)
            else:
                self.combobox.setCurrentIndex(self.false_index)
                    
    def standard(self):
        return (str(self.combobox.currentText()))      
    
    def tfn(self):
        currentIndex = self.combobox.currentIndex()
        combo_value = None
        if currentIndex == self.true_index:
            combo_value = True
        elif currentIndex == self.false_index:
            combo_value = False
        return combo_value
        
class PlainText:
    def __init__(self, ui_element):
        self.plaintext = ui_element
        self.parsed_entry = None

    def fill_with(self, words):
        if words is None:
            self.plaintext.clear()
        else:
            self.plaintext.clear()
            self.plaintext.insertPlainText(words)

    def parse_input(self):
        self.parsed_entry = self.plaintext.toPlainText()
    
class CheckBox:
    def __init__(self, ui_element):
        self.checkbox = ui_element
        self.parsed_entry = None

    def parse_input(self):
        if self.checkbox.isChecked():
            self.parsed_entry = True
        else:
            self.parsed_entry = False
        
    def fill_with(self, filler):
        if filler:
            self.checkbox.setChecked(True)
        else:
            self.checkbox.setChecked(False)
    
class LineEdit:
    def __init__(self, ui_element, restrict_to = None):
        self.line_edit = ui_element
        self.parsed_entry = None
        
        self.validator = None
        self.input_restriction = restrict_to
        if restrict_to is not None:
            self.restrict_input(restrict_to)

    def enable(self):
        self.line_edit.setEnabled(True)
    def disable(self):
        self.line_edit.setEnabled(False)
    def focus(self):
        self.line_edit.setFocus(True)

    def restrict_input(self, restrict_to):
        #check for the analagous validator
        if restrict_to == 'int':
            self.validator = QIntValidator()
        elif restrict_to == 'float' or restrict_to == 'double':
            self.validator = QDoubleValidator()
        else:
            print("Input restriction to %s not handled." % restrict_to)
            self.validator = None
        #set the ui element's validator if one was found    
        if self.validator is not None:
            self.line_edit.setValidator(self.validator)            

    def parse_input(self):
        if self.input_restriction is None:
            self.parsed_entry = LineEdit.standard_line(self.line_edit)
        elif self.input_restriction == 'double'\
        or   self.input_restriction == 'float':
            self.parsed_entry = LineEdit.standard_line(self.line_edit)
        elif self.input_restriction == 'int':
            self.parsed_entry = LineEdit.int_line(self.line_edit)
        else:
            print("Entry type %s not handled in parse_input()." % \
                  self.entry_type)
            print("None will be given.")
            self.parsed_entry = None

    def fill_with(self, filler):
        if filler is None:
            self.line_edit.setText('')
        else:
            self.line_edit.setText(str(filler))            
            
    @staticmethod            
    def standard_line(line_edit):
        """returns the text from a line edit, stripped of trailing/leading white
        space. If a modify function is specified, it will be applied after 
        stripping. If the line edit was empty, None is returned."""
        text = None

        text = line_edit.text().strip().lower()

        if text == '':
            text = None
        return text
    
    @staticmethod       
    def int_line(line_edit):
        text = LineEdit.standard_line(line_edit)
        if text is not None:
            try:
                text = int(text)
            except:
                print("Warning: unable to convert %s to an integer." % text)
        return text