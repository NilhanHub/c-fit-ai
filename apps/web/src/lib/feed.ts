import type { JobCard, StoryCard } from "./types";

function scoreJob(job: JobCard): number {
  const freshnessScore = Math.max(0, 360 - job.freshnessMinutes) * 0.28;
  const trustScore = job.trustScore * 0.52;
  const applyScore = job.applyEase * 0.2;
  const salaryBonus = job.salaryDisclosed ? 8 : 0;
  const deltaBonus = (job.deltaBadges?.length ?? 0) * 3;
  const warningPenalty = (job.suspiciousFlags?.length ?? 0) * 10;

  return (
    freshnessScore + trustScore + applyScore + salaryBonus + deltaBonus - warningPenalty
  );
}

export function rankJobs(jobs: JobCard[]): JobCard[] {
  return [...jobs].sort((left, right) => scoreJob(right) - scoreJob(left));
}

export function getVisibleStories(
  stories: StoryCard[],
  now: Date,
): StoryCard[] {
  return [...stories]
    .filter((story) => new Date(story.expiresAt).getTime() > now.getTime())
    .sort((left, right) => {
      const leftCountdown =
        left.countdownMinutes ?? new Date(left.expiresAt).getTime() - now.getTime();
      const rightCountdown =
        right.countdownMinutes ?? new Date(right.expiresAt).getTime() - now.getTime();
      return leftCountdown - rightCountdown || right.trustScore - left.trustScore;
    });
}

export function buildTrustWarnings(job: JobCard): string[] {
  const warnings = [...job.suspiciousFlags];

  if (job.trustScore >= 90) {
    warnings.unshift("Verified employer with strong response history.");
  } else if (job.trustScore >= 80) {
    warnings.unshift(
      "Verified employer. Review the salary and shift details before applying.",
    );
  } else {
    warnings.unshift(
      "Risk raised. Confirm the employer identity before leaving the app.",
    );
  }

  return warnings;
}
