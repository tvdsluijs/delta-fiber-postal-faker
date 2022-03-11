#!python

# postcode.tech for API

# er zit wel iets van handwerk aan dit script!
# belangrijkste is dat je even de postcodes.csv vult
# voor mijn dorp heb ik de gegevens hiervandaan gehaald
# https://postcodebijadres.nl/4443
# even de straatnamen er uit en alles splitsen met een ;
# zodat je de volgende regels krijgt.
# 4443AA;1;39
# postcode;starthuisnummer;eindhuisnummer
# daarna even een API token halen bij postcode.tech
# en die plaats je in een config.ini (voorbeeld: config_sample.ini)
# daarin staat dan zo iets als:
# [postcode_api]
# token: 49102cb3-07ce-4e42-a0b2-742663393a54 (dit is een nep token)
# vergeet niet om een .venv op te zetten :-)
# python -m venv .venv
# en daarna (als je in je venv werkt)
# pip install -r requirements.txt

import sys
import csv
import os
import configparser
import traceback

import requests
from requests.structures import CaseInsensitiveDict

import sqlite3

# from json.tool import main
from time import sleep
from random import randint

from tqdm.auto import trange
from tqdm import tqdm

class DeltaFiber():
    def __init__(self) -> None:
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.config_file = os.path.join(self.dir_path, './config.ini')
        self.token = None
        self.conn = None
        self.c = None
        self.config = None
        self.headers = CaseInsensitiveDict()
        self.csv = "postcodes.csv"
        self.db = "used_postalcodes.db"
        self.delta_url = "https://www.deltafibernetwerk.nl/umbraco/api/zipcodecheckapi/zipcodecheck"

        self.getToken()
        self.setPostcodeHeaders()
        self.createTable()

        pass

    def readConfig(self) -> None:
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)

    def getToken(self) -> None:
        try:
            self.readConfig()
            self.token = self.config['postcode_api']['token']
        except Exception as e:
            sys.exit(f"We have an error: {e}\n", traceback.format_exc())

    def databaseConnect(self) -> None:
        try:
            self.conn = sqlite3.connect(self.db)
            self.c = self.conn.cursor()
        except Exception as e:
            sys.exit(f"We have an error: {e}\n", traceback.format_exc())

    def createTable(self) -> None:
        if not self.conn:
           self.databaseConnect()
        try:
            self.c.execute('''
                            CREATE TABLE IF NOT EXISTS postalcodes
                            ([postalcode] STRING, [housenumber] INT, [message] STRING, [GAAction] STRING, [GALabel] STRING,
                            PRIMARY KEY (postalcode, housenumber))
                            ''')
        # HELAAS
            self.conn.commit()
        except Exception as e:
            sys.exit(f"We have an error: {e}\n", traceback.format_exc())

    def setPostcodeHeaders(self) -> None:
        self.headers["Accept"] = "application/json"
        self.headers["Authorization"] = f"Bearer {self.token}"

    def savePostCodeNr(self, zipcode:str = None, housenumber:int = None, message:str = "", gaaction:str = "", galabel:str = None) -> None:
        if not self.conn:
           self.databaseConnect()
        try:
            self.c.execute(f"""
                    INSERT INTO postalcodes (postalcode, housenumber, message, GAAction, GALabel)
                    VALUES ('{zipcode}',{housenumber},'{message}', '{gaaction}', '{galabel}')
            """)
            self.conn.commit()
        except Exception as e:
            sys.exit(f"We have an error: {e}\n", traceback.format_exc())

    def selectPostCodeNr(self, zipcode:str = None, housenumber:int = None) -> str:
        if not self.conn:
           self.databaseConnect()
        try:
            self.c.execute(f"""
            SELECT COUNT(*) as nr
            FROM postalcodes
            WHERE postalcode = '{zipcode}'
            AND housenumber = {housenumber}
            """)
            data = self.c.fetchone()
            return data[0]
        except Exception as e:
            sys.exit(f"We have an error: {e}\n", traceback.format_exc())

    def dropDatabase(self) -> None:
        if not self.conn:
           self.databaseConnect()
        try:
            self.c.execute("DROP TABLE IF EXISTS postalcodes;")
        except Exception as e:
            sys.exit(f"We have an error: {e}\n", traceback.format_exc())

    def checkDelta(self, zipcode:str = None, housenumber:int = None ) -> None:
        try:
            data_object = {'zipcode': zipcode, 'housenumber': housenumber, 'housenumberextension': "", 'area': "", 'IsExtended': 'false'}
            x = requests.post(self.delta_url, data = data_object)
            return x.json()
        except Exception as e:
            sys.exit(f"We have an error: {e}\n", traceback.format_exc())

    def checkPostcode(self, zipcode:str = None, housenumber:int = None ) -> bool:
                    url = f"https://postcode.tech/api/v1/postcode?postcode={zipcode}&number={housenumber}"
                    resp = requests.get(url, headers=self.headers)
                    data = resp.json()
                    try:
                        if data['message'] == "No result for this combination.":
                            return False
                    except KeyError as e:
                        pass

                    try:
                        if data['street'] is not None:
                            return True
                    except KeyError as e:
                        sys.exit(f"We have an error: {e}\n", traceback.format_exc())

    def processCSVData(self) -> None:

        with open(self.csv) as csv_file:
            lines = len(csv_file.readlines())

        with open(self.csv, mode='r') as file:
            reader = csv.reader(file)
            for row in tqdm(reader, total=lines, desc="CSV File Process"):
                items = row[0].split(";")
                postcode = items[0]
                huis_start = int(items[1])
                huis_stop = int(items[2])

                for i in tqdm(range(huis_start, huis_stop), desc=f"{postcode} from {huis_start} to {huis_stop}", leave=False):
                    # does it exist in de database? No is process
                    if not self.selectPostCodeNr(zipcode=postcode, housenumber=i):
                        # We have to wait a bit as the postcode check does not let you check more then one every sec
                        for sec in tqdm(range(2, 10), desc="Waiting for next check!", leave=False, bar_format='Waiting .... {remaining}'):
                            sleep(1)

                        # does it exist in the Postalbook? Yes is process
                        if self.checkPostcode(zipcode=postcode, housenumber=i):
                            #check in deltafiber site
                            data = self.checkDelta(zipcode=postcode, housenumber=i)

                            #save data in sqlite database
                            self.savePostCodeNr(zipcode=postcode, housenumber=i, message=data['Title'], gaaction=data['GAAction'], galabel=data['GALabel'])
                        else:
                            # if the postcode / nr does not exist just save in the database it does not exsist!
                            self.savePostCodeNr(zipcode=postcode, housenumber=i, message="Postal / House nr does not exist!", gaaction="", galabel="")

if __name__ == "__main__":
    df = DeltaFiber()
    df.processCSVData()