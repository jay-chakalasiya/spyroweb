import pymongo
import pandas as pd


class db_transform():

    def __init__(self, ip_string, db, user_id):
        self.ip_string = ip_string
        self.db = db
        self.user_id = user_id

        self.database = self.connect_to_db()

        col_names = {'fev1': ['DATE', 'FEV1'],
                     'pef': ['DATE', 'PEF'],
                     'o2': ['DATE', 'O2'],
                     'pulse': ['DATE', 'PULSE'],
                     'totalSleepMinutes': ['DATE', 'SLEEP'],
                     'activityGoalPercentage': ['DATE', 'ACTIVITY']
                     }

        self.spiros_data_obj = self.extract_data_from_db('spiros')
        self.spo2_data_obj = self.extract_data_from_db('spo2')
        self.fitbit_data_obj = self.extract_data_from_db('fitbits')

        # self.fev1 = self.trasform_data(self.spiros_data_obj, 'fev1', col_names['fev1'])
        # self.pef = self.trasform_data(self.spiros_data_obj, 'pef', col_names['pef'])
        # self.o2 = self.trasform_data(self.spo2_data_obj, 'o2', col_names['o2'])
        # self.pulse = self.trasform_data(self.spo2_data_obj, 'pulse', col_names['pulse'])
        # self.activity = self.trasform_data(self.fitbit_data_obj, 'activityGoalPercentage', col_names['activityGoalPercentage'])
        # self.sleep = self.trasform_data(self.fitbit_data_obj, 'totalSleepMinutes', col_names['totalSleepMinutes'])
        # self.pulse = self.trasform_data(self.fitbit_data_obj, 'totalSleepMinutes', col_names['totalSleepMinutes'])

        self.raw_dataframes = {
            'O2': self.trasform_data(
                self.spo2_data_obj,
                'o2',
                col_names['o2']),
            'FEV1': self.trasform_data(
                self.spiros_data_obj,
                'fev1',
                col_names['fev1']),
            'PEF': self.trasform_data(
                self.spiros_data_obj,
                'pef',
                col_names['pef']),
            'SLEEP': self.trasform_data(
                self.fitbit_data_obj,
                'totalSleepMinutes',
                col_names['totalSleepMinutes']),
            'ACTIVITY': self.trasform_data(
                self.fitbit_data_obj,
                'activityGoalPercentage',
                col_names['activityGoalPercentage']),
            'PULSE': self.trasform_data(
                self.spo2_data_obj,
                'pulse',
                col_names['pulse'])
        }

        self.data = []
        for i in range(5):
            temp = {}
            for k, v in self.raw_dataframes.items():
                temp[k] = filter_frame(v, i)
            self.data.append(temp)

    def connect_to_db(self):
        import pymongo
        client = pymongo.MongoClient(self.ip_string)
        if client.list_database_names():
            print("Seccessfully Connected")
            return client[self.db]
        else:
            print("Ddin't connect")
            return None

    def extract_data_from_db(self, collection):
        db_coll = self.database[collection]
        # Extract the data
        user_filter = {'user': self.user_id}
        db_data = [item for item in db_coll.find()]
        return db_data

    def trasform_data(self, data_obj, field, col_names):
        import pandas as pd
        data_ls = []
        for data_item in data_obj:
            data_ls.append([data_item['createdAt'].date(), data_item[field]])
        return pd.DataFrame(data_ls, columns=col_names)

def filter_frame(df, value):
    dff = df.copy()
    if value == 1:
        dff = dff[-7:] if len(dff) >= 7 else dff
    elif value == 2:
        dff = dff[-30:] if len(dff) >= 30 else dff
    elif value == 3:
        dff = dff[-90:] if len(dff) >= 90 else dff
    elif value == 4:
        dff = dff[-365:] if len(dff) >= 365 else dff
    return dff

class db_mock():

    def __init__(self):
        import pathlib
        import pandas as pd
        PATH = pathlib.Path(__file__).parent
        DATA_PATH = PATH.joinpath("data").resolve()

        self.raw_dataframes = {
            'O2': pd.read_csv(DATA_PATH.joinpath("data_o2.csv")),
            'FEV1': pd.read_csv(DATA_PATH.joinpath("data_fev1.csv")),
            'PEF': pd.read_csv(DATA_PATH.joinpath("data_pef.csv")),
            'SLEEP': pd.read_csv(DATA_PATH.joinpath("data_sleep.csv")),
            'ACTIVITY': pd.read_csv(DATA_PATH.joinpath("data_activity.csv")),
            'PULSE': pd.read_csv(DATA_PATH.joinpath("data_pulse.csv"))
        }

        self.data = []
        for i in range(5):
            temp = {}
            for k, v in self.raw_dataframes.items():
                temp[k] = filter_frame(v, i)
            self.data.append(temp)

