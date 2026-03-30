import { describe, expect, it } from "vitest";

import { getVisibleStories, rankJobs } from "./feed";
import type { JobCard, StoryCard } from "./types";

function makeJobCard(overrides: Partial<JobCard>): JobCard {
  return {
    id: "job-default",
    title: "Default job",
    employerName: "Default employer",
    roleFamily: "Customer Support",
    locationLabel: "Colombo",
    freshnessMinutes: 60,
    freshnessLabel: "1h ago",
    trustScore: 80,
    trustLabel: "Verified employer",
    applyEase: 80,
    applyModeLabel: "Quick apply",
    salaryLabel: "LKR 80k - 100k",
    salaryDisclosed: true,
    badges: [],
    summary: "Default summary",
    suspiciousFlags: [],
    lastVerifiedLabel: "30m ago",
    statusTimeline: [],
    ...overrides,
  };
}

function makeStoryCard(overrides: Partial<StoryCard>): StoryCard {
  return {
    id: "story-default",
    title: "Default story",
    body: "Default story body",
    authorName: "Default author",
    templateLabel: "Urgent hiring",
    expiresAt: "2026-03-17T01:00:00.000Z",
    expiresInLabel: "Ends in 4h",
    trustScore: 80,
    accent: "flame",
    ...overrides,
  };
}

describe("rankJobs", () => {
  it("prioritizes fresher and more trusted jobs", () => {
    const jobs: JobCard[] = [
      makeJobCard({
        id: "job-stale",
        title: "Customer Support Executive",
        freshnessMinutes: 240,
        trustScore: 68,
        applyEase: 80,
      }),
      makeJobCard({
        id: "job-fast",
        title: "Junior Growth Associate",
        freshnessMinutes: 18,
        trustScore: 92,
        applyEase: 84,
      }),
    ];

    const ranked = rankJobs(jobs);

    expect(ranked[0].id).toBe("job-fast");
  });
});

describe("getVisibleStories", () => {
  it("hides stories from the user exactly when they expire", () => {
    const stories: StoryCard[] = [
      makeStoryCard({
        id: "story-live",
        expiresAt: "2026-03-17T02:30:00.000Z",
        trustScore: 95,
      }),
      makeStoryCard({
        id: "story-expired",
        expiresAt: "2026-03-16T20:00:00.000Z",
        trustScore: 88,
      }),
    ];

    const visible = getVisibleStories(stories, new Date("2026-03-16T21:00:00.000Z"));

    expect(visible.map((story) => story.id)).toEqual(["story-live"]);
    expect(stories).toHaveLength(2);
  });
});
