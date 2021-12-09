import datetime
import pandas as pd
import os

MODEL_PATH  = os.path.join(os.path.dirname(__file__))
DATASET_PATH = os.path.join(os.path.dirname(__file__), 'dataset')
DB_PATH = os.path.join(os.path.dirname(MODEL_PATH), 'db.sqlite3')



def imageinfo_to_db(path, target_table, gender=None, preprocess=False, db=DB_PATH, con=None):
    db_df = pd.read_csv(path)
    if preprocess:
        db_df['format'] = db_df['file_name'].apply(lambda x: x.split('.')[1])
        db_df['file_name'] = db_df['file_name'].apply(lambda x: x.split('.')[0])
        db_df['gender'] = db_df['format'].apply(lambda x: gender)
        db_df['created_at'] = db_df['gender'].apply(lambda x: datetime.datetime.now())
        db_df['updated_at'] = db_df['gender'].apply(lambda x: datetime.datetime.now())
        # db_df.to_csv(f'{gender}_modified.csv')
    print(db_df)
    db_df.to_sql(target_table, con, if_exists='append', index=False)
    # con.close()

def cluster_to_db(path, target_table, preprocess=False, db=DB_PATH, con=None):
    db_df = pd.read_csv(path)
    if preprocess:
        db_df['cluster'] = db_df.apply(lambda x: str(x['cluster_1']) + str(x['cluster_2']) + str(x['cluster_3']), axis=1)
    db_df = db_df.loc[:, ['image_id', 'cluster']]
    print(db_df)
    db_df.to_sql(target_table, con, if_exists='append', index=False)
    # con.close()

def embedding_to_db(path, target_table, preprocess=False, db=DB_PATH, con=None):
    db_df = pd.read_csv(path)
    if preprocess:
        db_df['image_id'] = db_df['image_id'].apply(lambda x: int(x))
        db_df['embedding'] = db_df.iloc[:, 1:129].apply(lambda x: str(list(x)), axis=1)
    db_df = db_df.loc[:, ['image_id', 'embedding']]
    print(db_df)
    db_df.to_sql(target_table, con, if_exists='append', index=False)
    # con.close()

