from datetime import date
from io import StringIO
from time import sleep

import pandas as pd
import requests
from bs4 import BeautifulSoup, Tag
from sqlmodel import Session

from .database import engine
from .models import Team

BASE = "https://fbref.com/en/comps/"
LEAGUES = [
    "9/Premier-League-Stats",
    "11/Serie-A-Stats",
    "12/La-Liga-Stats",
    "13/Ligue-1-Stats",
    "20/Bundesliga-Stats",
    "21/Liga-Profesional-Argentina-Stats",
]


def get_current_season() -> str:
    today = date.today()
    if today.month >= 8:
        return f"{today.year}-{today.year + 1}"
    return f"{today.year - 1}-{today.year}"


def get_soup(url: str) -> BeautifulSoup:
    res = requests.get(url)
    res.raise_for_status()
    return BeautifulSoup(res.text, "html.parser")


def get_team_id_and_name(row: Tag) -> tuple[str, str]:
    href = row.find("a")["href"]
    team_id = href.split("/")[3]
    team_name = href.split("/")[4].replace("-Stats", "").replace("-", " ")
    return team_id, team_name


def write_teams_to_db() -> None:
    country_league_map = {
        "GER": "Bundesliga",
        "FRA": "Ligue 1",
        "ENG": "Premier League",
        "ITA": "Serie A",
        "ESP": "La Liga",
    }

    top_5_leagues_link = "https://fbref.com/en/comps/Big5/Big-5-European-Leagues-Stats"
    soup = get_soup(top_5_leagues_link)
    table = soup.find("table", id="big5_table")

    with Session(engine) as session:
        for row in table.find("tbody").find_all("tr"):
            team_id, team_name = get_team_id_and_name(row)
            country_cell = row.find("td", {"data-stat": "country"})
            country_code = country_cell.text.strip().split()[-1]
            league = country_league_map[country_code]
            if not session.get(Team, team_id):
                team = Team(id=team_id, name=team_name, league=league)
                session.add(team)
        session.commit()
    return


def clean_table(soup: BeautifulSoup, table_id: str) -> pd.DataFrame:
    table = soup.find("table", id=table_id)
    df = pd.read_html(StringIO(str(table)))[0]

    # Use data-stat as column names, more descriptive and no duplicates
    header_row = table.find("thead").find_all("tr")[-1]
    col_names = [th.get("data-stat") for th in header_row.find_all("th")]
    df.columns = col_names

    excluded_cols = ["players_used", "minutes_per_game", "minutes_90s", "team"]
    df = df.drop(excluded_cols, axis=1, errors="ignore")

    # Get team_id and full team name from link
    team_ids = []
    for row in table.find("tbody").find_all("tr"):
        team_id, _ = get_team_id_and_name(row)
        team_ids.append(team_id)
    df["team_id"] = team_ids
    return df


def parse_and_merge_team_category(soup: BeautifulSoup, category: str) -> pd.DataFrame:
    df_for = clean_table(soup, f"stats_squads_{category}_for")
    df_against = clean_table(soup, f"stats_squads_{category}_against")

    df_merged = pd.merge(
        df_for, df_against, on="team_id", how="inner", suffixes=("_for", "_against")
    )
    df_merged["season"] = get_current_season()
    return df_merged


def write_teams_stats_to_db() -> None:
    team_categories = [
        "defense",
        "gca",
        "keeper",
        "misc",
        "passing",
        "passing_types",
        "keeper_adv",
        "playing_time",
        "possession",
        "shooting",
        "standard",
    ]

    for league in LEAGUES:
        print(f"Writing {league}...")
        soup = get_soup(BASE + league)
        for category in team_categories:
            stats_df = parse_and_merge_team_category(soup, category)
            stats_df.to_sql(
                f"team_{category}",
                engine,
                if_exists="append",
                index=False,
            )
        print(f"sleeping {league}...")
        sleep(20)  # To avoid overwhelming the server
