from typing import Optional
from sqlmodel import Field, SQLModel
import datetime


class Chassis(SQLModel, table=True):

    id: Optional[str] = Field(default=None, primary_key=True)
    constructor_id: str
    name: str
    full_name: str


class Circuit(SQLModel, table=True):

    id: Optional[str] = Field(default=None, primary_key=True)
    name: str
    full_name: str
    previous_names: Optional[str]
    type: str
    place_name: str
    country_id: str
    latitude: float
    longitude: float
    total_races_held: int


class Constructor(SQLModel, table=True):

    id: Optional[str] = Field(default=None, primary_key=True)
    name: str
    full_name: str
    country_id: str
    best_championship_position: Optional[int]
    best_starting_grid_position: Optional[int]
    best_race_result: Optional[int]
    total_championship_wins: int
    total_race_entries: int
    total_race_starts: int
    total_race_wins: int
    total_1_and_2_finishes: int
    total_race_laps: int
    total_podiums: int
    total_podium_races: int
    total_points: float
    total_championship_points: float
    total_pole_positions: int
    total_fastest_laps: int


class Constructor_Chronology(SQLModel, table=True):

    constructor_id: Optional[str] = Field(default=None, primary_key=True)
    position_display_order: Optional[int] = Field(default=None, primary_key=True)
    other_constructor_id: str
    year_from: int
    year_to: Optional[int]


class Continent(SQLModel, table=True):

    id: Optional[str] = Field(default=None, primary_key=True)
    code: str
    name: str
    demonym: str


class Country(SQLModel, table=True):

    id: Optional[str] = Field(default=None, primary_key=True)
    alpha2_code: str
    alpha3_code: str
    name: str
    demonym: Optional[str]
    continent_id: str


class Driver(SQLModel, table=True):

    id: Optional[str] = Field(default=None, primary_key=True)
    name: str
    first_name: str
    last_name: str
    full_name: str
    abbreviation: str
    permanent_number: Optional[str]
    gender: str
    date_of_birth: datetime.date
    date_of_death: Optional[datetime.date]
    place_of_birth: str
    country_of_birth_country_id: str
    nationality_country_id: str
    second_nationality_country_id: Optional[str]
    best_championship_position: Optional[int]
    best_starting_grid_position: Optional[int]
    best_race_result: Optional[int]
    total_championship_wins: int
    total_race_entries: int
    total_race_starts: int
    total_race_wins: int
    total_race_laps: int
    total_podiums: int
    total_points: float
    total_championship_points: float
    total_pole_positions: int
    total_fastest_laps: int
    total_driver_of_the_day: int
    total_grand_slams: int


class Driver_Family_Relationship(SQLModel, table=True):

    driver_id: Optional[str] = Field(default=None, primary_key=True)
    position_display_order: Optional[int] = Field(default=None, primary_key=True)
    other_driver_id: str
    type: str


class Engine(SQLModel, table=True):

    id: Optional[str] = Field(default=None, primary_key=True)
    engine_manufacturer_id: str
    name: str
    full_name: str
    capacity: Optional[float]
    configuration: Optional[str]
    aspiration: Optional[str]


class Engine_Manufacturer(SQLModel, table=True):

    id: Optional[str] = Field(default=None, primary_key=True)
    name: str
    country_id: str
    best_championship_position: Optional[int]
    best_starting_grid_position: Optional[int]
    best_race_result: Optional[int]
    total_championship_wins: int
    total_race_entries: int
    total_race_starts: int
    total_race_wins: int
    total_race_laps: int
    total_podiums: int
    total_podium_races: int
    total_points: float
    total_championship_points: float
    total_pole_positions: int
    total_fastest_laps: int


class Entrant(SQLModel, table=True):

    id: Optional[str] = Field(default=None, primary_key=True)
    name: str


class Grand_Prix(SQLModel, table=True):

    id: Optional[str] = Field(default=None, primary_key=True)
    name: str
    full_name: str
    short_name: str
    abbreviation: str
    country_id: Optional[str]
    total_races_held: int


