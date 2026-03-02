from __future__ import annotations

from functools import partial
from typing import Any

from psyflow import StimUnit, set_trial_context

from .utils import PLAYER_LEFT, PLAYER_PARTICIPANT, PLAYER_RIGHT


def _deadline_s(value: Any) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, (list, tuple)) and value:
        try:
            return float(max(value))
        except Exception:
            return None
    return None


def _player_key(player: int) -> str:
    if player == PLAYER_PARTICIPANT:
        return "participant"
    if player == PLAYER_LEFT:
        return "left"
    return "right"


def _player_name(player: int, player_names: dict[str, str]) -> str:
    return str(player_names.get(_player_key(player), _player_key(player).title()))


def _trial_id(controller) -> int:
    if hasattr(controller, "next_trial_id"):
        return int(controller.next_trial_id())
    return 1


def _sample_avatar_delay(controller, value: Any, default_value: float) -> float:
    if hasattr(controller, "sample_avatar_delay"):
        return float(controller.sample_avatar_delay(value))
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, (list, tuple)) and value:
        try:
            return float(max(value))
        except Exception:
            return float(default_value)
    return float(default_value)


def _toss_start_trigger(settings, to_player: int):
    if to_player == PLAYER_PARTICIPANT:
        return settings.triggers.get("toss_start_to_participant")
    if to_player == PLAYER_LEFT:
        return settings.triggers.get("toss_start_to_left")
    return settings.triggers.get("toss_start_to_right")


def _ball_position_for_player(stim_bank, player: int):
    if player == PLAYER_PARTICIPANT:
        return stim_bank.get("participant_node").pos
    if player == PLAYER_LEFT:
        return stim_bank.get("left_node").pos
    return stim_bank.get("right_node").pos


def _add_scene(
    unit: StimUnit,
    stim_bank,
    *,
    holder: int,
    ball_holder: int,
    status_stim=None,
    prompt_stim=None,
) -> StimUnit:
    highlight_color = [1.0, 1.0, 0.0]
    for node_id, player_id in (
        ("participant_node", PLAYER_PARTICIPANT),
        ("left_node", PLAYER_LEFT),
        ("right_node", PLAYER_RIGHT),
    ):
        node_stim = stim_bank.rebuild(
            node_id,
            lineColor=highlight_color if player_id == holder else "white",
            lineWidth=4 if player_id == holder else 3,
        )
        unit.add_stim(node_stim)

    unit.add_stim(stim_bank.get("participant_label"))
    unit.add_stim(stim_bank.get("left_label"))
    unit.add_stim(stim_bank.get("right_label"))
    unit.add_stim(stim_bank.rebuild("ball", pos=_ball_position_for_player(stim_bank, ball_holder)))

    if status_stim is not None:
        unit.add_stim(status_stim)
    if prompt_stim is not None:
        unit.add_stim(prompt_stim)
    return unit


