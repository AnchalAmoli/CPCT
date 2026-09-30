# python stuff
from datetime import datetime, timezone


#MODULE1
class Patient:
    def __init__(self, patient_id, name, age, cancer_type, stage):
        self.patient_id = str(patient_id).strip()
        self.name = name.strip()

        # quick validation check
        if age < 0 or age > 120:
            raise ValueError(f"Age {age} is not valid.")
        self.age = age

        self.cancer_type = cancer_type.strip()

        # valid stages list - missed some rare ones prob but this works for now
        valid_stages = ["0", "1", "1a", "1b", "2", "2a", "2b", "3", "3a", "3b", "3c", "4"]
        if str(stage).lower() not in valid_stages:
            raise ValueError(f"Stage '{stage}' is not recognized.")
        self.stage = str(stage).upper()

        self.doctor = None
        self.vitals_history = []
        self.treatments = []

#MODULE2
    def assign_doctor(self, doc_obj):
      
        self.doctor = doc_obj

    def add_vitals(self, weight, pain_score, notes=""):
        if pain_score < 0 or pain_score > 10:
            raise ValueError("Pain score must be between 0 and 10.")

        weight_warning = False
        
        # Check if they lost too much weight rapidly
        if len(self.vitals_history) > 0:
            last_weight = self.vitals_history[-1]["weight"]
            weight_diff = last_weight - float(weight)
            if weight_diff > 2.0:
                weight_warning = True

        entry = {
            "date": datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M"),
            "weight": float(weight),
            "pain": int(pain_score),
            "notes": notes,
            "weight_warning": weight_warning
        }
        
        self.vitals_history.append(entry)
        return weight_warning

class Doctor:
    def __init__(self, doctor_id, name, specialty):
        self.doctor_id = str(doctor_id).strip()
        self.name = name.strip()
        self.specialty = specialty.strip()
        self.patients = []

    def add_patient(self, p):
        if p not in self.patients:
            self.patients.append(p)

class Treatment:
    def __init__(self, treatment_id, name, scheduled_date):
        self.treatment_id = treatment_id
        self.name = name
        self.scheduled_date = scheduled_date
        self.status = "Scheduled"

class TrackerSystem:
    def __init__(self):
        self.patients = {}
        self.doctors = {}
        self.logs = []

#MODULE3
    def log_message(self, tag, text):
        now = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{now}] [{tag}] {text}"
        self.logs.append(entry)
        # print(entry)  # uncomment this if debugging logs later

    def add_patient(self, patient_id, name, age, cancer_type, stage):
        if patient_id in self.patients:
            self.log_message("ERROR", f"Patient ID '{patient_id}' already exists.")
            return False, "Patient ID already exists."

        try:
            p = Patient(patient_id, name, age, cancer_type, stage)
            self.patients[patient_id] = p
            self.log_message("INFO", f"Added patient '{name}'.")
            return True, f"Patient {name} added successfully."
        except ValueError as err:
            self.log_message("ERROR", str(err))
            return False, str(err)

    def add_doctor(self, doctor_id, name, specialty):
        if doctor_id in self.doctors:
            self.log_message("ERROR", f"Doctor ID '{doctor_id}' already exists.")
            return False, "Doctor ID already exists."

        doc = Doctor(doctor_id, name, specialty)
        self.doctors[doctor_id] = doc
        self.log_message("INFO", f"Added Dr. {name}.")
        return True, f"Dr. {name} added successfully."

    def assign_doctor_to_patient(self, patient_id, doctor_id):
        p = self.patients.get(patient_id)
        d = self.doctors.get(doctor_id)

        if not p:
            return False, "Patient not found."
        if not d:
            return False, "Doctor not found."

        p.assign_doctor(d)
        d.add_patient(p)
        self.log_message("INFO", f"Assigned Dr. {d.name} to Patient {p.name}.")
        return True, f"Assigned Dr. {d.name} to {p.name}."

