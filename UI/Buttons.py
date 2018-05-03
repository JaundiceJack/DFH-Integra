class SearchButton:
    def __init__(self, field_element):
        self.field = field_element
        self.text = None
        self.entry_type = None
        self.item_number = None

    def search(self, item):
        """execute different searches based one what type of input was found"""       
        self.get_search_text()
        self.determine_entry_type()
        if self.entry_type == 'raw_item_number':
            self.search_number(item)

    def get_search_text(self):
        self.text = str(self.field.text()).strip().lower()
    
    def determine_entry_type(self):
        if self.is_raw_item_number():
            self.entry_type = 'raw_item_number'

    def search_number(self, item):
        item.select_item_number(self.item_number)
    
    def is_raw_item_number(self):
        is_raw = False
        try:
            number = int(self.text)
            if number > 10000 and number < 20000:
                is_raw = True
                self.item_number = number
        except:
            pass
        finally:
            return is_raw