class Race(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    year: int
    round: int
    date: datetime.date
    time: Optional[str]
    grand_prix_id: str
    official_name: str
    qualifying_format: str
    sprint_qualifying_format: Optional[str]
    circuit_id: str
    circuit_type: str
    course_length: float
    laps: int
    distance: float
    scheduled_laps: Optional[int]
    scheduled_distance: Optional[float]
    pre_qualifying_date: Optional[datetime.date]
    pre_qualifying_time: Optional[str]
    free_practice_1_date: Optional[datetime.date]
    free_practice_1_time: Optional[str]
    free_practice_2_date: Optional[datetime.date]
    free_practice_2_time: Optional[str]
    free_practice_3_date: Optional[datetime.date]
    free_practice_3_time: Optional[str]
    free_practice_4_date: Optional[datetime.date]
    free_practice_4_time: Optional[str]
    qualifying_1_date: Optional[datetime.date]
    qualifying_1_time: Optional[str]
    qualifying_2_date: Optional[datetime.date]
    qualifying_2_time: Optional[str]
    qualifying_date: Optional[datetime.date]
    qualifying_time: Optional[str]
    sprint_qualifying_date: Optional[datetime.date]
    sprint_qualifying_time: Optional[str]
    sprint_race_date: Optional[datetime.date]
    sprint_race_time: Optional[str]
    warming_up_date: Optional[datetime.date]
    warming_up_time: Optional[str]


class Race_Constructor_Standing(SQLModel, table=True):

    race_id: Optional[int] = Field(default=None, primary_key=True)
    position_display_order: Optional[int] = Field(default=None, primary_key=True)
    position_number: Optional[int]
    position_text: str
    constructor_id: str
    engine_manufacturer_id: str
    points: float
    positions_gained: Optional[int]


class Race_Data(SQLModel, table=True):

    race_id: Optional[int] = Field(default=None, primary_key=True)
    type: Optional[str] = Field(default=None, primary_key=True)
    position_display_order: Optional[int] = Field(default=None, primary_key=True)
    position_number: Optional[int]
    position_text: str
    driver_number: str
    driver_id: str
    constructor_id: str
    engine_manufacturer_id: str
    tyre_manufacturer_id: str
    practice_time: Optional[str]
    practice_time_millis: Optional[int]
    practice_gap: Optional[str]
    practice_gap_millis: Optional[int]
    practice_interval: Optional[str]
    practice_interval_millis: Optional[int]
    practice_laps: Optional[int]
    qualifying_time: Optional[str]
    qualifying_time_millis: Optional[int]
    qualifying_q1: Optional[str]
    qualifying_q1_millis: Optional[int]
    qualifying_q2: Optional[str]
    qualifying_q2_millis: Optional[int]
    qualifying_q3: Optional[str]
    qualifying_q3_millis: Optional[int]
    qualifying_gap: Optional[str]
    qualifying_gap_millis: Optional[int]
    qualifying_interval: Optional[str]
    qualifying_interval_millis: Optional[int]
    qualifying_laps: Optional[int]
    starting_grid_position_qualification_position_number: Optional[int]
    starting_grid_position_qualification_position_text: Optional[str]
    starting_grid_position_grid_penalty: Optional[str]
    starting_grid_position_grid_penalty_positions: Optional[int]
    starting_grid_position_time: Optional[str]
    starting_grid_position_time_millis: Optional[int]
    race_shared_car: Optional[bool]
    race_laps: Optional[int]
    race_time: Optional[str]
    race_time_millis: Optional[int]
    race_time_penalty: Optional[str]
    race_time_penalty_millis: Optional[int]
    race_gap: Optional[str]
    race_gap_millis: Optional[int]
    race_gap_laps: Optional[int]
    race_interval: Optional[str]
    race_interval_millis: Optional[int]
    race_reason_retired: Optional[str]
    race_points: Optional[float]
    race_qualification_position_number: Optional[int]
    race_qualification_position_text: Optional[str]
    race_grid_position_number: Optional[int]
    race_grid_position_text: Optional[str]
    race_positions_gained: Optional[int]
    race_pit_stops: Optional[int]
    race_fastest_lap: Optional[bool]
    race_driver_of_the_day: Optional[bool]
    race_grand_slam: Optional[bool]
    fastest_lap_lap: Optional[int]
    fastest_lap_time: Optional[str]
    fastest_lap_time_millis: Optional[int]
    fastest_lap_gap: Optional[str]
    fastest_lap_gap_millis: Optional[int]
    fastest_lap_interval: Optional[str]
    fastest_lap_interval_millis: Optional[int]
    pit_stop_stop: Optional[int]
    pit_stop_lap: Optional[int]
    pit_stop_time: Optional[str]
    pit_stop_time_millis: Optional[int]
    driver_of_the_day_percentage: Optional[float]


class Race_Driver_Standing(SQLModel, table=True):

    race_id: Optional[int] = Field(default=None, primary_key=True)
    position_display_order: Optional[int] = Field(default=None, primary_key=True)
    position_number: Optional[int]
    position_text: str
    driver_id: str
    points: float
    positions_gained: Optional[int]


class Season(SQLModel, table=True):

    year: Optional[int] = Field(default=None, primary_key=True)


class Season_Constructor(SQLModel, table=True):

    year: Optional[int] = Field(default=None, primary_key=True)
    constructor_id: Optional[str] = Field(default=None, primary_key=True)
    position_number: Optional[int]
    position_text: Optional[str]
    best_starting_grid_position: Optional[int]
    best_race_result: Optional[int]
    total_race_entries: int
    total_race_starts: int
    total_race_wins: int
    total_1_and_2_finishes: int
    total_race_laps: int
    total_podiums: int
    total_podium_races: int
    total_points: float
    total_pole_positions: int
    total_fastest_laps: int


class Season_Constructor_Standing(SQLModel, table=True):

    year: Optional[int] = Field(default=None, primary_key=True)
    position_display_order: Optional[int] = Field(default=None, primary_key=True)
    position_number: Optional[int]
    position_text: str
    constructor_id: str
    engine_manufacturer_id: str
    points: float


class Season_Driver(SQLModel, table=True):

    year: Optional[int] = Field(default=None, primary_key=True)
    driver_id: Optional[str] = Field(default=None, primary_key=True)
    position_number: Optional[int]
    position_text: Optional[str]
    best_starting_grid_position: Optional[int]
    best_race_result: Optional[int]
    total_race_entries: int
    total_race_starts: int
    total_race_wins: int
    total_race_laps: int
    total_podiums: int
    total_points: float
    total_pole_positions: int
    total_fastest_laps: int
    total_driver_of_the_day: int
    total_grand_slams: int


class Season_Driver_Standing(SQLModel, table=True):

    year: Optional[int] = Field(default=None, primary_key=True)
    position_display_order: Optional[int] = Field(default=None, primary_key=True)
    position_number: Optional[int]
    position_text: str
    driver_id: str
    points: float


class Season_Engine_Manufacturer(SQLModel, table=True):

    year: Optional[int] = Field(default=None, primary_key=True)
    engine_manufacturer_id: Optional[str] = Field(default=None, primary_key=True)
    position_number: Optional[int]
    position_text: Optional[str]
    best_starting_grid_position: Optional[int]
    best_race_result: Optional[int]
    total_race_entries: int
    total_race_starts: int
    total_race_wins: int
    total_race_laps: int
    total_podiums: int
    total_podium_races: int
    total_points: float
    total_pole_positions: int
    total_fastest_laps: int


class Season_Entrant(SQLModel, table=True):

    year: Optional[int] = Field(default=None, primary_key=True)
    entrant_id: Optional[str] = Field(default=None, primary_key=True)
    country_id: str


class Season_Entrant_Chassis(SQLModel, table=True):

    year: Optional[int] = Field(default=None, primary_key=True)
    entrant_id: Optional[str] = Field(default=None, primary_key=True)
    constructor_id: Optional[str] = Field(default=None, primary_key=True)
    engine_manufacturer_id: Optional[str] = Field(default=None, primary_key=True)
    chassis_id: Optional[str] = Field(default=None, primary_key=True)


class Season_Entrant_Constructor(SQLModel, table=True):

    year: Optional[int] = Field(default=None, primary_key=True)
    entrant_id: Optional[str] = Field(default=None, primary_key=True)
    constructor_id: Optional[str] = Field(default=None, primary_key=True)
    engine_manufacturer_id: Optional[str] = Field(default=None, primary_key=True)


class Season_Entrant_Driver(SQLModel, table=True):

    year: Optional[int] = Field(default=None, primary_key=True)
    entrant_id: Optional[str] = Field(default=None, primary_key=True)
    constructor_id: Optional[str] = Field(default=None, primary_key=True)
    engine_manufacturer_id: Optional[str] = Field(default=None, primary_key=True)
    driver_id: Optional[str] = Field(default=None, primary_key=True)
    rounds: Optional[str]
    rounds_text: Optional[str]
    test_driver: bool


class Season_Entrant_Engine(SQLModel, table=True):

    year: Optional[int] = Field(default=None, primary_key=True)
    entrant_id: Optional[str] = Field(default=None, primary_key=True)
    constructor_id: Optional[str] = Field(default=None, primary_key=True)
    engine_manufacturer_id: Optional[str] = Field(default=None, primary_key=True)
    engine_id: Optional[str] = Field(default=None, primary_key=True)


class Season_Entrant_Tyre_Manufacturer(SQLModel, table=True):

    year: Optional[int] = Field(default=None, primary_key=True)
    entrant_id: Optional[str] = Field(default=None, primary_key=True)
    constructor_id: Optional[str] = Field(default=None, primary_key=True)
    engine_manufacturer_id: Optional[str] = Field(default=None, primary_key=True)
    tyre_manufacturer_id: Optional[str] = Field(default=None, primary_key=True)


class Season_Tyre_Manufacturer(SQLModel, table=True):

    year: Optional[int] = Field(default=None, primary_key=True)
    tyre_manufacturer_id: Optional[str] = Field(default=None, primary_key=True)
    best_starting_grid_position: Optional[int]
    best_race_result: Optional[int]
    total_race_entries: int
    total_race_starts: int
    total_race_wins: int
    total_race_laps: int
    total_podiums: int
    total_podium_races: int
    total_pole_positions: int
    total_fastest_laps: int


class Tyre_Manufacturer(SQLModel, table=True):

    id: Optional[str] = Field(default=None, primary_key=True)
    name: str
    country_id: str
    best_starting_grid_position: Optional[int]
    best_race_result: Optional[int]
    total_race_entries: int
    total_race_starts: int
    total_race_wins: int
    total_race_laps: int
    total_podiums: int
    total_podium_races: int
    total_pole_positions: int
    total_fastest_laps: int
