import sqlite3

class Wheelchair:
    def __init__(self, model, frame_clamps, mount_location):
        self.model = model
        self.frame_clamps = frame_clamps.split(',')
        self.mount_location = mount_location

class AACDevice:
    def __init__(self, name, weight, eyegaze):
        self.name = name
        self.weight = weight
        self.eyegaze = bool(eyegaze)  # Convert to boolean

class Mount:
    def __init__(self, name, weight_capacity):
        self.name = name
        self.weight_capacity = weight_capacity

def load_data():
    conn = sqlite3.connect('mounting_solutions.db')
    cursor = conn.cursor()

    wheelchairs = []
    cursor.execute("SELECT model, frame_clamps, location FROM wheelchairs")
    for row in cursor.fetchall():
        wheelchairs.append(Wheelchair(*row))

    aac_devices = []
    cursor.execute("SELECT name, weight, eyegaze FROM aac_devices")
    for row in cursor.fetchall():
        aac_devices.append(AACDevice(*row))

    mounts = []
    cursor.execute("SELECT name, weight_capacity FROM mounts")
    for row in cursor.fetchall():
        mounts.append(Mount(*row))

    product_urls = {}
    cursor.execute("SELECT product_name, url FROM product_urls")
    for row in cursor.fetchall():
        product_urls[row[0]] = row[1]

    conn.close()

    return wheelchairs, aac_devices, mounts, product_urls