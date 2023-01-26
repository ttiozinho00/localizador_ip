# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import requests
import argparse
import urllib.request
import os

os.system("clear")

def show_result(infos):
    if 'Address' not in infos:
        infos['Address'] = "N/A"
    if 'Street' not in infos:
        infos['Street'] = "N/A"
        
    show_info = ("IP {0}\n".format(infos["IP Address"]) + "Longitude: {0}\n".format(infos["Longitude"]) + "Latitude: {0}\n".format(infos["Latitude"]) + "Estado: {0}\n".format(infos["Region"]) + "Cidade: {0}\n".format(infos["City"]) + "Endereco: {0}\n".format(infos["Address"]) + "Rua: {0}\n".format(infos["Street"]))
    if 'Local Time' in infos:
        show_info += "Horario do Local: {0}\n".format(infos["Local Time"])
    show_info += "Pais: {0}\n".format(infos["Country Code"])
    print (show_info)

def command_line():
    parse = argparse.ArgumentParser(
        description="Get informations of IP Address")    
    parse.add_argument("-i", "--ip", help="IP to get informations")    
    args = parse.parse_args()
    if args.ip:
        get_data(args.ip)
    else:
        parse.print_help()

def get_data(ip_address):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;Win64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
    url = "http://www.geoiptool.com/en/?ip=" + ip_address
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        infos = search_informations(response.text)
        return show_result(infos)
    return None    

def search_informations(data):
    if data is not None:
        informations = BeautifulSoup(data, features="lxml")
        data_ip = informations.findAll("div", {"class": "sidebar-data hidden-xs hidden-sm"})
        return take_informations(data_ip)

def take_informations(bs_data_found):
    data = bs_data_found[0]
    all_informations = data.findAll("span")
    dict_data = {}
    i= 0
    while i < len(all_informations):
        key = str(all_informations[i].string).replace(":","")
        value = str(all_informations[i+1].string)
        dict_data[key] = value
        i += 2
    return dict_data

command_line()
