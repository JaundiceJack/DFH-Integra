from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError
from sqlalchemy import inspect

class Basis:
    def __init__(self, table_class):
        self.table_class = table_class
        self.data = None
        self.data_access_dict = {}
        self.update_attributes = []

    def check_data_persistence(self):
        persistent = False
        if self.data is not None:
            inst = inspect(self.data)
            if inst.persistent:
                persistent = True
        return persistent
        
    def basis_access(self, session):
        """basis_access returns True if a persistent instance of the data
        is found and False if not."""
        accessed = False
        if self.data is None:
            self.basis_query(session)
        if self.check_data_persistence():
            accessed = True
        else:
            self.basis_query(session)
            if self.check_data_persistence():
                accessed = True                
        return accessed

    def basis_update(self, session, **updates):
        if self.data is not None:
            for attribute in self.update_attributes:
                value = updates.get(attribute, 'noupdate')
                if value != 'noupdate':
                    try:
                        setattr(self.data, attribute, value)
                    except AttributeError:
                        print("No %s attribute in %s." % \
                              (attribute, self.table_class.__name__))
                        print("Changes will not be saved.")
                    except Exception as ex:
                        print(ex)
                        raise
                    else:
                        self.basis_commit(session)
        else:
            print("No %s data to update." % self.table_class.__name__)
            print("Run query or new to populate data.")  
        
    def basis_query(self, session):
        try:
            self.data = session.query(self.table_class).\
            filter_by(**self.data_access_dict).one()
        except NoResultFound:
            self.data = None
        except MultipleResultsFound:
            print("Error: Multiple entries found in scalar query.")
            print("Query was to %s." % self.table_class.__name__)
            raise
        except Exception as ex:
            print("Error: Unhandled exception in query.")
            print("Query was to %s." % self.table_class.__name__)
            print(ex)
            raise
    
    def basis_commit(self, session):
        try:
            session.flush()
        except (IntegrityError, FlushError) as ex:
            self.data = None
            session.rollback()
            print("Error: Duplicated data discovered on commit to %s." % \
                  self.table_class.__name__)
            raise ex                      
        except:
            self.data = None
            session.rollback()
            print("Error: An unhandled exception occured.")
            print("Failed to commit entry to %s" % \
                  self.table_class.__name__)
            raise
        else:
            session.commit()
    
    def basis_new(self, session):
        new_basis = self.table_class(**self.data_access_dict)
        try:
            session.add(new_basis)
            session.flush()
        except (IntegrityError, FlushError) as ex:
            self.data = None
            session.rollback()
            print("Error: Provided name/identifier already exists in the database.")
            raise ex                      
        except:
            self.data = None
            session.rollback()
            print("Error: An unhandled exception occured.")
            print("Failed to commit new entry to %s" % \
                  self.table_class.__name__)
            raise
        else:
            session.commit()
            self.data = new_basis
    
    #Note: Children using this method must call remove on all related members    
    def basis_remove(self, session):
        if self.data is not None:       
            try:
                session.delete(self.data)
                session.flush()
            except(IntegrityError, FlushError) as ex:
                session.rollback()
                print("Error: Unable to remove data from %s" % \
                      self.table_class.__name__)
            except Exception as ex:
                session.rollback()
                print("Error: Failed to delete entry in %s" % \
                      self.table_class.__name__)
                print(ex)
                raise
            else:
                session.commit()
                self.data = None                
        else:
            print("No data to remove from %s." % self.table_class.__name__)
            
    def manual_new(self, session, table, **kwargs):
        new_thing = table(**kwargs)
        try:
            session.add(new_thing)
            session.flush()
        except (IntegrityError, FlushError) as ex:
            session.rollback()
            print("Error: Provided name/identifier already exists in %s." % \
                  table.__name__)
            raise ex                      
        except:
            session.rollback()
            print("Error: An unhandled exception occured.")
            print("Failed to commit new entry to %s" % \
                  table.__name__)
            raise
        else:
            session.commit() 
            
    def manual_update(self, session, table,
                      update_data, update_attributes, **updates):
        if update_data is not None:
            for attribute in update_attributes:
                value = updates.get(attribute, 'noupdate')
                if value != 'noupdate':
                    try:
                        setattr(update_data, attribute, value)
                    except AttributeError:
                        print("No %s attribute in %s." % \
                              (attribute, table.__name__))
                        print("Changes will not be saved.")
                    except Exception as ex:
                        print(ex)
                        raise
                    else:
                        session.commit()
        else:
            print("No %s data to update." % table.__name__)
            print("Run query or new to populate data.") 
            
    def manual_remove(self, session, table, remove_data):
        if remove_data is not None:       
            try:
                session.delete(remove_data)
                session.flush()
            except(IntegrityError, FlushError) as ex:
                session.rollback()
                print("Error: Unable to remove data from %s" % \
                      table.__name__)
            except Exception as ex:
                session.rollback()
                print("Error: Failed to delete entry in %s" % \
                      table.__name__)
                print(ex)
                raise
            else:
                session.commit()              
        else:
            print("No data to remove from %s." % table.__name__)        
            
