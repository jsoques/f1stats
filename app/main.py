from typing import Optional
from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import htmlgenerator as hg
from htmlgenerator import mark_safe
from sqlalchemy.sql.functions import count
from sqlmodel import Session, select
import pygal

from app.database import close_db, create_db_and_tables, get_db
from app.models.f1 import (
    Constructor,
    Country,
    Driver,
    Engine,
    Engine_Manufacturer,
    Race,
    Race_Data,
    Season,
    Season_Constructor,
    Season_Constructor_Standing,
    Season_Driver_Standing,
    Season_Entrant_Driver,
    Season_Entrant_Engine,
)


HTML_404_PAGE = "<h1>404</h1>"


async def not_found(request, exc):
    return HTMLResponse(content=HTML_404_PAGE, status_code=exc.status_code)


exceptions = {
    404: not_found,
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up")
    create_db_and_tables()
    yield
    print("Shutting down")
    close_db()


app = FastAPI(
    docs_url=None, redoc_url=None, exception_handlers=exceptions, lifespan=lifespan
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/api/season", response_class=HTMLResponse)
def read_season(year: Optional[int | None] = None, db: Session = Depends(get_db)):

    if year == 0:
        return ""

    number_of_races = db.exec(
        select(Race).where(Race.year == year).order_by(Race.date)
    ).all()

    constructors = db.exec(
        select(Season_Constructor, Constructor.full_name)
        .join(Constructor, Season_Constructor.constructor_id == Constructor.id)
        .where(Season_Constructor.year == year)
        .order_by(Season_Constructor.position_number)
    ).all()

    constructors_standing = db.exec(
        select(Season_Constructor_Standing)
        .where(Season_Constructor_Standing.year == year)
        .order_by(Season_Constructor_Standing.position_number)
    ).all()

    season_driver_standing = db.exec(
        select(Season_Driver_Standing, Season_Entrant_Driver)
        .join(
            Season_Entrant_Driver,
            Season_Driver_Standing.driver_id == Season_Entrant_Driver.driver_id,
        )
        .where(Season_Driver_Standing.year == year)
        .where(Season_Entrant_Driver.year == year)
        .order_by(Season_Driver_Standing.position_number)
    ).all()

    # Constructors
    constructors_bar_chart = pygal.Bar(
        x_label_rotation=40, width=900, height=600, explicit_size=True
    )
    constructors_bar_chart.title = "Constructors"
    constructors_bar_chart.x_title = "Position"
    constructors_bar_chart.x_labels = [
        str(constructor.Season_Constructor.constructor_id)
        for constructor in constructors
    ]
    constructors_bar_chart.y_title = "Points"
    constructors_bar_chart.add(
        "Points", [constructor.points for constructor in constructors_standing]
    )

    # Constructors podiums
    constructors_podiums_bar_chart = pygal.Bar(
        x_label_rotation=40, width=900, height=600, explicit_size=True
    )
    constructors_podiums_bar_chart.title = "Constructors"
    constructors_podiums_bar_chart.x_title = "Position"
    constructors_podiums_bar_chart.x_labels = [
        str(constructor.Season_Constructor.constructor_id)
        for constructor in constructors
    ]

    # other stats
    # driver_nationality
    driver_nationality = db.exec(
        select(Country.name, count(Driver.nationality_country_id))
        .join(
            Country,
            Driver.nationality_country_id == Country.id,
        )
        .group_by(Country.name)
        .order_by(count(Driver.nationality_country_id).desc())
    ).all()

    print()

    # engine manufacturer wins
    engine_manufacturer_wins = db.exec(
        select(
            count(Race_Data.race_id).label("wins"),
            Season_Entrant_Engine.engine_manufacturer_id.label("manufacturer"),
            # Engine.full_name.label("engine_name"),
            Engine_Manufacturer.name.label("engine_manufacturer"),
            Engine_Manufacturer.country_id,
        )
        .join(
            Constructor,
            Race_Data.constructor_id == Constructor.id,
        )
        .join(
            Season_Entrant_Engine,
            Season_Entrant_Engine.constructor_id == Constructor.id,
        )
        .join(
            Engine,
            Season_Entrant_Engine.engine_id == Engine.id,
        )
        .join(
            Engine_Manufacturer,
            Season_Entrant_Engine.engine_manufacturer_id == Engine_Manufacturer.id,
        )
        .where(Race_Data.position_number == 1)
        .group_by(Season_Entrant_Engine.engine_manufacturer_id)
        .order_by(count(Race_Data.race_id).desc())
    ).all()

    # bar_chart2.y_title = "Total Podiums"
    constructors_podiums_bar_chart.add(
        "Total Podiums",
        [constructor.Season_Constructor.total_podiums for constructor in constructors],
    )
    # bar_chart2.y_title = "Total Race Wins"
    constructors_podiums_bar_chart.add(
        "Total Race Wins",
        [
            constructor.Season_Constructor.total_race_wins
            for constructor in constructors
        ],
    )

    # Drivers
    drivers_bar_chart = pygal.Bar(
        x_label_rotation=40, width=900, height=600, explicit_size=True
    )
    drivers_bar_chart.title = "Drivers"
    drivers_bar_chart.x_title = "Position"
    drivers_bar_chart.x_labels = [
        str(driver.Season_Driver_Standing.driver_id)
        for driver in season_driver_standing
    ]
    drivers_bar_chart.y_title = "Points"
    drivers_bar_chart.add(
        "Points",
        [driver.Season_Driver_Standing.points for driver in season_driver_standing],
    )

    # Drivers nationality
    drivers_nationality_bar_chart = pygal.Bar(
        x_label_rotation=40, width=1300, height=800, explicit_size=True
    )
    drivers_nationality_bar_chart.title = "Drivers"
    drivers_nationality_bar_chart.x_title = "Country"
    drivers_nationality_bar_chart.x_labels = [
        driver[0] for driver in driver_nationality
    ]
    drivers_nationality_bar_chart.y_title = "Number of drivers"
    drivers_nationality_bar_chart.add(
        "Number of drivers", [driver[1] for driver in driver_nationality]
    )

    engine_manufacturer_wins_bar_chart = pygal.Bar(
        x_label_rotation=40, width=1300, height=800, explicit_size=True
    )
    engine_manufacturer_wins_bar_chart.title = "Engine Manufacturers"
    engine_manufacturer_wins_bar_chart.x_title = "Manufacturer"
    engine_manufacturer_wins_bar_chart.x_labels = [
        engine_manufacturer[1] for engine_manufacturer in engine_manufacturer_wins
    ]
    engine_manufacturer_wins_bar_chart.y_title = "Number of wins"
    engine_manufacturer_wins_bar_chart.add(
        "Number of wins",
        [engine_manufacturer[0] for engine_manufacturer in engine_manufacturer_wins],
    )

    constructors_svg_chart = constructors_bar_chart.render().decode("utf-8")
    constructors_podiums_svg_chart = constructors_podiums_bar_chart.render().decode(
        "utf-8"
    )
    drivers_svg_chart = drivers_bar_chart.render().decode("utf-8")
    drivers_nationality_svg_chart = drivers_nationality_bar_chart.render().decode(
        "utf-8"
    )
    engine_manufacturer_wins_svg_chart = (
        engine_manufacturer_wins_bar_chart.render().decode("utf-8")
    )

    # races

    my_page = hg.DIV(
        hg.H1(f"Formula 1 Standings {str(year)}"),
        hg.H2(f"Number of races: {str(len(number_of_races))}"),
        hg.TABLE(
            hg.THEAD(
                hg.TR(
                    hg.TH("Date"),
                    hg.TH("Grand Prix"),
                    hg.TH("Round"),
                )
            ),
            hg.TBODY(
                *[
                    hg.TR(
                        hg.TD(str(race.date)),
                        hg.TD(race.official_name),
                        hg.TD(str(race.round)),
                    )
                    for race in number_of_races
                ]
            ),
            _class="pure-table pure-table-bordered",
        ),
        hg.HR(),
        hg.DIV(
            hg.H2(f"Constructors {str(year)}"),
        ),
        hg.TABLE(
            hg.THEAD(
                hg.TR(
                    hg.TH("Pos"),
                    hg.TH("Constructor"),
                    hg.TH("Best Starting Grid Position"),
                    hg.TH("Best Race Result"),
                    hg.TH("Total Race Entries"),
                    hg.TH("Total Race Starts"),
                    hg.TH("Total Race Wins"),
                    hg.TH("Total 1 and 2 Finishes"),
                    hg.TH("Total Race Laps"),
                    hg.TH("Total Podiums"),
                    hg.TH("Total Podium Races"),
                    hg.TH("Total Points"),
                    hg.TH("Total Pole Positions"),
                    hg.TH("Total Fastest Laps"),
                )
            ),
            hg.TBODY(
                *[
                    hg.TR(
                        hg.TD(str(constructor.Season_Constructor.position_number)),
                        hg.TD(constructor.full_name),
                        hg.TD(
                            str(
                                constructor.Season_Constructor.best_starting_grid_position
                            )
                        ),
                        hg.TD(str(constructor.Season_Constructor.best_race_result)),
                        hg.TD(str(constructor.Season_Constructor.total_race_entries)),
                        hg.TD(str(constructor.Season_Constructor.total_race_starts)),
                        hg.TD(str(constructor.Season_Constructor.total_race_wins)),
                        hg.TD(
                            str(constructor.Season_Constructor.total_1_and_2_finishes)
                        ),
                        hg.TD(str(constructor.Season_Constructor.total_race_laps)),
                        hg.TD(str(constructor.Season_Constructor.total_podiums)),
                        hg.TD(str(constructor.Season_Constructor.total_podium_races)),
                        hg.TD(str(constructor.Season_Constructor.total_points)),
                        hg.TD(str(constructor.Season_Constructor.total_pole_positions)),
                        hg.TD(str(constructor.Season_Constructor.total_fastest_laps)),
                    )
                    for constructor in constructors
                ],
            ),
            _class="pure-table pure-table-bordered",
        ),
        hg.DIV(
            mark_safe(constructors_svg_chart), mark_safe(constructors_podiums_svg_chart)
        ),
        hg.HR(),
        hg.DIV(hg.H2(f"Constructors Standing {str(year)}")),
        hg.TABLE(
            hg.THEAD(
                hg.TR(
                    hg.TH("Pos"),
                    hg.TH("Constructor"),
                    hg.TH("Engine Manufacturer"),
                    hg.TH("Points"),
                )
            ),
            hg.TBODY(
                *[
                    hg.TR(
                        hg.TD(str(constructor_standing.position_number)),
                        hg.TD(constructor_standing.constructor_id),
                        hg.TD(str(constructor_standing.engine_manufacturer_id)),
                        hg.TD(str(constructor_standing.points)),
                    )
                    for constructor_standing in constructors_standing
                ],
            ),
            _class="pure-table pure-table-bordered",
        ),
        hg.HR(),
        hg.DIV(hg.H2(f"Drivers Standing {str(year)}")),
        hg.TABLE(
            hg.TR(
                hg.TD(
                    hg.TABLE(
                        hg.THEAD(
                            hg.TR(
                                hg.TH("Pos"),
                                hg.TH("Driver"),
                                hg.TH("Points"),
                                hg.TH("Team"),
                                hg.TH("Engine Manufacturer"),
                            )
                        ),
                        hg.TBODY(
                            *[
                                hg.TR(
                                    hg.TD(
                                        str(
                                            driver_standing.Season_Driver_Standing.position_number
                                        )
                                    ),
                                    hg.TD(
                                        driver_standing.Season_Driver_Standing.driver_id
                                    ),
                                    hg.TD(
                                        str(
                                            driver_standing.Season_Driver_Standing.points
                                        )
                                    ),
                                    hg.TD(
                                        driver_standing.Season_Entrant_Driver.constructor_id
                                    ),
                                    hg.TD(
                                        str(
                                            driver_standing.Season_Entrant_Driver.engine_manufacturer_id
                                        )
                                    ),
                                )
                                for driver_standing in season_driver_standing
                            ],
                        ),
                        _class="pure-table pure-table-bordered",
                    ),
                ),
                hg.TD(
                    hg.DIV(mark_safe(drivers_svg_chart)),
                ),
            )
        ),
        hg.HR(),
        hg.H2("Other Statistics (All years)"),
        hg.HR(),
        hg.DIV(hg.H2("Drivers Nationality")),
        hg.TABLE(
            hg.TR(
                hg.TD(
                    hg.TABLE(
                        hg.THEAD(
                            hg.TR(
                                hg.TH("Country"),
                                hg.TH("Number of drivers"),
                            )
                        ),
                        hg.TBODY(
                            *[
                                hg.TR(
                                    hg.TD(str(driver[0])),
                                    hg.TD(str(driver[1])),
                                )
                                for driver in driver_nationality
                            ],
                        ),
                        _class="pure-table pure-table-bordered",
                    ),
                ),
                hg.TD(hg.DIV(mark_safe(drivers_nationality_svg_chart))),
            ),
        ),
        hg.HR(),
        hg.H2("Engine Manufacturers Wins"),
        hg.TABLE(
            hg.TR(
                hg.TD(
                    hg.TABLE(
                        hg.TR(
                            hg.TD(
                                hg.TABLE(
                                    hg.THEAD(
                                        hg.TR(
                                            hg.TH("Number of wins"),
                                            hg.TH("Engine Manufacturer"),
                                            hg.TH("Country"),
                                        )
                                    ),
                                    hg.TBODY(
                                        *[
                                            hg.TR(
                                                hg.TD(str(engine_wins[0])),
                                                hg.TD(str(engine_wins[2])),
                                                hg.TD(str(engine_wins[3])),
                                            )
                                            for engine_wins in engine_manufacturer_wins
                                        ],
                                    ),
                                    _class="pure-table pure-table-bordered",
                                ),
                            ),
                        ),
                    ),
                ),
                hg.TD(hg.DIV(mark_safe(engine_manufacturer_wins_svg_chart))),
            ),
        ),
    )
    return hg.render(my_page, {})


@app.get("/", response_class=HTMLResponse)
def read_root(db: Session = Depends(get_db)):

    seasons = db.exec(select(Season)).all()

    seasons.sort(key=lambda x: x.year, reverse=True)

    seasons_selection = hg.SELECT(
        hg.OPTION(value="0", label=""),
        *[
            hg.OPTION(value=str(season.year), label=str(season.year))
            for season in seasons
        ],
        name="year",
        style="width: 100px",
        hx_get="/api/season",
        hx_trigger="change",
        hx_target="#content",
        hx_indicator="#spinner",
    )

    my_page = hg.HTML(
        hg.HEAD(
            hg.SCRIPT(src="https://unpkg.com/htmx.org@2.0.4"),
            hg.LINK(
                rel="stylesheet",
                href="https://cdn.jsdelivr.net/npm/purecss@3.0.0/build/pure-min.css",
                integrity="sha384-X38yfunGUhNzHpBaEBsWLO+A0HDYOQi8ufWDkZ0k9e0eXz/tH3II7uKZ9msv++Ls",
                crossorigin="anonymous",
            ),
            hg.STYLE(
                ".my-indicator{display:none;} .htmx-request .my-indicator{display:inline;} .htmx-request.my-indicator{display:inline;}",
            ),
        ),
        hg.BODY(
            hg.H1("F1 Stats"),
            hg.H3("Select season"),
            hg.DIV(
                seasons_selection,
                id="seasons",
            ),
            hg.HR(),
            hg.IMAGE(
                id="spinner",
                _class="my-indicator",
                src="static/img/clock.svg",
            ),
            hg.DIV(id="content"),
            style="padding: 20px",
        ),
        doctype=True,
    )

    return hg.render(my_page, {})
