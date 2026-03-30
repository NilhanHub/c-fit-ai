export type StatusStep = {
  label: string;
  time: string;
  tone: "done" | "active" | "idle";
};

export type TrustTone = "verified" | "watch" | "risky";

export type StoryAccent = "flame" | "lagoon" | "midnight" | "sunrise";

export type StoryKind =
  | "employer_urgent"
  | "candidate_intro"
  | "campus_burst"
  | "walk_in"
  | "salary_drop";

export type AlertMode = "act_now" | "review" | "digest";

export type JobCard = {
  id: string;
  title: string;
  employerId?: string;
  employerName: string;
  roleFamily: string;
  locationLabel: string;
  commuteLabel?: string;
  freshnessMinutes: number;
  freshnessLabel: string;
  trustScore: number;
  trustLabel: string;
  trustTone?: TrustTone;
  applyEase: number;
  applyModeLabel: string;
  salaryLabel: string;
  salaryDisclosed: boolean;
  badges: string[];
  deltaBadges?: string[];
  whyNow?: string[];
  rankingReason?: string;
  summary: string;
  suspiciousFlags: string[];
  sourceLabel?: string;
  lastVerifiedLabel: string;
  deadlineLabel?: string;
  employerActiveLabel?: string;
  responseLabel?: string;
  salaryNote?: string;
  trustSignals?: string[];
  proofPoints?: string[];
  screeningPreview?: string[];
  linkedStoryIds?: string[];
  statusTimeline: StatusStep[];
};

export type StoryCard = {
  id: string;
  kind?: StoryKind;
  title: string;
  body: string;
  authorName: string;
  authorMeta?: string;
  templateLabel: string;
  expiresAt: string;
  expiresInLabel: string;
  countdownMinutes?: number;
  trustScore: number;
  trustLabel?: string;
  accent: StoryAccent;
  actionLabel?: string;
  actionHint?: string;
  mediaLabel?: string;
  seen?: boolean;
  linkedJobId?: string;
  priorityNote?: string;
};

export type MiniCard = {
  id: string;
  name?: string;
  title: string;
  summary?: string;
  body?: string;
};

export type TrustPillar = {
  title: string;
  body: string;
};

export type SavedSearchCard = {
  id: string;
  title: string;
  summary: string;
  matchCount: number;
  urgentCount: number;
  freshnessLabel: string;
  nextPulse: string;
  alertMode: string;
};

export type AlertCard = {
  id: string;
  title: string;
  body: string;
  mode: AlertMode;
  timeLabel: string;
  reason: string;
  relatedJobId?: string;
};

export type EmployerProfile = {
  id: string;
  companyName: string;
  headline: string;
  verificationLabel: string;
  responseLabel: string;
  activeLabel: string;
  salaryDisciplineLabel: string;
  officeProofLabel: string;
  badges: string[];
  trustFacts: string[];
};

export type PulseMetric = {
  label: string;
  value: string;
  tone: "hot" | "cool" | "watch";
  note: string;
};
