import requests
from bs4 import BeautifulSoup
import json
import time


class SiteRequests():

    counties = {
    'Adams' : 0 , 
    'Alcorn' : 1 , 
    'Amite' : 2 , 
    'Attala' : 3 , 
    'Benton' : 4 , 
    'Bolivar' : 5 , 
    'Calhoun' : 6 , 
    'Carroll' : 7 , 
    'Chickasaw' : 8 , 
    'Choctaw' : 9 , 
    'Claiborne' : 10 , 
    'Clarke' : 11 , 
    'Clay' : 12 , 
    'Coahoma' : 13 , 
    'Copiah' : 14 , 
    'Covington' : 15 , 
    'DeSoto' : 16 , 
    'Forrest' : 17 , 
    'Franklin' : 18 , 
    'George' : 19 , 
    'Greene' : 20 , 
    'Grenada' : 21 , 
    'Hancock' : 22 , 
    'Harrison' : 23 , 
    'Hinds' : 24 , 
    'Holmes' : 25 , 
    'Humphreys' : 26 , 
    'Issaquena' : 27 , 
    'Itawamba' : 28 , 
    'Jackson' : 29 , 
    'Jasper' : 30 , 
    'Jefferson' : 31 , 
    'Jefferson Davis' : 32 , 
    'Jones' : 33 , 
    'Kemper' : 34 , 
    'Lafayette' : 35 , 
    'Lamar' : 36 , 
    'Lauderdale' : 37 , 
    'Lawrence' : 38 , 
    'Leake' : 39 , 
    'Lee' : 40 , 
    'Leflore' : 41 , 
    'Lincoln' : 42 , 
    'Lowndes' : 43 , 
    'Madison' : 44 , 
    'Marion' : 45 , 
    'Marshall' : 46 , 
    'Monroe' : 47 , 
    'Montgomery' : 48 , 
    'Neshoba' : 49 , 
    'Newton' : 50 , 
    'Noxubee' : 51 , 
    'Oktibbeha' : 52 , 
    'Panola' : 53 , 
    'Pearl River' : 54 , 
    'Perry' : 55 , 
    'Pike' : 56 , 
    'Pontotoc' : 57 , 
    'Prentiss' : 58 , 
    'Quitman' : 59 , 
    'Rankin' : 60 , 
    'Scott' : 61 , 
    'Sharkey' : 62 , 
    'Simpson' : 63 , 
    'Smith' : 64 , 
    'Stone' : 65 , 
    'Sunflower' : 66 , 
    'Tallahatchie' : 67 , 
    'Tate' : 68 , 
    'Tippah' : 69 , 
    'Tishomingo' : 70 , 
    'Tunica' : 71 , 
    'Union' : 72 , 
    'Walthall' : 73 , 
    'Warren' : 74 , 
    'Washington' : 75 , 
    'Wayne' : 76 , 
    'Webster' : 77 , 
    'Wilkinson' : 78 , 
    'Winston' : 79 , 
    'Yalobusha' : 80 , 
    'Yazoo' : 81 , 
    }

    def __init__(self):
        self.starturl = "https://www.sos.ms.gov/tfsearch/default.aspx"
        self.processsearch = "https://www.sos.ms.gov/tfsearch/LandsSearch.asmx/ProcessSearch"
        self.searchdetail  =  "https://www.sos.ms.gov/tfsearch/LandsSearch.asmx/ProcessSearchDetail"
        self.headers = {
                "content-type": "application/json"
                }



    def get_process_search_body(self, parcel , county ):
        body_teste = {"tmpCounties": str(self.counties[county]),"tmpSection":"","tmpTownship":"","tmpTownshipDir":"",
              "tmpRange":"","tmpRangeDir":"","tmpSubdivision":"","tmpLine1":"","tmpLine2":"",
              "tmpCity":"","tmpZipcode":"","tmpParcelNum":parcel,"tmpPPIN":"","tmpValueStart":"",
              "tmpValueEnd":"","tmpAssessedOwner":"","tmpLegalDesc":"","tmpAddrSearchType":"C",
              "tmpLegalSearchType":"E","startingNumber":0,"numberToDisplay":50}
        
        return json.dumps(body_teste)


    def get_parcel_detail_body(self, parcelid):
        id = {"tmpParcelId":parcelid}
        id_json = json.dumps(id)
        return id_json
    

    def parcel_decoded_body(self, lista):
        BASE_DICT = {
                "county":  lista[25] , 
                'tax_sale_date': lista[30] ,  
                'tax_year': lista[31] ,
                'parcel_number': lista[26] ,
                'ppin': lista[27] ,
                'assessed_owners': lista[28], 
                'legal_description': lista[18] ,
                'section': lista[8] , 
                'township': lista[9]  , 
                'range':lista[10]  , 
                'acres': lista[13] ,  
                'dimensions':lista[17] ,
                'subdvision': "" ,
                'lot' :  "" , 
                'block': "" , 
                'phase_part': "" ,  
                'property_address': f"{lista[20]} {lista[23]} {lista[24]}",  
                'blighted': lista[3]  , 
                'tax_district_code': lista[4] , 
                'taxes_and_fees_owed': lista[5] ,
                'last_report_market_value': lista[1] , 
                'county_broker': "" , 
                'lands_representative': lista[32] , 
                'chancery_clerk': lista[33] ,
                'tax_assessor': lista[34] ,
            }
        return BASE_DICT


    def get_parcel_data(self ,  parcel, county):
        with requests.session() as s:
            try:
                r = s.get(self.starturl)
                r = s.post(self.processsearch , self.get_process_search_body(parcel, county) ,  headers=self.headers)
                buscar_parcel = r.content
                parcel_id = r.json()['d'].split("%")[0]
                r = s.post(self.searchdetail , self.get_parcel_detail_body(parcel_id) , headers=self.headers)
                resposta_final = r.json()
                s.close()
                return self.parcel_decoded_body(r.json()['d'].split("%"))
            except Exception as e:
                print (parcel , county)
                print (self.get_process_search_body(parcel, county))
                # parcel_id = r.json()['d'].split("%")[0]
                print (buscar_parcel)
                print (parcel_id)
                print (resposta_final)
                print (e)





    