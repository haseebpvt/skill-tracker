"""The event log, the velocity estimate, and the generated ROADMAP.md."""

from __future__ import annotations

from datetime import date, timedelta

from core import velocity as velocity_mod
from core.history import STATUS_CHANGE, Event, append_events, read_events
from core.models import Topic
from core.render import bar, render_roadmap_doc
from core.repo import Repo

TODAY = date(2026, 8, 20)


def make_topics(count: int, status: str = "not-started") -> list[Topic]:
    return [Topic(id=f"t{i}", title=f"T{i}", status=status) for i in range(count)]


def change(days_ago: int, topic_id: str, to_status: str, from_status: str = "not-started") -> Event:
    stamp = (TODAY - timedelta(days=days_ago)).isoformat()
    return Event(
        ts=f"{stamp}T09:00:00Z",
        type=STATUS_CHANGE,
        topic_id=topic_id,
        from_status=from_status,
        to_status=to_status,
    )


# ----------------------------------------------------------------------
# History log
# ----------------------------------------------------------------------


def test_append_and_read_round_trip(repo: Repo):
    append_events(repo.root, [change(1, "t0", "learning"), change(0, "t0", "comfortable", "learning")])
    events, issues = read_events(repo.root)
    assert not issues
    assert [e.to_status for e in events] == ["learning", "comfortable"]


def test_append_never_rewrites_earlier_lines(repo: Repo):
    append_events(repo.root, [change(2, "t0", "learning")])
    first = (repo.root / "data/history.jsonl").read_text()
    append_events(repo.root, [change(1, "t1", "learning")])
    assert (repo.root / "data/history.jsonl").read_text().startswith(first)


def test_malformed_lines_are_skipped_not_fatal(repo: Repo):
    path = repo.root / "data/history.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('{"ts":"2026-08-01T00:00:00Z","type":"note"}\nnot json\n{"type":"note"}\n')
    events, issues = read_events(repo.root)
    assert len(events) == 1
    assert len(issues) == 2


def test_events_are_sorted_by_timestamp(repo: Repo):
    append_events(repo.root, [change(0, "t0", "learning"), change(5, "t1", "learning")])
    events, _ = read_events(repo.root)
    assert events[0].ts < events[1].ts


def test_writes_record_events(repo: Repo):
    repo.update_topic_status("alpha", "first-topic", "comfortable", note="probed it")
    events, _ = read_events(repo.root)
    assert len(events) == 1
    event = events[0]
    assert event.type == STATUS_CHANGE
    assert (event.from_status, event.to_status) == ("learning", "comfortable")
    assert event.note == "probed it"
    assert event.ts.endswith("Z")


def test_every_write_regenerates_the_roadmap_doc(repo: Repo):
    doc = repo.root / "ROADMAP.md"
    assert not doc.exists()
    repo.update_topic_status("alpha", "first-topic", "comfortable")
    assert doc.is_file()
    assert "GENERATED FILE" in doc.read_text()


# ----------------------------------------------------------------------
# Velocity
# ----------------------------------------------------------------------


def test_no_events_means_no_forecast():
    result = velocity_mod.compute([], make_topics(10), today=TODAY, target_date="2026-09-01")
    assert result["has_data"] is False
    assert result["forecast"]["available"] is False
    assert result["forecast"]["projected_date"] is None


def test_thin_history_refuses_to_project():
    """Two data points is not a trend — say so instead of inventing a date."""
    events = [change(3, "t0", "strong"), change(1, "t1", "strong")]
    result = velocity_mod.compute(events, make_topics(10), today=TODAY, target_date="2026-09-01")
    forecast = result["forecast"]
    assert forecast["available"] is False
    assert "at least 3" in forecast["reason"]


def test_forecast_appears_once_there_is_enough_history():
    events = [change(days, f"t{i}", "strong") for i, days in enumerate([8, 6, 4, 2])]
    topics = make_topics(10)
    for topic in topics[:4]:
        topic.status = "strong"

    result = velocity_mod.compute(events, topics, today=TODAY, target_date="2026-09-30")
    forecast = result["forecast"]
    assert forecast["available"] is True
    assert forecast["projected_date"] is not None
    # 4 points over 8 observed days = 0.5/day, 6 remaining -> ~12 days.
    assert result["points_per_day"] == 0.5
    assert forecast["days_to_finish"] == 12


def test_confidence_scales_with_sample_size():
    topics = make_topics(40)
    for count, expected in ((4, "low"), (8, "medium"), (13, "high")):
        # Spread across distinct days, otherwise the burst guard blocks the forecast.
        events = [change(12 - (i % 10), f"t{i}", "strong") for i in range(count)]
        for topic in topics[:count]:
            topic.status = "strong"
        result = velocity_mod.compute(events, topics, today=TODAY)
        assert result["forecast"]["confidence"] == expected, count
        for topic in topics:
            topic.status = "not-started"


def test_a_single_busy_day_does_not_become_a_rate():
    """One productive afternoon is not evidence of a weekly pace."""
    topics = make_topics(10)
    for topic in topics[:4]:
        topic.status = "strong"
    same_day = [change(0, f"t{i}", "strong") for i in range(4)]

    result = velocity_mod.compute(same_day, topics, today=TODAY, target_date="2026-09-30")
    assert result["active_days"] == 1
    assert result["forecast"]["available"] is False
    assert "different days" in result["forecast"]["reason"]