#the basis_otm class is used for relating the basis otm relations to specific
#entries in the otm relation, designated in a dictionary keyed by
#uniquely constrained columns
class Basis_OTM:
    def __init__(self, table_class,
                 interactive_singlet_class, singlet_key_column):
        self.table_class = table_class       
        self.singlet_class = interactive_singlet_class
        
        self.data = []
        self.data_access_dict = {}
        
        self.singlet_key_column = singlet_key_column
        self.keys = []        
        self.specific = {}
    
    def check_data_persistence(self):
        persistent = False
        for datum in self.data:
            if datum is not None:
                inst = inspect(datum)
                if not inst.persistent:
                    break
            else:
                break
        else:
            persistent = True
        return persistent
    
    def otm_access(self, session):
        """otm_access returns True if all data is persistent and False if not."""
        accessed = False
        if not self.data:
            self.basis_query(session)
        else:
            accessed = self.check_data_persistence()
            if not accessed:
                self.otm_query(session)
                accessed = self.check_data_persistence()                
        return accessed
    
    def otm_new(self, session, **kwargs):
        """This attempts to add a new row to the table_class of the one-to-many relation."""
        new_data = self.table_class(**kwargs)
        key = "not generated"
        try:
            session.add(new_data)
            session.flush()
        except (IntegrityError, FlushError) as ex:
            print("Error: Provided name/identifier already exists in the database.")
            raise ex
        except Exception as ex:
            print("Error: Failed to commit new %s" % \
                  self.table_class.__name__)
            print(ex)
            raise
        else:
            session.commit()
            key = self.generate_key(new_data)
            self.data.append(new_data)
            self.label_singlets()
        return key
        
    def otm_query(self, session):
        #load raw data
        self.query_raw_data(session)
        #generate identifiers for each datum and assign them to a dictionary       
        self.label_singlets()
      
    def query_raw_data(self, session):
        try:
            self.data = session.query(self.table_class).\
            filter_by(**self.data_access_dict).\
            order_by(self.table_class.id).all()
        except Exception as ex:
            print(ex)
            raise

    def label_singlets(self):
        self.specific = {}
        for datum in self.data:
            key = self.generate_key(datum)
            if key != '':
                self.keys.append(key)
                singlet = self.singlet_class()
                singlet.data = datum
                self.specific[key] = singlet
            else:
                print("Warning: Data not assigned for item %s." % \
                      datum)
 
    def generate_key(self, datum):
        key_string = ""
        try:
            key = getattr(datum, self.singlet_key_column)
            if key is not None:
                key_string += str(key)
            else:
                print("Warning: a key was not generated for an entry in %s." % \
                      self.table_class.__name__)
        except AttributeError:
            print("Error: Provided keyword '%s' not found in %s." % \
                  self.singlet_key_column, self.table_class.__name__)
            raise
        except Exception as ex:
            print("Error: An unhanded exception occured.")
            print("Unable to generate specific key for %s" % \
                  self.table_class.__name__)
            raise
        return key_string

#################################################################################

