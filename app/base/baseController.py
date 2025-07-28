import json

#TO-DO: SOON
class baseController():
    def __init__(self, main_model, module_name, db, query_params = None) -> None:
        self.main_model = main_model
        self.module_name = module_name
        self.db = db
        # self.columns = self._get_columns()
        self.query_params = query_params.dict() if query_params else {}

        if 'filter' in self.query_params:
            self.query_params['filter'] = json.loads(self.query_params['filter'])
