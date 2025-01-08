""" Vehicle Assembly Line Management System """

import random
import time

class Vehicle:
    stages = ["Chassis Assembly",
              "Engine Installation",
              "Transmission Installation",
              "Electrical Wiring",
              "Interior Assembly",
              "Paint Shop",
              "Quality Control"]

    def __init__(self, vehicle_id, model, color):
        self.vehicle_id = vehicle_id
        self.model = model
        self.color = color
        self.current_stage = 0
        self.is_completed = False
        self.start_time = time.time()
        self.stage_times = []

    def move_to_next_stage(self):
        if self.current_stage < len(Vehicle.stages) - 1:
            self.stage_times.append(time.time() - self.start_time)
            self.current_stage += 1
            self.start_time = time.time()
        else:
            self.is_completed = True
            self.stage_times.append(time.time() - self.start_time)

    def get_required_parts(self):
        return AssemblyLine.required_parts[Vehicle.stages[self.current_stage]]


class Excavator(Vehicle):
    stages = ["Chassis Assembly",
              "Engine Installation",
              "Hydraulic Installation",
              "Electrical Wiring",
              "Cabin Assembly",
              "Paint Shop",
              "Quality Control"]

    def get_required_parts(self):
        return AssemblyLine.required_parts[Excavator.stages[self.current_stage]]


class Bulldozer(Vehicle):
    stages = ["Chassis Assembly",
              "Engine Installation",
              "Transmission Installation",
              "Electrical Wiring",
              "Blade Assembly",
              "Paint Shop",
              "Quality Control"]

    def get_required_parts(self):
        return AssemblyLine.required_parts[Bulldozer.stages[self.current_stage]]


class Part:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    def use(self, amount):
        self.quantity -= amount


class AssemblyLine:
    required_parts = {
        "Chassis Assembly": ["Chassis", "Wheels"],
        "Engine Installation": ["Engine"],
        "Transmission Installation": ["Transmission"],
        "Hydraulic Installation": ["Hydraulics"],
        "Electrical Wiring": ["Wiring"],
        "Cabin Assembly": ["Cabin"],
        "Blade Assembly": ["Blade"],
        "Interior Assembly": ["Seats"],
        "Paint Shop": ["Paint"],
        "Quality Control": []
    }

    delay_probabilities = {
        "Chassis Assembly": 0.05,
        "Engine Installation": 0.1,
        "Transmission Installation": 0.38,
        "Electrical Wiring": 0.12,
        "Interior Assembly": 0.07,
        "Paint Shop": 0.15,
        "Quality Control": 0.22
    }

    delay_types = ["Equipment Malfunction",
                   "Worker Absenteeism",
                   "Part Shortage"]

    def __init__(self, parts_inventory):
        self.vehicles = []
        self.parts_inventory = parts_inventory
        self.completed_vehicles = 0
        self.total_delays = 0
        self.total_delay_time = 0

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def check_parts(self, required_parts):
        for part in required_parts:
            if self.parts_inventory[part].quantity <= 0:
                return False
        return True

    def use_parts(self, required_parts):
        for part in required_parts:
            self.parts_inventory[part].use(1)

    def simulate_delay(self, vehicle, id):
        if random.random() <= AssemblyLine.delay_probabilities[Vehicle.stages[vehicle.current_stage]]:
            delay_type = random.choice(AssemblyLine.delay_types)
            delay_time = random.randint(1, 10)
            self.total_delays += 1
            self.total_delay_time += delay_time
            print(
                f"Vehicle {id} encountered delay at {Vehicle.stages[vehicle.current_stage]} due to {delay_type}. Waiting for {delay_time} hours.")
            time.sleep(delay_time * 0.1)

    def optimize_vehicles(self):
        def vehicle_priority(vehicle):
            current_stage = vehicle.current_stage
            parts_available = self.check_parts(vehicle.get_required_parts())
            return current_stage, parts_available

        self.vehicles.sort(key=vehicle_priority, reverse=True)

    def run(self):
        while self.vehicles:
            self.optimize_vehicles()
            for vehicle in self.vehicles:
                # check state and parts
                if not vehicle.is_completed and self.check_parts(vehicle.get_required_parts()):
                    self.simulate_delay(vehicle, vehicle.vehicle_id)
                    self.use_parts(vehicle.get_required_parts())
                    vehicle.move_to_next_stage()
                    print(f"Vehicle {vehicle.vehicle_id} moved to {Vehicle.stages[vehicle.current_stage]}")
                    if vehicle.is_completed:
                        self.completed_vehicles += 1
                elif not self.check_parts(vehicle.get_required_parts()):
                    print(f"Not enough parts for {Vehicle.stages[vehicle.current_stage]}")
            self.vehicles = [v for v in self.vehicles if not v.is_completed]

        # Report statistics after the run is complete
        self.report_statistics()

    def report_statistics(self):
        print("\n--- Production Statistics ---")
        print(f"Total Vehicles Completed: {self.completed_vehicles}")
        print(f"Total Delays Encountered: {self.total_delays}")
        print(f"Total Delay Time: {self.total_delay_time} Hours")

def user_input():
    """Gets user input for adding vehicles."""
    vehicle_id = input("Enter Vehicle ID: ")
    model = input("Enter Vehicle Model: ")
    color = input("Enter Vehicle Color: ")
    vehicle_type = input("Enter Vehicle Type (Excavator/Bulldozer/Other): ")
    return vehicle_id, model, color, vehicle_type


def main():
    parts_inventory = {
        "Chassis": Part("Chassis", 10),
        "Wheels": Part("Wheels", 40),
        "Engine": Part("Engine", 10),
        "Transmission": Part("Transmission", 10),
        "Hydraulics": Part("Hydraulics", 10),
        "Wiring": Part("Wiring", 10),
        "Cabin": Part("Cabin", 5),
        "Blade": Part("Blade", 5),
        "Seats": Part("Seats", 20),
        "Paint": Part("Paint", 10)
    }

    assembly_line = AssemblyLine(parts_inventory)

    while True:
        print("\n1. Add Vehicle\n2. Run Simulation\n3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            vehicle_id, model, color, vehicle_type = user_input()
            if vehicle_type.lower() == "excavator":
                vehicle = Excavator(vehicle_id, model, color)
            elif vehicle_type.lower() == "bulldozer":
                vehicle = Bulldozer(vehicle_id, model, color)
            else:
                vehicle = Vehicle(vehicle_id, model, color)
            assembly_line.add_vehicle(vehicle)
        elif choice == "2":
            assembly_line.run()
        elif choice == "3":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
