from sw_entities import EvacuationPlan, Garrison, MilitaryBase, \
    Person, Planet, Species, Starship
import sw_utilities as utl


ENDPOINT = 'https://swapi.py4e.com/api'

def create_person(data):
    """Creates a Person instance from dictionary data (a map),
    converting string values to the appropriate type whenever
    possible.

    Parameters:
        data (dict): source data

    Returns:
        person: new Person instance
    """

    person = Person(data['url'], data['name'])
    person.birth_year = data['birth_year']
    person.height = utl.convert_str_to_float(data['height'])
    person.mass = utl.convert_str_to_float(data['mass'])
    person.homeworld = create_planet(utl.get_swapi_resource(data['homeworld']))
    person.species = create_species(utl.get_swapi_resource(data['species'][0]))

    return person

def create_planet(data):
    """Creates a Planet instance from dictionary data (a map),
    converting string values to the appropriate type whenever
    possible.

    Parameters:
        data (dict): source data

    Returns:
        planet: new Planet instance
    """

    planet = Planet(data['url'], data['name'])
    planet.gravity = data['gravity']
    planet.climate = utl.convert_str_to_list(data['climate'], ', ')
    planet.terrain = utl.convert_str_to_list(data['terrain'], ', ')
    planet.surface_water = utl.convert_str_to_int(data['surface_water'])
    planet.population = utl.convert_str_to_int(data['population'])

    return planet

def create_species(data):
    """Creates a Species instance from dictionary data (a map),
    converting string values to the appropriate type whenever
    possible.

    Parameters:
        data (dict): source data

    Returns:
        species: new Species instance
    """

    species = Species(data['url'], data['name'])
    species.classification = data['classification']
    species.designation = data['designation']
    species.language = data['language']

    return species


def create_starship(data):
    """Creates a Starship instance from dictionary data (a map),
    converting string values to the appropriate type whenever
    possible. Assigning crews and passengers are considered separate
    operations.

    Parameters:
        data (dict): source data

    Returns:
        starship: a new Starship instance
    """

    starship = Starship(data['url'], data['name'], data['model'], data['starship_class'])
    starship.length = utl.convert_str_to_float(data['length'])
    starship.max_atmosphering_speed = utl.convert_str_to_float(data['max_atmosphering_speed'])
    starship.hyperdrive_rating = utl.convert_str_to_float(data['hyperdrive_rating'])
    starship.MGLT = utl.convert_str_to_int(data['MGLT'])
    starship.armament = utl.convert_str_to_list(data['armament'], ', ')
    starship.crew = utl.convert_str_to_int(data['crew'])
    starship.passengers = utl.convert_str_to_int(data['passengers'])
    starship.consumables = data['consumables']
    starship.cargo_capacity = utl.convert_str_to_int(data['cargo_capacity'])

    return starship


