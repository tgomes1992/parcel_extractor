import pandas as pd
from ParcelModule import SiteRequests
import time
import numpy as np
import asyncio
import aiohttp
from ParcelModule.AsyncSiteRequests import AsyncSiteRequests
import requests

buscar_site = AsyncSiteRequests()

resultado_final =  []
error_jobs =  []

def get_parcels():    
    df  = pd.read_excel('land_file_versao_excel.xlsx' ,  dtype=str )
    df.columns = ["parcel_number","county","property_address","assessed_owners","market_value" ]
    parcels = []    
    for parcel in df.iterrows():
        item  = parcel[1].to_dict()
        parcels.append(item)
    return parcels




def processar_lista_de_parcelas(lista):
    rotinas = []
    for parcel in lista:
        try:
            teste  = buscar_site.get_parcel_data(parcel["parcel_number"] , parcel['county'])
            if type(teste) == dict:
                resultado_final.append(teste)
        except Exception as e:
            pass




async def main():
    parcels = get_parcels()
    with requests.session() as session:
        coroutines = []
        for parcel in parcels:
            coroutines.append(buscar_site.get_parcel_data(session,parcel['parcel_number'] ,parcel['county']))
        data = await asyncio.gather(*coroutines)
        df = pd.DataFrame.from_dict(data)
        df.to_excel("parcels_result.xlsx")
    






asyncio.run(buscar_site.busca_requests(get_parcels()))


