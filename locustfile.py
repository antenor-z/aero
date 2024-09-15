from locust import HttpUser, task, between
import random

icaos = ["SBRJ", "SBGR", "SBPA", "SBFZ", "SBRF", "SBGO", 
         "SBKP", "SBSG", "SBSL", "SBSV", "SBCF", "SBBR"]

class FastAPIUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def load_airport_menu(self):
        self.client.get("/")

    @task
    def load_airport_info(self):
        icao = random.choice(icaos)
        self.client.get(f"/info/{icao}")  

    @task
    def load_taf_info(self):
        icao = random.choice(icaos)
        self.client.get(f"/taf/{icao}")  

    @task
    def load_wind(self):
        self.client.get("/wind/")

    @task
    def calculate_windcalc(self):
        self.client.get("/windcalc/?runway_head=90&wind_dir=100&wind_speed=15")

    @task
    def load_descent(self):
        self.client.get("/descent")

    @task
    def load_history(self):
        icao = random.choice(icaos)
        self.client.get(f"/history/{icao}")