"""Tests for the main application entry point."""

import runpy

from flask import Flask


def test_main_entry_point_runs_application(monkeypatch):
    run_calls = []

    def fake_run(self, **kwargs):
        run_calls.append(kwargs)

    monkeypatch.setattr(Flask, "run", fake_run)

    runpy.run_path("app/main.py", run_name="__main__")

    assert len(run_calls) == 1
    assert run_calls[0]["debug"] is False