class OTOSpec(Basis):
    def __init__(self, table_class):
        super().__init__(table_class)
        self.item_number = None      
        self.data_access_dict.update({'item_id': self.item_number})           
    
    def select_item_number(self, new_item_number):
        self.item_number = new_item_number
        self.data_access_dict['item_id'] = new_item_number
    
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
    
    def update(self, session, **updates):
        if self.has_ids('update') and self.access(session):
            self.basis_update(session, **updates)
    
    #TODO: in upper levels, raise a dialog if duplicate data is added
    def new(self, session):
        if self.has_ids('create new') and not self.access(session):
            self.basis_new(session)

    def query(self, session):
        if self.has_ids('query'):
            self.access(session)
            
    def remove(self, session):
        if self.has_ids('remove') and self.access(session):
            self.basis_remove(session)

#################################################################################

class OTMSpec(Basis_OTM):
    def __init__(self, table_class, interactive_class, key_column):
        super().__init__(table_class, interactive_class, key_column)
        self.item_number = None
        self.data_access_dict.update({'item_id': self.item_number})
        
    def select_item_number(self, new_item_number):
        self.item_number = new_item_number
        self.data_access_dict['item_id'] = new_item_number
        self.update_singlets()
      
    def update_singlets(self):
        for key, singlet in self.specific.items():
            singlet.select_item_number(self.item_number)

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
            return self.otm_access(session)
        else:
            return False
       
    def query(self, session):
        if self.has_ids('query'):
            self.otm_query(session)
            self.update_singlets()
 
    def remove(self, session):
        if self.has_ids('remove') and self.access(session):
            for key, singlet in self.specific.items():
                singlet.remove(session)
            
    def new(self, session, **new_singlet_identifier):
        if self.has_ids('create new'):
            kwargs = {}
            kwargs.update({'item_id': self.item_number})
            kwargs.update(new_singlet_identifier)
            self.otm_new(session, **kwargs)
            self.update_singlets()

#################################################################################

class OTMSpec_Singlet(OTOSpec):
    def __init__(self, table_class):
        super().__init__(table_class)
        self.identifier_is_called = "identifier"
        self.identifier = None        
    
    def has_ids(self, func_name):
        has_identifier = False
        if self.identifier is not None:
            has_identifier = True
        else:
            print("No %s given to %s %s." % \
                  (self.identifier_is_called,
                   func_name,
                   self.table_class.__name__))            
        return super().has_ids(func_name) and has_identifier

#################################################################################

class OTOLotData(Basis):
    def __init__(self, table_class):
        super().__init__(table_class)
        self.item_number = None
        self.lot_id = None
        self.data_access_dict.update({'lot_id': self.lot_id})       
    
    def select_item_number(self, new_item_number):
        """Changes the item number associated with the OTOLotData object."""
        self.item_number = new_item_number

    def select_lot_id(self, new_lot_id):
        """Changes the lot id associated with the OTOLotData object and
        updates the data access dict to obtain/modify the database by lot."""
        self.lot_id = new_lot_id
        self.data_access_dict['lot_id'] = new_lot_id  
        
    def has_ids(self, func_name):
        """Checks whether the OTOLotData object has both its item and lot numbers
        set. func_name is passed in purely for neat looking error messages"""
        has_item_number = False
        has_lot_id = False
        if self.item_number is not None:
            has_item_number = True
        else:
            print("No item number provided to %s %s." % \
                  (func_name, self.table_class.__name__))
        if self.lot_id is not None:
            has_lot_id = True
        else:
            print("No lot id provided to %s %s." % \
                  (func_name, self.table_class.__name__))
        return has_item_number and has_lot_id

    def access(self, session):
        if self.has_ids('access'):        
            return self.basis_access(session)
        else:
            return False

    def update(self, session, **updates):
        if self.has_ids('update') and self.access(session):
            self.basis_update(session, **updates)
    
    #TODO: in upper levels, raise a dialog if duplicate data is added
    def new(self, session):
        if self.has_ids('create new') and not self.access(session):
            self.basis_new(session)
            
    def query(self, session):
        if self.has_ids('query') and self.data is not None:
            self.basis_query(session)            
            #self.access(session)  
            
    def remove(self, session):
        if self.has_ids('remove') and self.access(session):
            self.basis_remove(session)
      
