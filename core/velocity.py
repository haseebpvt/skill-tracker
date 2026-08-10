"""Velocity and forecasting from the event history.

Progress is measured in **points**: each topic is worth 1.0, and a status is
worth a fraction of it (:data:`core.models.STATUS_WEIGHTS`) — the same scale the
progress percentages use, so the chart and the header can never disagree.

A note on honesty: a forecast built from three data points is numerology. This
module refuses to project a completion date unless there is enough history to
justify one, and always reports the sample size and a confidence level so the
caller can say *why* it is or is not confident.
"""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from .history import STATUS_CHANGE, Event
from .models import STATUS_WEIGHTS, Topic

#: Trailing window used for the velocity estimate.
DEFAULT_WINDOW_DAYS = 14

#: Below this many status changes in the window, we do not project a date.
MIN_EVENTS_FOR_FORECAST = 3

#: ...and they must be spread over at least this many distinct days. Without
#: this, one productive afternoon becomes "21 topics/week" and the projection
#: says you will finish tomorrow. A rate needs a span, not just a count.
MIN_ACTIVE_DAYS_FOR_FORECAST = 3

#: Sample sizes at which confidence steps up.
_MEDIUM_CONFIDENCE_EVENTS = 6
_HIGH_CONFIDENCE_EVENTS = 12

#: Slack, in days, within which "projected" counts as "on track" vs the target.
_ON_TRACK_TOLERANCE_DAYS = 2

#: Cap on how far ahead we are willing to draw a projection line.
_MAX_PROJECTION_DAYS = 365


def _weight(status: str) -> float:
    return STATUS_WEIGHTS.get(status, 0.0)


def _points_delta(event: Event) -> float:
    """How many points a status change was worth (can be negative)."""
    if event.type != STATUS_CHANGE:
        return 0.0
    return _weight(event.to_status) - _weight(event.from_status)


def compute(
    events: list[Event],
    topics: list[Topic],
    *,
    today: date,
    target_date: str | None = None,
    start_date: str | None = None,
    window_days: int = DEFAULT_WINDOW_DAYS,
) -> dict[str, Any]:
    """Build the velocity payload: history series, rate, and forecast."""
    total_points = float(len(topics))
    earned_points = sum(_weight(t.status) for t in topics)
    remaining = max(total_points - earned_points, 0.0)
    percent = round(100 * earned_points / total_points, 1) if total_points else 0.0

    status_events = [e for e in events if e.type == STATUS_CHANGE and e.date]

    # Topics that already had a status before the log existed contribute a
    # baseline, otherwise the curve would start above zero with no explanation.
    recorded = sum(_points_delta(e) for e in status_events)
    baseline = max(earned_points - recorded, 0.0)

    series = _build_series(status_events, baseline, total_points, today=today, start_date=start_date)

    window_start = today - timedelta(days=window_days)
    in_window = [e for e in status_events if _as_date(e.date) and _as_date(e.date) > window_start]
    gained_in_window = sum(max(_points_delta(e), 0.0) for e in in_window)

    # Measure over the observed span, not the nominal window: two events three
    # days apart is 3 days of evidence, not 14.
    observed_days = _observed_days(in_window, today=today, window_days=window_days)
    points_per_day = (gained_in_window / observed_days) if observed_days > 0 else 0.0

    active_days = len({e.date for e in in_window})
    forecast = _forecast(
        points_per_day=points_per_day,
        remaining=remaining,
        events_in_window=len(in_window),
        active_days=active_days,
        today=today,
        target_date=target_date,
    )

    return {
        "has_data": bool(status_events),
        "window_days": window_days,
        "events_in_window": len(in_window),
        "active_days": active_days,
        "observed_days": round(observed_days, 1),
        "points_per_day": round(points_per_day, 3),
        "topics_per_week": round(points_per_day * 7, 2),
        "total_points": round(total_points, 2),
        "earned_points": round(earned_points, 2),
        "remaining_points": round(remaining, 2),
        "percent": percent,
        "baseline_points": round(baseline, 2),
        "forecast": forecast,
        "series": series,
        "projection": _projection(series, points_per_day, total_points, forecast, today=today),
        "target_line": _target_line(series, start_date, target_date, baseline, total_points),
    }


def _build_series(
    status_events: list[Event],
    baseline: float,
    total_points: float,
    *,
    today: date,
    start_date: str | None,
) -> list[dict[str, Any]]:
    """Cumulative earned points per day, from the first known day to today."""
    if not status_events and not start_date:
        return []

    by_day: dict[str, float] = {}
    for event in status_events:
        by_day[event.date] = by_day.get(event.date, 0.0) + _points_delta(event)

    first_event_day = min(by_day) if by_day else None
    candidates = [d for d in (_as_date(start_date), _as_date(first_event_day)) if d]
    if not candidates:
        return []
    first = min(candidates)
    if first > today:
        first = today

    series: list[dict[str, Any]] = []
    running = baseline
    cursor = first
    while cursor <= today:
        key = cursor.isoformat()
        running += by_day.get(key, 0.0)
        series.append(
            {
                "date": key,
                "earned": round(running, 3),
                "percent": round(100 * running / total_points, 2) if total_points else 0.0,
            }
        )
        cursor += timedelta(days=1)
    return series