def run_trial(
    win,
    kb,
    settings,
    condition,
    stim_bank,
    controller,
    trigger_runtime,
    ball_state=None,
    block_id=None,
    block_idx=None,
):
    """Run one toss event in the Cyberball state machine."""
    trial_id = _trial_id(controller)
    block_label = str(block_id) if block_id is not None else "block_0"
    block_index = int(block_idx) if block_idx is not None else 0
    trial_index = int(getattr(controller, "toss_count_block", 0)) + 1
    condition_label = str(condition).strip().lower()

    if not isinstance(ball_state, dict):
        ball_state = {"holder": PLAYER_LEFT}
    holder_before = int(ball_state.get("holder", PLAYER_LEFT))
    if holder_before not in (PLAYER_PARTICIPANT, PLAYER_LEFT, PLAYER_RIGHT):
        holder_before = PLAYER_LEFT

    player_names_cfg = getattr(settings, "player_names", {})
    if not isinstance(player_names_cfg, dict):
        player_names_cfg = {}
    player_names = {
        "participant": str(player_names_cfg.get("participant", "You")),
        "left": str(player_names_cfg.get("left", "Player A")),
        "right": str(player_names_cfg.get("right", "Player B")),
    }

    total_tosses = int(getattr(settings, "trial_per_block", 0) or 0)
    if total_tosses <= 0:
        total_tosses = int(getattr(settings, "total_trials", 1) or 1)

    status_stim = stim_bank.get_and_format(
        "status_line",
        condition_name=condition_label.title(),
        toss_num=trial_index,
        total_tosses=total_tosses,
    )

    make_unit = partial(StimUnit, win=win, kb=kb, runtime=trigger_runtime)

    from_player = holder_before
    to_player = holder_before
    participant_turn = holder_before == PLAYER_PARTICIPANT
    participant_response = ""
    participant_rt = None
    participant_timed_out = False

    if participant_turn:
        left_key = str(getattr(settings, "left_key", "f")).strip().lower()
        right_key = str(getattr(settings, "right_key", "j")).strip().lower()
        response_keys = [left_key, right_key]
        participant_timeout = float(getattr(settings, "participant_timeout", 2.5))

        participant_prompt = stim_bank.get("participant_prompt")
        participant_phase = make_unit(unit_label="participant_turn")
        _add_scene(
            participant_phase,
            stim_bank,
            holder=holder_before,
            ball_holder=holder_before,
            status_stim=status_stim,
            prompt_stim=participant_prompt,
        )
        set_trial_context(
            participant_phase,
            trial_id=trial_id,
            phase="participant_turn",
            deadline_s=_deadline_s(participant_timeout),
            valid_keys=response_keys,
            block_id=block_label,
            condition_id=condition_label,
            task_factors={
                "condition": condition_label,
                "holder_before": _player_key(holder_before),
                "participant_turn": True,
                "left_key": left_key,
                "right_key": right_key,
                "block_idx": block_index,
            },
            stim_id="cyberball_scene+participant_prompt+status_line",
        )
        participant_phase.capture_response(
            keys=response_keys,
            duration=participant_timeout,
            onset_trigger=settings.triggers.get("participant_turn_onset"),
            response_trigger={
                left_key: settings.triggers.get("participant_choice_left"),
                right_key: settings.triggers.get("participant_choice_right"),
            },
            timeout_trigger=settings.triggers.get("participant_timeout"),
        )
        participant_phase.to_dict()

        response_key = str(participant_phase.get_state("response", "")).strip().lower()
        rt_value = participant_phase.get_state("rt", None)
        participant_rt = float(rt_value) if isinstance(rt_value, (int, float)) else None
        if response_key == left_key:
            to_player = PLAYER_LEFT
            participant_response = left_key
        elif response_key == right_key:
            to_player = PLAYER_RIGHT
            participant_response = right_key
        else:
            participant_timed_out = True
            to_player = int(
                controller.fallback_participant_target(
                    getattr(settings, "no_response_policy", "random")
                )
            )
    else:
        avatar_delay = _sample_avatar_delay(controller, settings.avatar_decision_delay, 1.0)
        avatar_prompt = stim_bank.get_and_format(
            "avatar_wait_prompt",
            holder_name=_player_name(holder_before, player_names),
        )

        avatar_phase = make_unit(unit_label="avatar_turn")
        _add_scene(
            avatar_phase,
            stim_bank,
            holder=holder_before,
            ball_holder=holder_before,
            status_stim=status_stim,
            prompt_stim=avatar_prompt,
        )
        set_trial_context(
            avatar_phase,
            trial_id=trial_id,
            phase="avatar_turn",
            deadline_s=_deadline_s(avatar_delay),
            valid_keys=[],
            block_id=block_label,
            condition_id=condition_label,
            task_factors={
                "condition": condition_label,
                "holder_before": _player_key(holder_before),
                "participant_turn": False,
                "block_idx": block_index,
            },
            stim_id="cyberball_scene+avatar_wait_prompt+status_line",
        )
        avatar_phase.show(
            duration=avatar_delay,
            onset_trigger=settings.triggers.get("avatar_turn_onset"),
        ).to_dict()
        to_player = int(controller.choose_avatar_target(holder_before, condition_label))

    toss_duration = float(getattr(settings, "toss_animation_duration", 0.45))
    toss_phase = make_unit(unit_label="toss_animation")
    _add_scene(
        toss_phase,
        stim_bank,
        holder=holder_before,
        ball_holder=to_player,
        status_stim=status_stim,
        prompt_stim=None,
    )
    set_trial_context(
        toss_phase,
        trial_id=trial_id,
        phase="toss_animation",
        deadline_s=_deadline_s(toss_duration),
        valid_keys=[],
        block_id=block_label,
        condition_id=condition_label,
        task_factors={
            "condition": condition_label,
            "from_player": _player_key(holder_before),
            "to_player": _player_key(to_player),
            "participant_turn": bool(participant_turn),
            "block_idx": block_index,
        },
        stim_id="cyberball_scene+status_line",
    )
    toss_phase.show(
        duration=toss_duration,
        onset_trigger=_toss_start_trigger(settings, to_player),
    ).to_dict()
    trigger_runtime.send(settings.triggers.get("toss_end"))

    inter_toss_interval = float(getattr(settings, "inter_toss_interval", 0.0))
    if inter_toss_interval > 0:
        inter_toss = make_unit(unit_label="inter_toss")
        _add_scene(
            inter_toss,
            stim_bank,
            holder=to_player,
            ball_holder=to_player,
            status_stim=status_stim,
            prompt_stim=None,
        )
        set_trial_context(
            inter_toss,
            trial_id=trial_id,
            phase="inter_toss",
            deadline_s=_deadline_s(inter_toss_interval),
            valid_keys=[],
            block_id=block_label,
            condition_id=condition_label,
            task_factors={
                "condition": condition_label,
                "holder_after": _player_key(to_player),
                "participant_turn": bool(participant_turn),
                "block_idx": block_index,
            },
            stim_id="cyberball_scene+status_line",
        )
        inter_toss.show(duration=inter_toss_interval).to_dict()

    controller.record_toss(from_player=from_player, to_player=to_player)
    ball_state["holder"] = int(to_player)

    trial_data = {
        "condition": condition_label,
        "trial_id": trial_id,
        "trial_index": trial_index,
        "block_id": block_label,
        "block_idx": block_index,
        "from_player": int(from_player),
        "to_player": int(to_player),
        "from_player_id": _player_key(from_player),
        "to_player_id": _player_key(to_player),
        "from_player_name": _player_name(from_player, player_names),
        "to_player_name": _player_name(to_player, player_names),
        "participant_turn": bool(participant_turn),
        "avatar_turn": bool(not participant_turn),
        "participant_response": participant_response,
        "participant_rt": participant_rt,
        "participant_timed_out": bool(participant_timed_out),
        "participant_received": bool(to_player == PLAYER_PARTICIPANT),
    }
    return trial_data