def main():
    """Entry point. This program will import two custom modules (sw_entities.py,
    sw_utilities.py) that provide class definitions and utility functions designed
    to interact with local file assets and the Star Wars API (SWAPI). Additional
    utility functions designed to simply the creation of object instances are
    located above.

    main() will manage the workflow required to create two Top Secret data files
    requested by Rebel Alliance Intelligence.

    - A JSON file comprising a list of uninhabited planets where a new rebel base
      could be situated if Imperial forces discover the location of Echo Base.

    - A JSON file describing the Echo Base including an evacuation plan of base
      personnel. The plan will assign Princess Leia and the protocol droid C-3PO
      to the transport Bright Hope. Upon departure the transport will be
      escorted by an X-wing starfighter piloted by Commander Luke Skywalker
      (with astromech droid R2-D2) and the light freighter Millennium Falcon
      crewed by the smugglers Han Solo and Chewbacca, the Wookiee.

    Parameters:
        None

    Returns:
        None
    """

    # Refer to SWAPI Echo Base Assignment Guide for instructions and tips.

    # Endpoints
    swapi_people_url = f"{ENDPOINT}/people/"
    swapi_planets_url = f"{ENDPOINT}/planets"
    swapi_starships_url = f"{ENDPOINT}/starships/"

    # 8.2 WARMUP: Locate uninhabited planets

    swapi_planets = utl.read_json('sw_planets-v1p0.json')
    uninhabited = []
    for planet_dictionary in swapi_planets:
        population = planet_dictionary['population']

        if utl.is_unknown(population):
            planet_instance = create_planet(planet_dictionary) # create an instance of that planet
            uninhabited.append(planet_instance)
    utl.write_custom_json('sw_uninhabited_planets.json', uninhabited)


    # 8.3 TEST CODE: Create an Echo Base person
    leia_organa = create_person(utl.get_swapi_resource(swapi_people_url)['results'][4])
    utl.write_custom_json('test_leia.json', leia_organa)

    # 8.4 TEST CODE: Create an Echo Base starship
    swapi_x_wing = utl.get_swapi_resource(swapi_starships_url)['results'][6]
    csv_x_wing = utl.read_csv_as_dict('sw_echo_base_transport_craft.csv', ',')[0]
    x_wing_combined = utl.combine_data(swapi_x_wing, csv_x_wing)
    x_wing_instance = create_starship(x_wing_combined)
    utl.write_custom_json('test_x_wing.json', x_wing_instance)

    # 8.5 Echo Base evacuation plan

    echo_base_data = utl.read_json('sw_echo_base-v1p0.json') # read file

    # 8.5.1 echo_base MiltaryBase

    echo_base = MilitaryBase(echo_base_data['url'], echo_base_data['name']) # instantiate MiltaryBase instance

    planet_instance = create_planet(utl.get_swapi_resource(swapi_planets_url)['results'][3])
    planet_instance.url = echo_base_data['planet']['url']
    echo_base.location = planet_instance

    garrison_instance = Garrison(echo_base_data['garrison']['url'], echo_base_data['garrison']['name'])
    person_instance = create_person(echo_base_data['garrison']['commander'])
    garrison_instance.commander = person_instance
    garrison_instance.personnel = echo_base_data['garrison']['personnel']
    echo_base.garrison = garrison_instance

    echo_base_data['air_space_assets'][0]['model'] = 'T-65 X-wing'
    echo_base_data['air_space_assets'][1]['model'] = 'BTL Y-wing'
    echo_base_data['air_space_assets'][2]['model'] = 't-47 airspeeder'
    echo_base_data['air_space_assets'][3]['model'] = 'GR-75 medium transport'
    echo_base_data['air_space_assets'][4]['model'] = 'YT-1300fp light freighter'
    
    echo_base.operational_status = echo_base_data['operational_status']
    echo_base.facilities = echo_base_data['facilities']
    echo_base.fixed_defenses = echo_base_data['fixed_defenses']
    echo_base.air_space_assets = echo_base_data['air_space_assets']


    # 8.5.2 evac_plan EvacuationPlan
    evac_plan_instance = EvacuationPlan(echo_base_data['evacuation_plan']['url'], echo_base_data['evacuation_plan']['name'])
    evac_plan_instance.classification = echo_base_data['evacuation_plan']['classification']
    evac_plan_instance.year_era = echo_base_data['evacuation_plan']['year_era']
    evac_plan_instance.description = echo_base_data['evacuation_plan']['description']
    evac_plan_instance.passenger_overload_multiplier = utl.convert_str_to_int(echo_base_data['evacuation_plan']['passenger_overload_multiplier'])
    evac_plan_instance.transport_assignments = echo_base_data['evacuation_plan']['transport_passenger_assignments']
    evac_plan_instance.transport_escorts = echo_base_data['evacuation_plan']['transport_escorts']

    # 8.5.3 gr_75_transport Starship
    swapi_gr_75 = utl.get_swapi_resource(swapi_starships_url)['results'][-1]
    csv_gr_75 = utl.read_csv_as_dict('sw_echo_base_transport_craft.csv', ',')[-2]
    gr_75_combined = utl.combine_data(swapi_gr_75, csv_gr_75)
    gr_75_combined['name'] = 'Bright Hope'
    gr_75_instance = create_starship(gr_75_combined)

    crew_data = utl.read_json('sw_bright_hope_crew.json')
    pilot_instance = create_person(crew_data['pilot'])
    co_pilot_instance = create_person(crew_data['co-pilot'])
    navigator_instance = create_person(crew_data['navigator'])
    
    crew1 = {
        'pilot': pilot_instance,
        'co-pilot': co_pilot_instance,
        'navigator': navigator_instance
    }
    gr_75_instance.assign_crew(crew1)

    C_3PO_person = create_person(utl.get_swapi_resource(swapi_people_url)['results'][1])

    manifest = [leia_organa, C_3PO_person]
    gr_75_instance.assign_passengers(manifest)
    
    evac_plan_instance.transport_assignments.append(gr_75_instance)

    # 8.5.4 x_wing Starship
    swapi_x_wing = utl.get_swapi_resource(swapi_starships_url)['results'][6]
    csv_x_wing = utl.read_csv_as_dict('sw_echo_base_transport_craft.csv', ',')[0]
    x_wing_combined = utl.combine_data(swapi_x_wing, csv_x_wing)
    x_wing_instance = create_starship(x_wing_combined)
    
    luke_person = create_person(utl.get_swapi_resource(swapi_people_url)['results'][0])
    R2_D2_person = create_person(utl.get_swapi_resource(swapi_people_url)['results'][2])
    crew2 = {
        'pilot': luke_person,
        'astromech_droid': R2_D2_person
    }
    x_wing_instance.assign_crew(crew2)

    evac_plan_instance.transport_escorts.append(x_wing_instance)

    # 8.5.5 m_falcon Starship
    swapi_mill_falcon = utl.get_swapi_resource(swapi_starships_url)['results'][4]
    csv_mill_falcon = utl.read_csv_as_dict('sw_echo_base_transport_craft.csv', ',')[-1]
    mill_falcon_combined = utl.combine_data(swapi_mill_falcon, csv_mill_falcon)
    mill_falcon_instance = create_starship(mill_falcon_combined)
    
    han_person = create_person(utl.get_swapi_resource("https://swapi.py4e.com/api/people/14/"))
    chewbacca_person = create_person(utl.get_swapi_resource("https://swapi.py4e.com/api/people/13/"))
    crew3 = {
        'pilot': han_person,
        'co-pilot': chewbacca_person
    }
    mill_falcon_instance.assign_crew(crew3)

    evac_plan_instance.transport_escorts.append(mill_falcon_instance)


    # 8.5.6 Evacuation arithmetic
    garrison_personnel_count = 0
    for value in echo_base_data['garrison']['personnel'].values():
        garrison_personnel_count += value
    evac_plan_instance.garrison_personnel_count = utl.convert_str_to_int(garrison_personnel_count)

    evac_plan_instance.num_available_transports = int(30)

    evac_plan_instance.max_passenger_overload_capacity = evac_plan_instance.num_available_transports * gr_75_instance.passengers * evac_plan_instance.passenger_overload_multiplier

    echo_base.evacuation_plan = evac_plan_instance

    # 8.5.7 Complete the evacuation plan and write to file


    # WRITE TO FILE
    filepath = 'sw_echo_base-v1p1.json'
    utl.write_custom_json(filepath, echo_base)


if __name__ == '__main__':
    main()