def _observed_days(in_window: list[Event], *, today: date, window_days: int) -> float:
    if not in_window:
        return 0.0
    first = _as_date(min(e.date for e in in_window))
    if first is None:
        return 0.0
    # At least one day, so a single busy day does not divide by zero.
    return float(max((today - first).days, 1))


def _forecast(
    *,
    points_per_day: float,
    remaining: float,
    events_in_window: int,
    active_days: int,
    today: date,
    target_date: str | None,
) -> dict[str, Any]:
    target = _as_date(target_date)
    base: dict[str, Any] = {
        "available": False,
        "projected_date": None,
        "days_to_finish": None,
        "target_date": target.isoformat() if target else None,
        "days_vs_target": None,
        "verdict": "unknown",
        "required_points_per_day": None,
        "confidence": "low",
        "reason": "",
    }

    if target and remaining > 0:
        days_left = (target - today).days
        base["required_points_per_day"] = round(remaining / days_left, 3) if days_left > 0 else None

    if remaining <= 0:
        return {**base, "available": True, "verdict": "ahead", "days_to_finish": 0,
                "projected_date": today.isoformat(), "confidence": "high",
                "reason": "everything is already at comfortable or better"}

    if events_in_window < MIN_EVENTS_FOR_FORECAST:
        return {
            **base,
            "reason": (
                f"only {events_in_window} status change(s) recorded in the last "
                f"{DEFAULT_WINDOW_DAYS} days — need at least {MIN_EVENTS_FOR_FORECAST} to project a date"
            ),
        }

    if active_days < MIN_ACTIVE_DAYS_FOR_FORECAST:
        return {
            **base,
            "reason": (
                f"all {events_in_window} status change(s) fall on {active_days} day(s) — "
                f"need activity across at least {MIN_ACTIVE_DAYS_FOR_FORECAST} different days "
                "before a rate means anything"
            ),
        }

    if points_per_day <= 0:
        return {**base, "reason": "no forward progress recorded in the window"}

    days_to_finish = int(round(remaining / points_per_day))
    if days_to_finish > _MAX_PROJECTION_DAYS:
        return {
            **base,
            "reason": f"at the current rate this would take over {_MAX_PROJECTION_DAYS} days",
        }

    projected = today + timedelta(days=days_to_finish)
    confidence = (
        "high" if events_in_window >= _HIGH_CONFIDENCE_EVENTS
        else "medium" if events_in_window >= _MEDIUM_CONFIDENCE_EVENTS
        else "low"
    )

    verdict = "unknown"
    days_vs_target = None
    if target:
        days_vs_target = (projected - target).days
        if days_vs_target > _ON_TRACK_TOLERANCE_DAYS:
            verdict = "behind"
        elif days_vs_target < -_ON_TRACK_TOLERANCE_DAYS:
            verdict = "ahead"
        else:
            verdict = "on-track"

    return {
        **base,
        "available": True,
        "projected_date": projected.isoformat(),
        "days_to_finish": days_to_finish,
        "days_vs_target": days_vs_target,
        "verdict": verdict,
        "confidence": confidence,
        "reason": f"based on {events_in_window} status change(s) in the last {DEFAULT_WINDOW_DAYS} days",
    }


def _projection(
    series: list[dict[str, Any]],
    points_per_day: float,
    total_points: float,
    forecast: dict[str, Any],
    *,
    today: date,
) -> list[dict[str, Any]]:
    """The dashed forward line, from today to the projected finish."""
    if not series or not forecast.get("available") or points_per_day <= 0 or not total_points:
        return []

    days = forecast.get("days_to_finish") or 0
    if days <= 0:
        return []

    running = series[-1]["earned"]
    points: list[dict[str, Any]] = []
    for offset in range(1, days + 1):
        running = min(running + points_per_day, total_points)
        points.append(
            {
                "date": (today + timedelta(days=offset)).isoformat(),
                "percent": round(100 * running / total_points, 2),
            }
        )
    return points


def _target_line(
    series: list[dict[str, Any]],
    start_date: str | None,
    target_date: str | None,
    baseline: float,
    total_points: float,
) -> list[dict[str, Any]]:
    """The straight line you would follow to hit the target exactly on time."""
    start = _as_date(start_date) or (_as_date(series[0]["date"]) if series else None)
    target = _as_date(target_date)
    if not start or not target or target <= start or not total_points:
        return []

    return [
        {"date": start.isoformat(), "percent": round(100 * baseline / total_points, 2)},
        {"date": target.isoformat(), "percent": 100.0},
    ]


def _as_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(str(value)[:10])
    except ValueError:
        return None
