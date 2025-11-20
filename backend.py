import mysql.connector
import random

class DatabaseManager:
    def __init__(self, host="localhost", user="root", password="password", database="it_inventory"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None

        self.local_storage = []
        self.generate_mock_data()

    def generate_mock_data(self):
        categories = ["Laptop", "Monitor", "Imprimantă", "Server", "Periferic"]
        for i in range(1, 15):
            status = random.choice(["Activ", "În Service", "Casat", "Garanție"])
            location = random.choice(["Birou 101", "Birou 205", "Server Room", "Secretariat"])
            brand = random.choice(['Dell', 'HP', 'Lenovo', 'Canon'])
            self.local_storage.append({
                "id": i,
                "name": f"{brand} Model {random.randint(100, 999)}",
                "category": random.choice(categories),
                "serial": f"SN{random.randint(10000, 99999)}",
                "location": location,
                "status": status
            })

    def connect(self):
        """Stabileste conexiunea la baza de date MySQL."""
        try:
            # self.conn = mysql.connector.connect(
            #     host=self.host, user=self.user, password=self.password, database=self.database
            # )
            return True
        except Exception as e:
            print(f"Eroare conectare DB: {e}")
            return False

    def get_equipment_data(self):
        """Returneaza lista de echipamente."""
        return [
            (x["id"], x["name"], x["category"], x["serial"], x["location"], x["status"])
            for x in self.local_storage
        ]

    def add_equipment(self, name, category, serial, location, status):
        """Adauga un echipament nou in 'baza de date'."""
        new_id = len(self.local_storage) + 1
        
        # TODO: SQL
        
        new_item = {
            "id": new_id,
            "name": name,
            "category": category,
            "serial": serial,
            "location": location,
            "status": status
        }
        self.local_storage.append(new_item)
        print(f"Backend Log: Added item {name}")
        return True

    def update_equipment(self, equip_id, name, category, serial, location, status):
        for item in self.local_storage:
            if str(item["id"]) == str(equip_id):
                item["name"] = name
                item["category"] = category
                item["serial"] = serial
                item["location"] = location
                item["status"] = status
                
                
                print(f"Backend Log: Updated item ID {equip_id}")
                return True
        print(f"Backend Log: Item ID {equip_id} not found for update")
        return False

    def get_stats(self):
        """Calculeaza statistici simple pentru Dashboard."""
        total = len(self.local_storage)
        service = len([x for x in self.local_storage if x["status"] == "În Service"])
        active = len([x for x in self.local_storage if x["status"] == "Activ"])
        return total, active, service