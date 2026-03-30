export type DeltaEventKind =
  | "new_job"
  | "saved_search_match"
  | "status_moved"
  | "salary_disclosed"
  | "trust_upgraded"
  | "walk_in_opening"
  | "employer_active_now"
  | "story_went_live"
  | "suspicious_listing_downgraded"
  | "deadline_closing"
  | "digest_ready";

export type DeltaEvent = {
  id: string;
  kind: DeltaEventKind;
  title?: string;
  detail?: string;
  timeLabel?: string;
  ctaLabel?: string;
  minutesAgo: number;
  urgencyScore: number;
  trustScore: number;
  relatedJobId?: string;
  relatedStoryId?: string;
};

const KIND_PRIORITY: Record<DeltaEventKind, number> = {
  walk_in_opening: 52,
  status_moved: 46,
  employer_active_now: 44,
  deadline_closing: 42,
  saved_search_match: 40,
  new_job: 38,
  salary_disclosed: 34,
  trust_upgraded: 32,
  story_went_live: 26,
  suspicious_listing_downgraded: 24,
  digest_ready: 10,
};

function freshnessScore(minutesAgo: number): number {
  return Math.max(0, 90 - minutesAgo) * 0.36;
}

function eventScore(event: DeltaEvent): number {
  return (
    KIND_PRIORITY[event.kind] +
    event.urgencyScore * 0.62 +
    event.trustScore * 0.18 +
    freshnessScore(event.minutesAgo)
  );
}

export function rankDeltaEvents(events: DeltaEvent[]): DeltaEvent[] {
  return [...events].sort((left, right) => eventScore(right) - eventScore(left));
}

export function buildDeltaSummary(events: DeltaEvent[]): {
  newJobs: number;
  statusMoves: number;
  trustShifts: number;
  liveStories: number;
  urgentNow: number;
} {
  const summary = {
    newJobs: 0,
    statusMoves: 0,
    trustShifts: 0,
    liveStories: 0,
    urgentNow: 0,
  };

  for (const event of events) {
    if (event.kind === "new_job") {
      summary.newJobs += 1;
    }

    if (event.kind === "status_moved") {
      summary.statusMoves += 1;
    }

    if (
      event.kind === "salary_disclosed" ||
      event.kind === "trust_upgraded" ||
      event.kind === "suspicious_listing_downgraded"
    ) {
      summary.trustShifts += 1;
    }

    if (event.kind === "story_went_live") {
      summary.liveStories += 1;
    }

    if (event.urgencyScore >= 70) {
      summary.urgentNow += 1;
    }
  }

  return summary;
}
