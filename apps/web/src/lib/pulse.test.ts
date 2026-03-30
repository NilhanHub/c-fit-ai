import { describe, expect, it } from "vitest";

import {
  buildDeltaSummary,
  rankDeltaEvents,
  type DeltaEvent,
} from "./pulse";

describe("rankDeltaEvents", () => {
  it("puts urgent action-first changes above passive updates", () => {
    const events: DeltaEvent[] = [
      {
        id: "event-status",
        kind: "status_moved",
        minutesAgo: 12,
        urgencyScore: 72,
        trustScore: 88,
      },
      {
        id: "event-walkin",
        kind: "walk_in_opening",
        minutesAgo: 4,
        urgencyScore: 98,
        trustScore: 91,
      },
      {
        id: "event-digest",
        kind: "digest_ready",
        minutesAgo: 1,
        urgencyScore: 22,
        trustScore: 90,
      },
    ];

    const ranked = rankDeltaEvents(events);

    expect(ranked.map((event) => event.id)).toEqual([
      "event-walkin",
      "event-status",
      "event-digest",
    ]);
  });
});

describe("buildDeltaSummary", () => {
  it("counts the meaningful movement since the last visit", () => {
    const events: DeltaEvent[] = [
      {
        id: "event-1",
        kind: "new_job",
        minutesAgo: 18,
        urgencyScore: 84,
        trustScore: 94,
      },
      {
        id: "event-2",
        kind: "salary_disclosed",
        minutesAgo: 20,
        urgencyScore: 76,
        trustScore: 91,
      },
      {
        id: "event-3",
        kind: "status_moved",
        minutesAgo: 8,
        urgencyScore: 89,
        trustScore: 90,
      },
      {
        id: "event-4",
        kind: "story_went_live",
        minutesAgo: 6,
        urgencyScore: 80,
        trustScore: 87,
      },
    ];

    expect(buildDeltaSummary(events)).toEqual({
      newJobs: 1,
      statusMoves: 1,
      trustShifts: 1,
      liveStories: 1,
      urgentNow: 4,
    });
  });
});
