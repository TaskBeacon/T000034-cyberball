from __future__ import annotations

import random
from typing import Any

from psychopy import logging
from psyflow import StimUnit


PLAYER_PARTICIPANT = 0
PLAYER_LEFT = 1
PLAYER_RIGHT = 2


class Controller:
    """Task-level state and toss policy for the Cyberball paradigm."""

    def __init__(
        self,
        inclusion_receive_prob: float = 0.33,
        exclusion_initial_receives: int = 2,
        random_seed: int | None = None,
        enable_logging: bool = True,
    ):
        self.inclusion_receive_prob = max(0.0, min(1.0, float(inclusion_receive_prob)))
        self.exclusion_initial_receives = max(0, int(exclusion_initial_receives))
        self.enable_logging = bool(enable_logging)
        self.rng = random.Random(random_seed)

        self.toss_count_total = 0
        self.participant_received_total = 0
        self.block_idx = -1
        self.block_condition = ""
        self.toss_count_block = 0
        self.participant_received_block = 0

    @classmethod
    def from_dict(cls, config: dict) -> "Controller":
        return cls(
            inclusion_receive_prob=float(
                config.get(
                    "inclusion_receive_prob",
                    config.get("inclusion_ratio", 0.33),
                )
            ),
            exclusion_initial_receives=int(
                config.get(
                    "exclusion_initial_receives",
                    config.get("exclusion_after_tosses", 2),
                )
            ),
            random_seed=config.get("random_seed", None),
            enable_logging=bool(config.get("enable_logging", True)),
        )

    def start_block(self, block_idx: int, condition: str) -> None:
        self.block_idx = int(block_idx)
        self.block_condition = str(condition)
        self.toss_count_block = 0
        self.participant_received_block = 0

    def sample_avatar_delay(self, avatar_delay_range: list[float] | tuple[float, float] | float) -> float:
        if isinstance(avatar_delay_range, (int, float)):
            value = max(0.0, float(avatar_delay_range))
            return value

        if isinstance(avatar_delay_range, (list, tuple)) and len(avatar_delay_range) >= 2:
            low = float(avatar_delay_range[0])
            high = float(avatar_delay_range[1])
            if high < low:
                low, high = high, low
            return max(0.0, float(self.rng.uniform(low, high)))

        return 1.0

    def choose_avatar_target(self, current_holder: int, condition: str) -> int:
        if current_holder not in (PLAYER_LEFT, PLAYER_RIGHT):
            raise ValueError(f"Avatar toss requested from invalid holder: {current_holder}")

        other_avatar = PLAYER_RIGHT if current_holder == PLAYER_LEFT else PLAYER_LEFT
        condition = str(condition).strip().lower()

        if condition == "exclusion":
            if self.participant_received_block < self.exclusion_initial_receives:
                return PLAYER_PARTICIPANT
            return other_avatar

        if self.rng.random() < self.inclusion_receive_prob:
            return PLAYER_PARTICIPANT
        return other_avatar

    def fallback_participant_target(self, no_response_policy: str = "random") -> int:
        policy = str(no_response_policy or "random").strip().lower()
        if policy == "left":
            return PLAYER_LEFT
        if policy == "right":
            return PLAYER_RIGHT
        return PLAYER_LEFT if self.rng.random() < 0.5 else PLAYER_RIGHT

    def record_toss(self, from_player: int, to_player: int) -> None:
        self.toss_count_total += 1
        self.toss_count_block += 1
        if to_player == PLAYER_PARTICIPANT:
            self.participant_received_total += 1
            self.participant_received_block += 1

        if self.enable_logging:
            logging.data(
                f"[Cyberball] block={self.block_idx} toss_block={self.toss_count_block} "
                f"toss_total={self.toss_count_total} from={from_player} to={to_player} "
                f"condition={self.block_condition}"
            )


def player_key(player: int) -> str:
    if player == PLAYER_PARTICIPANT:
        return "participant"
    if player == PLAYER_LEFT:
        return "left"
    return "right"


def player_name(player: int, player_names: dict[str, str]) -> str:
    return str(player_names.get(player_key(player), player_key(player).title()))


def ball_position_for_player(stim_bank: Any, player: int):
    if player == PLAYER_PARTICIPANT:
        return stim_bank.get("participant_node").pos
    if player == PLAYER_LEFT:
        return stim_bank.get("left_node").pos
    return stim_bank.get("right_node").pos


def add_scene(
    unit: StimUnit,
    stim_bank: Any,
    *,
    holder: int,
    ball_holder: int,
    status_stim: Any = None,
    prompt_stim: Any = None,
) -> StimUnit:
    highlight_color = [1.0, 1.0, 0.0]
    for node_id, player_id in (
        ("participant_node", PLAYER_PARTICIPANT),
        ("left_node", PLAYER_LEFT),
        ("right_node", PLAYER_RIGHT),
    ):
        unit.add_stim(
            stim_bank.rebuild(
                node_id,
                lineColor=highlight_color if player_id == holder else "white",
                lineWidth=4 if player_id == holder else 3,
            )
        )

    unit.add_stim(stim_bank.get("participant_label"))
    unit.add_stim(stim_bank.get("left_label"))
    unit.add_stim(stim_bank.get("right_label"))
    unit.add_stim(stim_bank.rebuild("ball", pos=ball_position_for_player(stim_bank, ball_holder)))

    if status_stim is not None:
        unit.add_stim(status_stim)
    if prompt_stim is not None:
        unit.add_stim(prompt_stim)
    return unit