# helper function for printing, formatting looks okay
#MODULE4
def show_patient_details(patient):
    print("\n" + "=" * 45)
    print(f" PATIENT REPORT - ID: {patient.patient_id}")
    print("=" * 45)
    print(f" Name       : {patient.name}")
    print(f" Age        : {patient.age}")
    print(f" Condition  : {patient.cancer_type} (Stage {patient.stage})")

    if patient.doctor != None:
        print(f" Doctor     : Dr. {patient.doctor.name} ({patient.doctor.specialty})")
    else:
        print(" Doctor     : Not Assigned")

    print("\nScheduled Treatments:")
    if len(patient.treatments) > 0:
        for t in patient.treatments:
            print(f"   • [{t.scheduled_date}] {t.name} (Status: {t.status})")
    else:
        print("   • No treatments scheduled.")

    print("\nVitals & Notes:")
    if len(patient.vitals_history) > 0:
        for v in patient.vitals_history:
            warning = " [!] WARNING: Sudden weight drop!" if v["weight_warning"] else ""
            print(f"   • {v['date']} | Weight: {v['weight']} kg | Pain: {v['pain']}/10{warning}")
            if v["notes"]:
                print(f"     Notes: {v['notes']}")
    else:
        print("   • No vitals recorded.")
    print("=" * 45)

def run_app():
    system = TrackerSystem()

    # dummy data to test quickly without typing every time
    system.add_doctor("D101", "Amina Roy", "Oncology")
    system.add_patient("P101", "Elena Rostova", 48, "Breast Cancer", "2b")
    system.assign_doctor_to_patient("P101", "D101")

#MODULE5
    while True:
        print("\n--- CANCER CARE TRACKER ---")
        print("1. Add Doctor")
        print("2. Add Patient")
        print("3. Assign Doctor to Patient")
        print("4. Record Vitals")
        print("5. Add Treatment")
        print("6. View Patient Report")
        print("7. Exit")

        choice = input("\nChoose an option (1-7): ").strip()

        if choice == "1":
            d_id = input("Doctor ID: ")
            name = input("Doctor Name: ")
            spec = input("Specialty: ")
            _, msg = system.add_doctor(d_id, name, spec)
            print(f"Result: {msg}")

        elif choice == "2":
            p_id = input("Patient ID: ")
            name = input("Patient Name: ")
            try:
                age = int(input("Age: "))
            except ValueError:
                print("Result: Age must be a number.")
                continue
            c_type = input("Cancer Type: ")
            stage = input("Stage (e.g. 1, 2b, 4): ")

            _, msg = system.add_patient(p_id, name, age, c_type, stage)
            print(f"Result: {msg}")

        elif choice == "3":
            p_id = input("Patient ID: ")
            d_id = input("Doctor ID: ")
            _, msg = system.assign_doctor_to_patient(p_id, d_id)
            print(f"Result: {msg}")

        elif choice == "4":
            p_id = input("Patient ID: ").strip()
            p = system.patients.get(p_id)
            if not p:
                print("Result: Patient not found.")
                continue
            try:
                wt = float(input("Weight (kg): "))
                pain = int(input("Pain level (0-10): "))
                notes = input("Notes: ")
                has_warning = p.add_vitals(wt, pain, notes)
                print(f"Result: Vitals recorded for {p.name}.")
                if has_warning:
                    print("Alert: Weight dropped by more than 2 kg!")
            except ValueError as err:
                print(f"Result: Invalid input - {err}")

        elif choice == "5":
            p_id = input("Patient ID: ").strip()
            p = system.patients.get(p_id)
            if not p:
                print("Result: Patient not found.")
                continue

            t_id = input("Treatment ID: ")
            t_name = input("Treatment Name: ")
            t_date = input("Date (YYYY-MM-DD): ")

            t = Treatment(t_id, t_name, t_date)
            p.treatments.append(t)
            print(f"Result: Treatment added for {p.name}.")

        elif choice == "6":
            p_id = input("Enter Patient ID: ").strip()
            p = system.patients.get(p_id)
            if p != None:
                show_patient_details(p)
            else:
                print("Result: Patient not found.")

        elif choice == "7":
            print("Exiting application. Bye!")
            break

        else:
            print("Invalid selection. Try again.")

if __name__ == "__main__":
    run_app()