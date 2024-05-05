from classes import Task

class AnalysisTask(Task):
    def __init__(self, data):
        self.data = data
    
    def shap_values(self):
        self.shape_values = self.bioage_model.shap_values()
    
    def get_prediction(self, data):
        self.prediction = self.bioage_model.predict(data)