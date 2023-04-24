import pandas as pd
from ParcelModule import SiteRequests
import time
import numpy as np

buscar_site = SiteRequests()

resultado_final =  []
error_jobs =  []

def get_parcels():
    
    df  = pd.read_csv('land_file.csv' )
    ndf = df.reset_index()
    ndf.columns = ["parcel_number","county","property_address","assessed_owners","market_value" , "item"]
    parcels = []
    for parcel in ndf.iterrows():
        item  = parcel[1].to_dict()
        item['parcel_number'] = item["parcel_number"].replace('"',"").replace("=","")
        parcels.append(item)

    return parcels


def processar_lista_de_parcelas(lista):
    for parcel in lista:
        time.sleep(3)
        try:
            teste  = buscar_site.get_parcel_data(parcel["parcel_number"] , parcel['county'])
            if type(teste) == dict:
                resultado_final.append(teste)
        except Exception as e:
            print ("ERRO")
            print (parcel)
            print (e)
            time.sleep(5)
            teste  = buscar_site.get_parcel_data(parcel["parcel_number"] , parcel['county'])
            if type(teste) == dict:
                resultado_final.append(teste)
            continue

        finally:
            print (len(resultado_final))
                

lista_de_parcelas = np.array_split(get_parcels(), 10)


    
for parcel_lista in lista_de_parcelas:
    processar_lista_de_parcelas(parcel_lista)


pd.DataFrame.from_dict(resultado_final).to_excel('buscas_parcels.xlsx')

