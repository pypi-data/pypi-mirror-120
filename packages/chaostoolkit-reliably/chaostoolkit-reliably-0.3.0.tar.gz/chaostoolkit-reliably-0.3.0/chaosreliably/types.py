from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from uuid import uuid4

from pydantic import BaseModel as PydanticBaseModel
from pydantic import Field, parse_obj_as
from pydantic.networks import HttpUrl
from pydantic.types import UUID4

OPTIONAL_DICT_LIST = Optional[List[Dict[str, Any]]]
RELATED_TO = Field(alias="relatedTo", default=[])


class BaseModel(PydanticBaseModel):
    class Config:
        allow_population_by_field_name = True


class ObjectiveResultMetadata(BaseModel):
    labels: Dict[str, str]
    related_to: OPTIONAL_DICT_LIST = RELATED_TO


class ObjectiveResultSpec(BaseModel):
    indicator_selector: Dict[str, str] = Field(alias="indicatorSelector")
    objective_percent: float = Field(alias="objectivePercent")
    actual_percent: float = Field(alias="actualPercent")
    remaining_percent: float = Field(alias="remainingPercent")


class ObjectiveResult(BaseModel):
    metadata: ObjectiveResultMetadata
    spec: ObjectiveResultSpec

    def parse_list(obj: Any) -> "List[ObjectiveResult]":
        return parse_obj_as(List[ObjectiveResult], obj)


class ChaosToolkitType(Enum):
    EXPERIMENT: str = "Chaos Toolkit Experiment"
    EXPERIMENT_EVENT: str = "Chaos Toolkit Experiment Event"
    EXPERIMENT_RUN: str = "Chaos Toolkit Experiment Run"
    EXPERIMENT_VERSION: str = "Chaos Toolkit Experiment Version"


class EntityContextExperimentLabels(BaseModel):
    type: str = Field(
        default=ChaosToolkitType.EXPERIMENT.value, alias="ctk_type", const=True
    )
    title: str = Field(alias="ctk_experiment_title")


class EntityContextExperimentVersionLabels(BaseModel):
    type: str = Field(
        default=ChaosToolkitType.EXPERIMENT_VERSION.value, alias="ctk_type", const=True
    )
    commit_hash: str = Field(alias="ctk_commit_hash")
    source: HttpUrl = Field(alias="ctk_source")


class EntityContextExperimentRunLabels(BaseModel):
    type: str = Field(
        default=ChaosToolkitType.EXPERIMENT_RUN.value, alias="ctk_type", const=True
    )
    id: UUID4 = Field(default_factory=lambda: uuid4(), alias="ctk_run_id", const=True)
    timestamp: datetime = Field(
        alias="ctk_run_timestamp",
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        const=True,
    )
    user: str = Field(alias="ctk_run_user")


class EventType(Enum):
    ACTIVITY_END = "ACTIVITY_END"
    ACTIVITY_START = "ACTIVITY_START"
    EXPERIMENT_END = "EXPERIMENT_END"
    EXPERIMENT_START = "EXPERIMENT_START"
    HYPOTHESIS_END = "HYPOTHESIS_END"
    HYPOTHESIS_START = "HYPOTHESIS_START"
    METHOD_END = "METHOD_END"
    METHOD_START = "METHOD_START"
    ROLLBACK_END = "ROLLBACK_END"
    ROLLBACK_START = "ROLLBACK_START"


class EntityContextExperimentEventLabels(BaseModel):
    type: str = Field(
        default=ChaosToolkitType.EXPERIMENT_EVENT.value, alias="ctk_type", const=True
    )
    event_type: str = Field(alias="ctk_event_type")
    timestamp: datetime = Field(
        alias="ctk_event_timestamp",
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        const=True,
    )
    name: str = Field(alias="ctk_event_name")
    output: Any = Field(alias="ctk_event_output")


class EntityContextMetadata(BaseModel):
    labels: Union[
        EntityContextExperimentLabels,
        EntityContextExperimentVersionLabels,
        EntityContextExperimentRunLabels,
        EntityContextExperimentEventLabels,
    ]
    related_to: OPTIONAL_DICT_LIST = RELATED_TO


class EntityContext(BaseModel):
    metadata: EntityContextMetadata
