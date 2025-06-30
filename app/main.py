from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, SQLModel, select

from . import models
from .database import engine, get_session

SessionDep = Annotated[Session, Depends(get_session)]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    SQLModel.metadata.create_all(engine)
    # write_teams_to_db()
    # write_teams_stats_to_db()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root(session: SessionDep) -> dict:
    return {"message": "FBref stats API is running"}


@app.get("/teams")
def read_teams(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[models.Team]:
    teams = session.exec(select(models.Team).offset(offset).limit(limit)).all()
    return list(teams)


@app.get("/teams/{team_id}/defense")
def read_team_defense(
    team_id: str,
    season: str,
    session: SessionDep,
) -> models.TeamDefense | None:
    statement = select(models.TeamDefense).where(
        models.TeamDefense.team_id == team_id,
        models.TeamDefense.season == season,
    )
    result = session.exec(statement).first()
    return result


@app.get("/teams/{team_id}/gca")
def read_team_gca(
    team_id: str,
    season: str,
    session: SessionDep,
) -> models.TeamGca | None:
    statement = select(models.TeamGca).where(
        models.TeamGca.team_id == team_id,
        models.TeamGca.season == season,
    )
    result = session.exec(statement).first()
    return result


@app.get("/teams/{team_id}/keeper")
def read_team_keeper(
    team_id: str,
    season: str,
    session: SessionDep,
) -> models.TeamKeeper | None:
    statement = select(models.TeamKeeper).where(
        models.TeamKeeper.team_id == team_id,
        models.TeamKeeper.season == season,
    )
    result = session.exec(statement).first()
    return result


@app.get("/teams/{team_id}/keeper-advanced")
def read_team_keeper_advanced(
    team_id: str,
    season: str,
    session: SessionDep,
) -> models.TeamKeeperAdv | None:
    statement = select(models.TeamKeeperAdv).where(
        models.TeamKeeperAdv.team_id == team_id,
        models.TeamKeeperAdv.season == season,
    )
    result = session.exec(statement).first()
    return result


@app.get("/teams/{team_id}/misc")
def read_team_misc(
    team_id: str,
    season: str,
    session: SessionDep,
) -> models.TeamMisc | None:
    statement = select(models.TeamMisc).where(
        models.TeamMisc.team_id == team_id,
        models.TeamMisc.season == season,
    )
    result = session.exec(statement).first()
    return result


@app.get("/teams/{team_id}/passing")
def read_team_passing(
    team_id: str,
    season: str,
    session: SessionDep,
) -> models.TeamPassing | None:
    statement = select(models.TeamPassing).where(
        models.TeamPassing.team_id == team_id,
        models.TeamPassing.season == season,
    )
    result = session.exec(statement).first()
    return result


@app.get("/teams/{team_id}/passing-types")
def read_team_passing_types(
    team_id: str,
    season: str,
    session: SessionDep,
) -> models.TeamPassingTypes | None:
    statement = select(models.TeamPassingTypes).where(
        models.TeamPassingTypes.team_id == team_id,
        models.TeamPassingTypes.season == season,
    )
    result = session.exec(statement).first()
    return result


@app.get("/teams/{team_id}/playing-time")
def read_team_playing_time(
    team_id: str,
    season: str,
    session: SessionDep,
) -> models.TeamPlayingTime | None:
    statement = select(models.TeamPlayingTime).where(
        models.TeamPlayingTime.team_id == team_id,
        models.TeamPlayingTime.season == season,
    )
    result = session.exec(statement).first()
    return result


@app.get("/teams/{team_id}/possession")
def read_team_possession(
    team_id: str,
    season: str,
    session: SessionDep,
) -> models.TeamPossession | None:
    statement = select(models.TeamPossession).where(
        models.TeamPossession.team_id == team_id,
        models.TeamPossession.season == season,
    )
    result = session.exec(statement).first()
    return result


@app.get("/teams/{team_id}/shooting")
def read_team_shooting(
    team_id: str,
    season: str,
    session: SessionDep,
) -> models.TeamShooting | None:
    statement = select(models.TeamShooting).where(
        models.TeamShooting.team_id == team_id,
        models.TeamShooting.season == season,
    )
    result = session.exec(statement).first()
    return result


@app.get("/teams/{team_id}/standard")
def read_team_standard(
    team_id: str,
    season: str,
    session: SessionDep,
) -> models.TeamStandard | None:
    statement = select(models.TeamStandard).where(
        models.TeamStandard.team_id == team_id,
        models.TeamStandard.season == season,
    )
    result = session.exec(statement).first()
    return result
