from sqlalchemy import create_engine
import idealfinder.my_model.process as process
import os, json, pymysql
from pathlib import Path

dataset_path = os.path.join(os.path.dirname(__file__), 'dataset')
gender = ['male', 'female']
app_name = 'idealfinder'
def init_db():
    database_config = json.loads(open(".config_secret/secret.json").read())["django"]["development"]["DATABASES"]["default"]
    host=database_config["HOST"]
    port=int(database_config["PORT"])
    user=database_config["USER"] 
    password=database_config["PASSWORD"]
    db=database_config["NAME"]
    charset='utf8'

    con_str = f'mysql+pymysql://{user}:{password}@{host}/{db}'
    con = create_engine(con_str)
    conn = con.connect()
    for g in gender:
        try:
            process.imageinfo_to_db(os.path.join(dataset_path, g+'.csv'), f'{app_name}_imageinfo', gender=g, preprocess=True, con=conn)
            process.cluster_to_db(os.path.join(dataset_path, f'{g}_cluster.csv'), f'{app_name}_clusterinfo', preprocess=True, con=conn)
            process.embedding_to_db(os.path.join(dataset_path, f'{g}_embeddings.csv'), f'{app_name}_embeddinginfo', preprocess=True, con=conn)
            # process.update_embedding(os.path.join(dataset_path, f'{g}_embeddings.csv'), 'myidol_embeddinginfo', preprocess=True)
        except Exception as e:
            print(e)
            pass
    conn.close()
if __name__ == "__main__":
    init_db()
