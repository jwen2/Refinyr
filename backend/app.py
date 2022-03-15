from flask import Flask
import pandas as pd
# import docker

class API:
    # client = null

    # def connectToClient():
        # self.client = docker.DockerClient(base_url='')

    @app.route('/api/upload', method=["POST"])
    def upload(csvFile):
        volume = client.volumes.get('{volume_id_here}')

    @app.route('/api/load', method=["GET"])
    def load(csvFile):
        df = pd.read_csv(csvFile)
        return df

    def isNullAny(df):
        return df.isnull().any()

    def isNullColumn(columnName, df):
        return df[columnName].isnull()

    def removeNullsFromDF(df):
        return df.dropna()

