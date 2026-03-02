from functools import partial
from pathlib import Path

import pandas as pd
from psychopy import core

from psyflow import (
    BlockUnit,
    StimBank,
    StimUnit,
    SubInfo,
    TaskRunOptions,
    TaskSettings,
    context_from_config,
    count_down,
    initialize_exp,
    initialize_triggers,
    load_config,
    parse_task_run_options,
    runtime_context,
)

from src import Controller, run_trial


def _make_qa_trigger_runtime():
    return initialize_triggers(mock=True)


MODES = ("human", "qa", "sim")
DEFAULT_CONFIG_BY_MODE = {
    "human": "config/config.yaml",
    "qa": "config/config_qa.yaml",
    "sim": "config/config_scripted_sim.yaml",
}


def _parse_args(task_root: Path) -> TaskRunOptions:
    return parse_task_run_options(
        task_root=task_root,
        description="Run Cyberball Task in human/qa/sim mode.",
        default_config_by_mode=DEFAULT_CONFIG_BY_MODE,
        modes=MODES,
    )


def run(options: TaskRunOptions):
    task_root = Path(__file__).resolve().parent
    cfg = load_config(str(options.config_path))
    mode = options.mode

    ctx = None
    if mode in ("qa", "sim"):
        ctx = context_from_config(task_dir=task_root, config=cfg, mode=mode)
        sim_participant = "sim"
        if ctx.session is not None:
            sim_participant = str(ctx.session.participant_id or "sim")
        with runtime_context(ctx):
            _run_impl(mode=mode, output_dir=ctx.output_dir, cfg=cfg, participant_id=sim_participant)
    else:
        _run_impl(mode=mode, output_dir=None, cfg=cfg, participant_id="human")


def _run_impl(*, mode: str, output_dir: Path | None, cfg: dict, participant_id: str):
    # 2. Collect subject info
    if mode == "qa":
        subject_data = {"subject_id": "qa"}
    elif mode == "sim":
        subject_data = {"subject_id": participant_id}
    else:
        subform = SubInfo(cfg["subform_config"])
        subject_data = subform.collect()

    # 3. Load task settings
    settings = TaskSettings.from_dict(cfg["task_config"])
    if mode in ("qa", "sim") and output_dir is not None:
        settings.save_path = str(output_dir)

    settings.add_subinfo(subject_data)

    if mode == "qa" and output_dir is not None:
        output_dir.mkdir(parents=True, exist_ok=True)
        settings.res_file = str(output_dir / "qa_trace.csv")
        settings.log_file = str(output_dir / "qa_psychopy.log")
        settings.json_file = str(output_dir / "qa_settings.json")

    # 4. Setup triggers
    settings.triggers = cfg["trigger_config"]
    if mode in ("qa", "sim"):
        trigger_runtime = _make_qa_trigger_runtime()
    else:
        trigger_runtime = initialize_triggers(cfg)

    # 5. Set up window & input
    win, kb = initialize_exp(settings)

    # 6. Setup stimulus bank
    stim_bank = StimBank(win, cfg["stim_config"])
    stim_bank = stim_bank.preload_all()

    # 7. Setup controller
    settings.controller = cfg["controller_config"]
    settings.save_to_json()
    controller = Controller.from_dict(settings.controller)

    trigger_runtime.send(settings.triggers.get("exp_onset"))

    # Instruction
    StimUnit("instruction_text", win, kb, runtime=trigger_runtime).add_stim(
        stim_bank.get("instruction_text")
    ).wait_and_continue()

    all_data = []
    total_blocks = int(getattr(settings, "total_blocks", 1))
    trial_per_block = int(getattr(settings, "trial_per_block", 0) or 0)
    if trial_per_block <= 0:
        total_trials = int(getattr(settings, "total_trials", total_blocks) or total_blocks)
        trial_per_block = max(1, total_trials // max(1, total_blocks))

    for block_i in range(total_blocks):
        condition = settings.conditions[block_i % len(settings.conditions)]
        controller.start_block(block_idx=block_i, condition=str(condition))
        ball_state = {"holder": 1}

        if mode not in ("qa", "sim"):
            count_down(win, 3, color="black")

        block = (
            BlockUnit(
                block_id=f"block_{block_i}",
                block_idx=block_i,
                settings=settings,
                window=win,
                keyboard=kb,
            )
                # Use one repeated block condition; each trial is one toss event.
                .add_condition([condition] * trial_per_block)
                .on_start(lambda b: trigger_runtime.send(settings.triggers.get("block_onset")))
                .on_end(lambda b: trigger_runtime.send(settings.triggers.get("block_end")))
                .run_trial(
                    partial(
                        run_trial,
                        stim_bank=stim_bank,
                        controller=controller,
                        trigger_runtime=trigger_runtime,
                        ball_state=ball_state, # Shared state across trials
                        block_id=f"block_{block_i}",
                        block_idx=block_i,
                    )
                )
                .to_dict(all_data)
            )

        block_trials = block.get_all_data()
        participant_receives = sum(1 for trial in block_trials if bool(trial.get("participant_received", False)))
        participant_turns = sum(1 for trial in block_trials if bool(trial.get("participant_turn", False)))

        if block_i < (total_blocks - 1):
            StimUnit("block", win, kb, runtime=trigger_runtime).add_stim(
                stim_bank.get_and_format(
                    "block_break",
                    block_num=block_i + 1,
                    total_blocks=total_blocks,
                    condition_name=str(condition).title(),
                    participant_receives=participant_receives,
                    participant_turns=participant_turns,
                )
            ).wait_and_continue()

    participant_receives_total = sum(1 for trial in all_data if bool(trial.get("participant_received", False)))
    participant_turns_total = sum(1 for trial in all_data if bool(trial.get("participant_turn", False)))

    StimUnit("goodbye", win, kb, runtime=trigger_runtime).add_stim(
        stim_bank.get_and_format(
            "good_bye",
            participant_receives_total=participant_receives_total,
            participant_turns_total=participant_turns_total,
            total_tosses=len(all_data),
        )
    ).wait_and_continue(terminate=True)

    trigger_runtime.send(settings.triggers.get("exp_end"))

    # 9. Save data
    df = pd.DataFrame(all_data)
    df.to_csv(settings.res_file, index=False)

    # 10. Close everything
    trigger_runtime.close()
    core.quit()


def main() -> None:
    task_root = Path(__file__).resolve().parent
    options = _parse_args(task_root)
    run(options)


if __name__ == "__main__":
    main()
