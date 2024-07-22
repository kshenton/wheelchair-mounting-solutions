import sqlite3

class Wheelchair:
    def __init__(self, model, frame_clamps, mount_location, wheelchair_image):
        self.model = model
        self.frame_clamp_ids = [int(id) for id in frame_clamps.split(',') if id] if frame_clamps else []
        self.mount_location = mount_location
        self.wheelchair_image = wheelchair_image

class AACDevice:
    def __init__(self, make, model, weight, eyegaze, device_image):
        self.make = make
        self.model = model
        self.weight = weight
        self.eyegaze = bool(eyegaze)
        self.device_image = device_image

class Product:
    def __init__(self, id, name, type, manufacturer, weight_capacity, description, url):
        self.id = id
        self.name = name
        self.type = type
        self.manufacturer = manufacturer
        self.weight_capacity = weight_capacity
        self.description = description
        self.url = url

def load_data():
    conn = sqlite3.connect('mounting_solutions.db')
    cursor = conn.cursor()

    wheelchairs = []
    cursor.execute("SELECT model, frame_clamps, mount_location, wheelchair_image FROM wheelchairs")
    for row in cursor.fetchall():
        wheelchairs.append(Wheelchair(*row))

    aac_devices = []
    cursor.execute("SELECT make, model, weight, eyegaze, device_image FROM aac_devices")
    for row in cursor.fetchall():
        aac_devices.append(AACDevice(*row))

    products = {}
    cursor.execute("SELECT id, name, type, manufacturer, weight_capacity, description, url FROM products")
    for row in cursor.fetchall():
        products[row[0]] = Product(*row)

    conn.close()

    return wheelchairs, aac_devices, products