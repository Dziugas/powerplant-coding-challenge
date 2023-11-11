def calculate_production_plan(data):
    production_plan = []
    unallocated_load = data["load"]
    unused_powerplants = []

    # let's split wind and sort by max generation as these powerplants have zero price
    # and don't have a Pmin
    wind_powerplants = [
        powerplant
        for powerplant in data["powerplants"]
        if powerplant["type"] == "windturbine"
    ]
    wind_powerplants_sorted = sorted(
        wind_powerplants, key=lambda k: k["pmax"], reverse=True
    )

    # for the rest of the powerplants let's calculate production cost per MWh and sort them by the lowest costs
    non_wind_powerplants_with_cost = [
        calculate_non_wind_powerplant_cost(data, powerplant)
        for powerplant in data["powerplants"]
        if powerplant["type"] != "windturbine"
    ]
    non_wind_powerplants_sorted = sorted(
        non_wind_powerplants_with_cost, key=lambda k: k["cost"]
    )

    # first let's deal with the wind
    if data["fuels"]["wind"] > 0:
        for powerplant in wind_powerplants_sorted:
            if unallocated_load > 0:
                max_production = powerplant["pmax"] * data["fuels"]["wind"] / 100
                if max_production < unallocated_load:
                    unallocated_load -= max_production
                    powerplant["p"] = max_production
                    production_plan.append(powerplant)
                else:
                    powerplant["p"] = unallocated_load
                    production_plan.append(powerplant)
                    unallocated_load = 0
            else:
                add_to_unused_powerplants(unused_powerplants, powerplant)
    else:
        for powerplant in wind_powerplants_sorted:
            add_to_unused_powerplants(unused_powerplants, powerplant)

    # if load not yet satisfied, let's loop the other powerplants
    if unallocated_load > 0:
        for powerplant in non_wind_powerplants_sorted:
            if unallocated_load > 0:
                if powerplant["pmin"] < unallocated_load < powerplant["pmax"]:
                    powerplant["p"] = unallocated_load
                    production_plan.append(powerplant)
                    unallocated_load = 0
                elif unallocated_load > powerplant["pmax"]:
                    unallocated_load -= powerplant["pmax"]
                    powerplant["p"] = powerplant["pmax"]
                    production_plan.append(powerplant)
                elif unallocated_load < powerplant["pmin"]:
                    unallocated_load -= powerplant["pmin"]
                    powerplant["p"] = powerplant["pmin"]
                    production_plan.append(powerplant)
            else:
                add_to_unused_powerplants(unused_powerplants, powerplant)
    else:
        for powerplant in non_wind_powerplants_sorted:
            add_to_unused_powerplants(unused_powerplants, powerplant)

    # let's try to adjust in case we're generating more power than the load requires
    if unallocated_load < 0:
        for powerplant in reversed(production_plan[:-1]):
            if (
                powerplant["pmin"]
                < powerplant["p"] + unallocated_load
                < powerplant["pmax"]
            ):
                powerplant["p"] += unallocated_load
                break

    production_plan = production_plan + unused_powerplants
    final_result = [
        {"name": powerplant["name"], "p": powerplant["p"]}
        for powerplant in production_plan
    ]

    return final_result


def add_to_unused_powerplants(unused_powerplants, powerplant):
    powerplant["p"] = 0.0
    unused_powerplants.append(powerplant)


def calculate_non_wind_powerplant_cost(data, powerplant):
    if powerplant["type"] == "gasfired":
        powerplant["cost"] = data["fuels"]["gas"] / powerplant["efficiency"]
    elif powerplant["type"] == "turbojet":
        powerplant["cost"] = data["fuels"]["kerosine"] / powerplant["efficiency"]
    return powerplant
