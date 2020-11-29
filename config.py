class graph_config():

    def __init__(self):

        self.cols = {
            'index_col': 'DATE',
            'O2': 'O2',
            'FEV1': 'FEV1',
            'PEF': 'PEF',
            'SLEEP': 'SLEEP',
            'ACTIVITY': 'ACTIVITY',
            'PULSE': 'PULSE'
        }

        self.titles = {
            'LUNG_GRAPH': 'Lung Functions',
            'O2': 'Oxygen Saturation',
            'PULSE': 'Heart Beats',
            'ACTIVITY': 'Active Minutes',
            'SLEEP': 'Sleep Minutes'
        }