#################################################################################

class OTOResult(OTOLotData):
    def __init__(self, table_class, spec_class):
        super().__init__(table_class)
        self.spec_class = spec_class
        self.spec_update_attributes = []
        #self.tests = test_class()
        
    #TODO: what if there is already a spec?
    def new_spec(self, session):
        if self.has_ids('create a new specification for') \
        and self.access(session):
            self.manual_new(session, self.spec_class, result_id = self.data.id)
            self.query(session)

    #TODO: what if there is not a spec to update?            
    def update_spec(self, session, **updates):
        if self.has_ids('update specification for') \
        and self.access(session):
            self.manual_update(session, self.spec_class, self.data.spec,
                               self.spec_update_attributes, **updates)

    def remove(self, session):
        if self.has_ids('remove') and self.access(session):
            self.manual_remove(session, self.spec_class, self.data.spec)
            self.basis_remove(session)
            
#################################################################################            
            
class OTMResult(Basis_OTM):        
    def __init__(self, table_class, interactive_class, key_column):
        super().__init__(table_class, interactive_class, key_column)
        self.item_number = None
        self.lot_id = None
        self.data_access_dict.update({'lot_id': self.lot_id})
        
    def select_item_number(self, new_item_number):
        self.item_number = new_item_number
        self.update_singlet_item_nums()
        
    def select_lot_id(self, new_lot_id):
        self.lot_id = new_lot_id
        self.data_access_dict['lot_id'] = new_lot_id
        self.update_singlet_lot_ids()
        
    def update_singlet_item_nums(self):
        for key, singlet in self.specific.items():
            singlet.select_item_number(self.item_number)
            
    def update_singlet_lot_ids(self):
        for key, singlet in self.specific.items():
            singlet.select_lot_id(self.lot_id)
    
    def has_ids(self, func_name):
        has_item_number = False
        has_lot_id = False
        if self.item_number is not None:
            has_item_number = True
        else:
            print("No item number provided to %s %s." % \
                  (func_name, self.table_class.__name__))
        if self.lot_id is not None:
            has_lot_id = True
        else:
            print("No lot id provided to %s %s." % \
                  (func_name, self.table_class.__name__))
        return has_item_number and has_lot_id
    
    def access(self, session):
        if self.has_ids('access'):
            return self.otm_access(session)
        else:
            return False     

    def query(self, session):
        if self.has_ids('query'):
            self.otm_query(session)
            self.update_singlet_item_nums()
            self.update_singlet_lot_ids()
            
    def remove(self, session):
        if self.has_ids('remove') and self.access(session):
            for key, singlet in self.specific.items():
                singlet.remove(session)
                
    def new(self, session, **new_singlet_identifier):
        if self.has_ids('create new'):
            kwargs = {}
            kwargs.update({'lot_id': self.lot_id})
            kwargs.update(new_singlet_identifier)
            key = self.otm_new(session, **kwargs)
            self.update_singlet_item_nums()   
            self.update_singlet_lot_ids()
            return key
        else:
            return ""

    def query_specs(self, session):
        for key, result in self.specific.items():
            result.query_spec(session)
            
#################################################################################   

class OTMResult_Singlet(OTOResult):
    def __init__(self, table_class, spec_class):
        super().__init__(table_class, spec_class)
        self.identifier_is_called = "result ID"
        self.identifier = None
        self.data_access_dict.update({'id': self.identifier})

    def select_result_id(self, new_result_id):
        self.identifier = new_result_id
        self.data_access_dict['id'] = new_result_id        
    
    def has_ids(self, func_name):
        has_identifier = False
        if self.identifier is not None:
            has_identifier = True
        else:
            print("No %s given to %s %s." % \
                  (self.identifier_is_called,
                   func_name,
                   self.table_class.__name__))            
        return super().has_ids(func_name) and has_identifier

#################################################################################