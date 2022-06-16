import requests
from bs4 import BeautifulSoup
import os
from service.filters import Filter
from service.send_data import send_data
from colorama import Fore


headers = {
    'User-Agent':'YOUR USER_AGENT',
}

try: #Try open setting file
    with open(f'{os.path.dirname(__file__)}\parsingSetting.txt','r') as file:
        """If setting file is exists"""
        setting = file.readlines() #File setting text
        url = setting[0].replace('Url:','').replace('\n','') 
        tag = setting[1].replace('Tag:','').replace('\n','')
        to_text = setting[2].replace('ToText:','').replace('\n','')
        tag_class = setting[3].replace('TagClass:','')
        server_url = setting[4].replace('ServerUrl:','').replace('\n','')

        if tag_class == 'None':
            tag_class = None
        if server_url == 'None':
            server_url = None


except FileNotFoundError: #If file not exists
    mode = str(input('Program mode 1/2: ')) #Type of mode
    url = str(input('Enter url: ')) #Site url
    tag = str(input('Enter tag: ')) #HTML tag
    tag_class = str(input('Enter class(Maybe blank): ')) #HTML tag class
    to_text = str(input('To text(y,n): ')) #To text select
    server_url = str(input('Enter server url(Blank,without send on server): ')) 

    if mode == '2':   
        """If user select setting mode"""
        with open(f'{os.path.dirname(__file__)}\parsingSetting.txt','w') as file: 
            file.write(f'Url:{url}\n') #Write url
            file.write(f'Tag:{tag}\n') #Write tag
            file.write(f'ToText:{to_text}\n') #Write change convert

            """Write TagClass"""
            if not tag_class:
                file.write(f'TagClass:None\n') 
            else:
                file.write(f'TagClass:{tag_class}\n')
            """Write ServerUrl"""
            if not server_url:
                file.write(f'ServerUrl:None') 
            else:
                file.write(f'ServerUrl:{server_url}')

class Parse:
    def __init__(self,url,tag,tag_class):
        self.url = url
        self.tag = tag
        self.tag_class = tag_class

    def get_html(self):
        #This func return full html code
        r = requests.get(self.url,headers=headers) #Send request 
        return r.text if r.status_code <= 203 else False

    def parsing(self):
        #This func find user tags in html text
        bs = BeautifulSoup(self.get_html(),'html.parser')
        return bs.find_all(self.tag,_class=self.tag_class) if self.tag_class != 'None' else bs.find_all(self.tag)

class ConvertData():
    def __init__(self,elements):
        self.elements = elements
    def convert_to_text(self) -> list:
        #Return only text value from tag
        return [v.get_text() for v in self.elements]
    

#Parse object 
obj = Parse(url,tag,tag_class)
#ConvertData object
obj1 = ConvertData(obj.parsing())

if to_text == 'y':
    data = obj1.convert_to_text()
else:
    data = obj.parsing()

#Filter.data_filter(data)

if server_url: 
    send_data(url,data)
else:
    print(Fore.BLUE,data)










