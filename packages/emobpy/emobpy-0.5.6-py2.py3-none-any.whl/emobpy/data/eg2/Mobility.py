from emobpy import Mobility

# Initialize seed
from emobpy.tools import set_seed
set_seed()

hrs = 168 # one week
steps = 0.25 # 15 minutes

for _ in range(2):  # creating five profiles
    try:
        m = Mobility()
        m.set_params("CFT", hrs, steps, "commuter", "01/01/2020")
        m.set_stats(
            "TripsPerDay.csv",
            "DepartureDestinationTrip_Worker.csv",
            "DistanceDurationTrip.csv",
        )
        m.set_rules("fulltime")
        m.run()
        m.save_profile("db")
    except:
        continue

for _ in range(2):  # creating five profiles
    try:
        m = Mobility()
        m.set_params("CPT", hrs, steps, "commuter", "01/01/2020")
        m.set_stats(
            "TripsPerDay.csv",
            "DepartureDestinationTrip_Worker.csv",
            "DistanceDurationTrip.csv",
        )
        m.set_rules("parttime")
        m.run()
        m.save_profile("db")
    except:
        continue

for _ in range(2):  # creating five profiles
    try:
        m = Mobility()
        m.set_params("NFT", hrs, steps, "non-commuter", "01/01/2020")
        m.set_stats(
            "TripsPerDay.csv",
            "DepartureDestinationTrip_Free.csv",
            "DistanceDurationTrip.csv",
        )
        m.set_rules("freetime")
        m.run()
        m.save_profile("db")
    except:
        continue
