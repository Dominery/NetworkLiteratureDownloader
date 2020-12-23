class Settings:
    """
    using Singleton Design to make the class only have an object.
    when instantiating the class if the class has been instantiated earlier it will return the former object.
    So all the objects using this class created will be the same object.
    """
    _instance = None  # to store the object

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Settings, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not self.__dict__:  # if the class has object, it won't init the properties
            self.index_url = "https://www.biqooge.com"
            self.search_url = "https://m.biqooge.com/s.php"
            self.select_max = 5
            self.threads_num = 5
            self.gevent_pool_num = 10
            self.request_head_paras_file = './sources/headers_content'
            self.window_title = 'NetworkLiteratureDownloader'
            self.store_directory_path = None

""""
another choice to create settings class
class Settings:
    # this will create different objects while they will share the same properties
    _shared_dict = {}
    def __new__(cls,*args,**kwargs):
        object = super(Settings,cls).__new__(cls,*args, **kwargs)
        object.__dict__ = cls._shared_dict
        return object
        
    def __init__(self):
        if not self._shared_dict: # make the initialization will start once 
            # properties
"""