def test_verdict_compares_projection_against_the_target():
    topics = make_topics(10)
    for topic in topics[:4]:
        topic.status = "strong"
    events = [change(days, f"t{i}", "strong") for i, days in enumerate([8, 6, 4, 2])]

    behind = velocity_mod.compute(events, topics, today=TODAY, target_date="2026-08-25")
    ahead = velocity_mod.compute(events, topics, today=TODAY, target_date="2026-10-30")
    assert behind["forecast"]["verdict"] == "behind"
    assert ahead["forecast"]["verdict"] == "ahead"


def test_finished_work_reports_ahead_not_a_projection():
    result = velocity_mod.compute([], make_topics(5, "strong"), today=TODAY, target_date="2026-09-01")
    assert result["remaining_points"] == 0
    assert result["forecast"]["verdict"] == "ahead"


def test_partial_statuses_count_fractionally():
    topics = make_topics(3)
    topics[0].status = "learning"      # 1/3
    topics[1].status = "comfortable"   # 2/3
    result = velocity_mod.compute([], topics, today=TODAY)
    assert result["earned_points"] == 1.0
    assert result["percent"] == 33.3


def test_baseline_explains_progress_made_before_the_log_existed():
    """Topics already advanced with no events must not make the curve start at 0."""
    topics = make_topics(10)
    for topic in topics[:5]:
        topic.status = "strong"
    result = velocity_mod.compute([change(2, "t0", "strong")], topics, today=TODAY)
    # 5 points earned, 1 of them recorded -> baseline of 4.
    assert result["baseline_points"] == 4.0
    assert result["series"][0]["earned"] >= 4.0


def test_series_is_daily_and_ends_today():
    events = [change(3, "t0", "strong"), change(1, "t1", "strong")]
    result = velocity_mod.compute(events, make_topics(10), today=TODAY)
    dates = [point["date"] for point in result["series"]]
    assert dates[-1] == TODAY.isoformat()
    assert dates == sorted(dates)
    assert len(set(dates)) == len(dates)


def test_series_is_monotonic_for_forward_progress():
    events = [change(days, f"t{i}", "strong") for i, days in enumerate([6, 4, 2])]
    result = velocity_mod.compute(events, make_topics(10), today=TODAY)
    earned = [point["earned"] for point in result["series"]]
    assert earned == sorted(earned)


def test_target_line_runs_from_start_to_full():
    result = velocity_mod.compute(
        [change(1, "t0", "strong")], make_topics(10), today=TODAY,
        start_date="2026-08-01", target_date="2026-09-01",
    )
    line = result["target_line"]
    assert line[0]["date"] == "2026-08-01"
    assert line[-1] == {"date": "2026-09-01", "percent": 100.0}


def test_projection_is_empty_without_a_forecast():
    result = velocity_mod.compute([change(1, "t0", "strong")], make_topics(10), today=TODAY)
    assert result["projection"] == []


def test_projection_never_exceeds_one_hundred_percent():
    topics = make_topics(10)
    for topic in topics[:8]:
        topic.status = "strong"
    events = [change(days, f"t{i}", "strong") for i, days in enumerate([8, 6, 4, 2])]
    result = velocity_mod.compute(events, topics, today=TODAY, target_date="2026-09-30")
    assert all(point["percent"] <= 100.0 for point in result["projection"])


# ----------------------------------------------------------------------
# Rendered document
# ----------------------------------------------------------------------


def test_bar_is_proportional():
    assert bar(0, 10) == "░" * 10
    assert bar(100, 10) == "█" * 10
    assert bar(50, 10).count("█") == 5


def test_rendered_doc_states_when_it_cannot_forecast(repo: Repo):
    state = repo.load()
    doc = render_roadmap_doc(state.to_dict(), state.events, today=TODAY)
    assert "not enough history yet" in doc
    assert "GENERATED FILE" in doc


def test_rendered_doc_lists_milestones_and_activity(repo: Repo):
    repo.set_roadmap_meta(start_date="2026-08-01", target_date="2026-09-01")
    repo.set_milestone("w1", title="Week 1", target="2026-08-25", skills=["alpha"])
    repo.update_topic_status("alpha", "first-topic", "comfortable", note="explained it cleanly")

    doc = (repo.root / "ROADMAP.md").read_text()
    assert "Week 1" in doc
    assert "explained it cleanly" in doc
    assert "## Recent activity" in doc


def test_rendered_doc_surfaces_broken_milestone_references(repo: Repo):
    repo.set_milestone("w1", title="Week 1", skills=["alpha"])
    # Delete a topic out from under the milestone by rewriting the file.
    path = repo.root / "data" / "skills" / "alpha" / "topics.md"
    path.write_text("## First topic\n- id: first-topic\n- priority: 1\n", encoding="utf-8")
    repo.set_milestone("w1", topics=["first-topic"])

    state = repo.load()
    derived = state.roadmap_view()["milestones"][0]
    assert derived["progress"]["total"] == 1
