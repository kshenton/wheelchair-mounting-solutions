import csv
import os
from data_models import Wheelchair, AACDevice, Mount

def load_wheelchairs(filename):
    wheelchairs = []
    with open(filename, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames
        print("CSV Headers:", headers)  # Debugging line to print headers
        for row in reader:
            frame_clamps = row['frame_clamps'].split(',')
            wheelchairs.append(Wheelchair(row['model'], frame_clamps, row['location']))
    return wheelchairs

def load_aac_devices(filename):
    aac_devices = []
    with open(filename, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            aac_devices.append(AACDevice(row['name'], float(row['weight'])))
    return aac_devices

def load_mounts(filename):
    mounts = []
    with open(filename, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            mounts.append(Mount(row['name'], float(row['weight_capacity'])))
    return mounts

def load_product_urls(filename):
    product_urls = {}
    with open(filename, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            product_urls[row['product_name']] = row['url']
    return product_urls

def load_data(app):
    current_dir = os.path.dirname(__file__)
    wheelchairs_csv = os.path.join(current_dir, 'wheelchairs.csv')
    aac_devices_csv = os.path.join(current_dir, 'aac_devices.csv')
    mounts_csv = os.path.join(current_dir, 'mounts.csv')
    product_urls_csv = os.path.join(current_dir, 'product_urls.csv')

    app.wheelchairs = load_wheelchairs(wheelchairs_csv)
    app.aac_devices = load_aac_devices(aac_devices_csv)
    app.mounts = load_mounts(mounts_csv)
    app.product_urls = load_product_urls(product_urls_csv)