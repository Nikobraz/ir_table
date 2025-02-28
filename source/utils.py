import json
import settings
from iracingdataapi.client import irDataClient


def parse_drivers(filepath):
    """
    Converts driver info from json to Member; see models.Member
    :param filepath: Path where json file is
    :return: Array with all members from json file; Empy array if file is empty
    """
    with open(filepath) as data:
        drivers = json.load(data)

        members = []
        for item in drivers['drivers']:
            member = [item['name'], item['id']]
            members.append(member)
            print("Member {0} parsed".format(member))

    return members


def get_data():
    category_list = ['Oval', 'SportCar','Formula','DirtOval','DirtRoad']
    idc = irDataClient(username=settings.USERNAME, password=settings.PASSWORD)
    drivers = parse_drivers('drivers.json')
    listdata = []
    for driver in drivers:
        data = {}
        driver_name = driver[0]
        driver_id = driver[1]
        driver_data = idc.member(cust_id=driver_id, include_licenses=True)
        data['name'] = driver_data["members"][0]["display_name"]
        data['id'] = driver_data["members"][0]["cust_id"]

        for category in category_list:
            data[category + 'SR'] = driver_data['members'][0]['licenses'][category_list.index(category)]['safety_rating']
            data[category + 'License'] = driver_data['members'][0]['licenses'][category_list.index(category)]['group_name']
            try:
                data[category + 'iR'] = driver_data['members'][0]['licenses'][category_list.index(category)]['irating']
            except:
                data[category + 'iR'] = 'No data'
        listdata.append(data)
    return listdata
