import { useState } from "react";

import { createDemoState } from "./data/demoData";
import { buildTrustWarnings, getVisibleStories, rankJobs } from "./lib/feed";
import type {
  AlertCard,
  EmployerProfile,
  JobCard,
  SavedSearchCard,
  StoryCard,
  TrustPillar,
} from "./lib/types";

const demo = createDemoState();

const copy = {
  en: {
    pulse: "Colombo Jobs Pulse",
    onboardingTitle: "Check what moved, not just what exists.",
    onboardingBody:
      "Fresh jobs, urgent stories, salary updates, and trust changes sorted for Colombo early-career seekers.",
    onboardingPreview: "Your pulse will open with",
    start: "Open my pulse",
    safeOnly: "Safe feed",
    salaryOnly: "Salary shown",
    changeFeed: "Since your last visit",
    changeBody:
      "New jobs, live employer moves, deadline pressure, and trust shifts ranked by why they matter now.",
    stories: "Urgent stories",
    actNow: "Move now",
    jobs: "Fresh ranked jobs",
    saved: "Saved searches",
    alerts: "Alert queue",
    report: "Report",
    apply: "Apply now",
    save: "Save role",
    detail: "Application pulse",
    why: "Why you are seeing this",
    trust: "Trust check",
    employer: "Employer credibility",
    launchStory: "Post a 24h story",
    candidateStory: "Intro story",
    employerStory: "Employer urgent story",
    hiddenTitle: "Safe mode hid a risky listing",
    hiddenBody:
      "You can still inspect it, but it should not compete with verified roles in the main pulse.",
    profileHint: "Seeker stories stay job-relevant and expire in 24h.",
    employerHint: "Urgent employer stories show deadline, salary, and verification cues up front.",
    reportHint:
      "Reports stay private. High-risk items can be hidden before review finishes.",
    reportTitle: "Report this item",
    empty: "No jobs match these filters right now.",
    reset: "Show everything again",
  },
  si: {
    pulse: "කොළඹ Jobs Pulse",
    onboardingTitle: "දැනට තියෙන දේට වඩා, දැන් මොනවා වෙනස් වුණාද බලන්න.",
    onboardingBody:
      "අලුත් jobs, urgent stories, salary updates, සහ trust changes එක තැනකට ගෙන ආවේ Colombo early-career seekers සඳහා.",
    onboardingPreview: "ඔබේ pulse එක open වෙන්නේ මෙහෙමයි",
    start: "මගේ pulse එක open කරන්න",
    safeOnly: "Safe feed",
    salaryOnly: "Salary shown",
    changeFeed: "අවසන් check එකෙන් පස්සේ",
    changeBody:
      "අලුත් jobs, employer moves, deadlines, සහ trust shifts දැන් වැදගත්කම අනුව rank කරලා.",
    stories: "Urgent stories",
    actNow: "Move now",
    jobs: "Fresh ranked jobs",
    saved: "Saved searches",
    alerts: "Alert queue",
    report: "Report",
    apply: "දැන් apply කරන්න",
    save: "Save role",
    detail: "Application pulse",
    why: "ඔබට මේක පෙන්වන්නේ ඇයි",
    trust: "Trust check",
    employer: "Employer credibility",
    launchStory: "24h story එකක් දාන්න",
    candidateStory: "Intro story",
    employerStory: "Employer urgent story",
    hiddenTitle: "Safe mode එක risky listing එකක් hide කළා",
    hiddenBody:
      "ඔබට ඒක බලන්න පුළුවන්, නමුත් verified roles එක්ක එකම තැන compete කරන්න දෙන්නේ නැහැ.",
    profileHint: "Seeker stories job-relevant වෙලා 24h ඉවරවෙයි.",
    employerHint:
      "Employer urgent stories එකේ deadline, salary, verification cues ඉස්සරහම පේනවා.",
    reportHint:
      "Reports private. High-risk items review ට කලින් hide වෙන්න පුළුවන්.",
    reportTitle: "මෙය report කරන්න",
    empty: "මෙම filters වලට match වෙන jobs නැහැ.",
    reset: "හැම role එකක්ම බලන්න",
  },
} as const;

const reportReasons = [
  "Fake job",
  "Fee or training payment",
  "Suspicious salary claim",
  "Harassment or unsafe contact",
  "Not job-related",
];

type OverlayState =
  | { type: "report"; target: string }
  | { type: "candidate" }
  | { type: "employer" }
  | null;

type UIStrings = (typeof copy)[keyof typeof copy];

function App() {
  const [language, setLanguage] = useState<"en" | "si">("en");
  const [ready, setReady] = useState(false);
  const [verifiedOnly, setVerifiedOnly] = useState(true);
  const [salaryOnly, setSalaryOnly] = useState(false);
  const [selectedRole, setSelectedRole] = useState("Customer Support");
  const [selectedArea, setSelectedArea] = useState(demo.targetAreas[0].id);
  const [selectedJobId, setSelectedJobId] = useState("job-jetwing-support");
  const [overlay, setOverlay] = useState<OverlayState>(null);
  const [candidateTemplate, setCandidateTemplate] = useState(
    demo.candidateTemplates[0],
  );
  const [employerTemplate, setEmployerTemplate] = useState(
    demo.employerTemplates[0],
  );

  const text = copy[language];
  const visibleStories = getVisibleStories(demo.stories, demo.now);
  const filteredJobs = rankJobs(demo.jobs).filter((job) => {
    if (verifiedOnly && job.trustScore < 80) {
      return false;
    }

    if (salaryOnly && !job.salaryDisclosed) {
      return false;
    }

    if (selectedRole !== "All" && job.roleFamily !== selectedRole) {
      return false;
    }

    return true;
  });

  const selectedJob =
    filteredJobs.find((job) => job.id === selectedJobId) ?? filteredJobs[0] ?? demo.jobs[0];
  const selectedEmployer = selectedJob.employerId
    ? demo.employers.find((employer) => employer.id === selectedJob.employerId)
    : undefined;

  const hiddenJobs = demo.jobs.filter((job) => job.trustScore < 80);
  const visibleEvents = demo.deltaEvents.slice(0, 5);
  const onboardingPreviewEvents = demo.deltaEvents.slice(0, 3);

  const openJobFromEvent = (jobId?: string) => {
    if (!jobId) {
      return;
    }

    const job = demo.jobs.find((item) => item.id === jobId);
    if (job && job.trustScore < 80) {
      setVerifiedOnly(false);
    }

    setSelectedJobId(jobId);
  };

  return (
    <main className="app-shell">
      {!ready ? (
        <section className="onboarding-shell">
          <div className="language-row">
            <div className="eyebrow-row">
              <p className="eyebrow">{text.pulse}</p>
              <span className="micro-badge">Colombo-first · mobile-first</span>
            </div>
            <div className="badge-row">
              <button
                className={`language-pill ${language === "en" ? "is-active" : ""}`}
                onClick={() => setLanguage("en")}
                type="button"
              >
                English
              </button>
              <button
                className={`language-pill ${language === "si" ? "is-active" : ""}`}
                onClick={() => setLanguage("si")}
                type="button"
              >
                සිංහල
              </button>
            </div>
          </div>

          <section className="onboarding-card">
            <div className="onboarding-copy">
              <h1>{text.onboardingTitle}</h1>
              <p className="hero-copy">{text.onboardingBody}</p>

              <div className="benefit-row">
                {demo.pulseMetrics.map((metric) => (
                  <article className={`metric-chip tone-${metric.tone}`} key={metric.label}>
                    <strong>{metric.value}</strong>
                    <span>{metric.label}</span>
                  </article>
                ))}
              </div>

              <div className="ritual-stack">
                <article className="ritual-card">
                  <div className="ritual-head">
                    <strong>Role pulse</strong>
                    <span>Choose what should lead</span>
                  </div>
                  <div className="chip-row">
                    {demo.roleFamilies.map((role) => (
                      <button
                        key={role}
                        className={`choice-chip ${selectedRole === role ? "is-selected" : ""}`}
                        onClick={() => setSelectedRole(role)}
                        type="button"
                      >
                        {role}
                      </button>
                    ))}
                  </div>
                </article>

                <article className="ritual-card">
                  <div className="ritual-head">
                    <strong>Target area</strong>
                    <span>Commute-aware from the first session</span>
                  </div>
                  <div className="area-grid">
                    {demo.targetAreas.map((area) => (
                      <button
                        key={area.id}
                        className={`area-card ${selectedArea === area.id ? "is-selected" : ""}`}
                        onClick={() => setSelectedArea(area.id)}
                        type="button"
                      >
                        <strong>{area.title}</strong>
                        <span>{area.note}</span>
                      </button>
                    ))}
                  </div>
                </article>
              </div>
            </div>

            <div className="preview-shell">
              <div className="preview-header">
                <div>
                  <p className="eyebrow">Tonight’s pulse</p>
                  <h2>{text.onboardingPreview}</h2>
                </div>
                <span className="preview-check">Safe feed on</span>
              </div>

              <div className="preview-panel">
                <div className="preview-summary">
                  <strong>{selectedRole}</strong>
                  <span>
                    {
                      demo.targetAreas.find((area) => area.id === selectedArea)?.title
                    }{" "}
                    · {demo.lastVisitLabel}
                  </span>
                </div>

                <div className="preview-queue">
                  {onboardingPreviewEvents.map((event) => (
                    <article className="preview-event" key={event.id}>
                      <div>
                        <strong>{event.title}</strong>
                        <p>{event.detail}</p>
                      </div>
                      <span>{event.timeLabel}</span>
                    </article>
                  ))}
                </div>

                <article className="preview-story-card">
                  <div className="story-card-topline">
                    <span className="story-chip">Walk-in now</span>
                    <span className="story-countdown">13h left</span>
                  </div>
                  <strong>Jetwing walk-in story</strong>
                  <p>Verified employer. Salary shown. Venue proof matched.</p>
                </article>

                <div className="trust-preview">
                  <span className="trust-badge tone-verified">Trust moves with the feed</span>
                  <p>
                    Salary changes, risk downgrades, and proof upgrades show up in the same
                    pulse as new jobs.
                  </p>
                </div>
              </div>

              <div className="onboarding-footer">
                <div>
                  <strong>Open with useful movement already visible</strong>
                  <p>Freshness first. Salary first where possible. Risk pushed down.</p>
                </div>
                <button className="primary-cta" onClick={() => setReady(true)} type="button">
                  {text.start}
                </button>
              </div>
            </div>
          </section>
        </section>
      ) : (
        <>
          <header className="command-surface">
            <div className="command-copy-wrap">
              <div className="eyebrow-row">
                <p className="eyebrow">{text.pulse}</p>
                <span className="micro-badge">{demo.lastVisitLabel}</span>
              </div>
              <h2 className="section-title">{text.changeFeed}</h2>
              <p className="command-copy">{text.changeBody}</p>
            </div>

            <div className="command-actions">
              <button
                className={`toggle-chip ${verifiedOnly ? "is-on" : ""}`}
                onClick={() => setVerifiedOnly((value) => !value)}
                type="button"
              >
                {text.safeOnly}
              </button>
              <button
                className={`toggle-chip ${salaryOnly ? "is-on" : ""}`}
                onClick={() => setSalaryOnly((value) => !value)}
                type="button"
              >
                {text.salaryOnly}
              </button>
              <button
                className="ghost-button"
                onClick={() => setOverlay({ type: "candidate" })}
                type="button"
              >
                {text.candidateStory}
              </button>
              <button
                className="ghost-button"
                onClick={() => setOverlay({ type: "employer" })}
                type="button"
              >
                {text.employerStory}
              </button>
            </div>
          </header>

          <section className="delta-stage">
            <div className="summary-strip">
              {demo.pulseMetrics.map((metric) => (
                <article className={`summary-card tone-${metric.tone}`} key={metric.label}>
                  <div className="summary-head">
                    <strong>{metric.value}</strong>
                    <span>{metric.label}</span>
                  </div>
                  <p>{metric.note}</p>
                </article>
              ))}
            </div>

            <section className="delta-ribbon">
              <div className="section-heading">
                <h3>{text.actNow}</h3>
                <span>{visibleEvents.length} live changes</span>
              </div>
              <div className="delta-scroll">
                {visibleEvents.map((event) => (
                  <article className={`delta-card kind-${event.kind}`} key={event.id}>
                    <div className="delta-meta">
                      <span className="delta-time">{event.timeLabel}</span>
                      <span className="trust-badge tone-hot">
                        {event.kind.replaceAll("_", " ")}
                      </span>
                    </div>
                    <strong>{event.title}</strong>
                    <p>{event.detail}</p>
                    <button
                      className="ghost-button"
                      onClick={() => openJobFromEvent(event.relatedJobId)}
                      type="button"
                    >
                      {event.ctaLabel ?? "Open"}
                    </button>
                  </article>
                ))}
              </div>
            </section>
          </section>

          <section className="dashboard-grid">
            <aside className="left-rail">
              <section className="rail-card safe-mode-card">
                <div className="section-heading">
                  <h3>{text.hiddenTitle}</h3>
                  <span>{hiddenJobs.length} hidden</span>
                </div>
                <p>{text.hiddenBody}</p>
                <button
                  className="ghost-button"
                  onClick={() => {
                    setVerifiedOnly(false);
                    setSelectedJobId(hiddenJobs[0].id);
                  }}
                  type="button"
                >
                  Review hidden listing
                </button>
              </section>

              <section className="rail-card">
                <div className="section-heading">
                  <h3>{text.saved}</h3>
                  <span>{demo.savedSearches.length} live</span>
                </div>
                <div className="rail-stack">
                  {demo.savedSearches.map((search) => (
                    <SavedSearchTile key={search.id} search={search} />
                  ))}
                </div>
              </section>

              <section className="rail-card">
                <div className="section-heading">
                  <h3>{text.alerts}</h3>
                  <span>personal</span>
                </div>
                <div className="rail-stack">
                  {demo.alerts.map((alert) => (
                    <AlertTile
                      alert={alert}
                      key={alert.id}
                      onOpen={() => openJobFromEvent(alert.relatedJobId)}
                    />
                  ))}
                </div>
              </section>
            </aside>

            <section className="main-column">
              <section className="panel-section story-section">
                <div className="section-heading">
                  <div>
                    <h3>{text.stories}</h3>
                    <p className="section-subcopy">
                      Stories exist for urgency, salary movement, walk-ins, and candidate proof.
                    </p>
                  </div>
                  <span>{visibleStories.length} live</span>
                </div>

                <div className="story-reel">
                  {visibleStories.map((story) => (
                    <StoryTile
                      key={story.id}
                      onOpen={() => {
                        if (story.linkedJobId) {
                          setSelectedJobId(story.linkedJobId);
                        }
                      }}
                      onReport={() => setOverlay({ type: "report", target: story.title })}
                      story={story}
                    />
                  ))}
                </div>
              </section>

              <section className="panel-section jobs-section">
                <div className="section-heading">
                  <div>
                    <h3>{text.jobs}</h3>
                    <p className="section-subcopy">
                      Ranked by freshness, trust, salary clarity, and whether something moved.
                    </p>
                  </div>
                  <span>{filteredJobs.length} visible</span>
                </div>

                <div className="role-strip">
                  {demo.roleFamilies.map((role) => (
                    <button
                      key={role}
                      className={`role-chip ${selectedRole === role ? "is-selected" : ""}`}
                      onClick={() => setSelectedRole(role)}
                      type="button"
                    >
                      {role}
                    </button>
                  ))}
                </div>

                {filteredJobs.length === 0 ? (
                  <div className="empty-card">
                    <h4>{text.empty}</h4>
                    <p>Try turning off salary-only or widening the safe feed for inspection.</p>
                    <button
                      className="ghost-button"
                      onClick={() => {
                        setVerifiedOnly(false);
                        setSalaryOnly(false);
                      }}
                      type="button"
                    >
                      {text.reset}
                    </button>
                  </div>
                ) : (
                  <div className="job-list">
                    {filteredJobs.map((job) => (
                      <JobTile
                        isSelected={selectedJob.id === job.id}
                        job={job}
                        key={job.id}
                        onOpen={() => setSelectedJobId(job.id)}
                        onReport={() => setOverlay({ type: "report", target: job.title })}
                      />
                    ))}
                  </div>
                )}
              </section>
            </section>

            <aside className="right-rail">
              <JobDetailSurface
                employer={selectedEmployer}
                job={selectedJob}
                onReport={() => setOverlay({ type: "report", target: selectedJob.title })}
                text={text}
                trustPillars={demo.trustPillars}
              />

              <section className="rail-card composer-launch-card">
                <div className="section-heading">
                  <h3>{text.launchStory}</h3>
                  <span>24h only</span>
                </div>
                <p>{text.profileHint}</p>
                <div className="launch-grid">
                  <button
                    className="launch-button"
                    onClick={() => setOverlay({ type: "candidate" })}
                    type="button"
                  >
                    <strong>{text.candidateStory}</strong>
                    <span>Template-led and tagged to roles</span>
                  </button>
                  <button
                    className="launch-button"
                    onClick={() => setOverlay({ type: "employer" })}
                    type="button"
                  >
                    <strong>{text.employerStory}</strong>
                    <span>Deadline, salary, and verification shown first</span>
                  </button>
                </div>
              </section>
            </aside>
          </section>
        </>
      )}

      {overlay ? (
        <div className="modal-layer">
          <div className="modal-card">
            {overlay.type === "report" ? (
              <>
                <div className="section-heading">
                  <div>
                    <h3>{text.reportTitle}</h3>
                    <p className="section-subcopy">{overlay.target}</p>
                  </div>
                  <button className="ghost-button" onClick={() => setOverlay(null)} type="button">
                    Close
                  </button>
                </div>
                <div className="report-grid">
                  {reportReasons.map((reason) => (
                    <button className="report-reason" key={reason} type="button">
                      {reason}
                    </button>
                  ))}
                </div>
                <p className="modal-footnote">{text.reportHint}</p>
              </>
            ) : overlay.type === "candidate" ? (
              <>
                <div className="section-heading">
                  <div>
                    <h3>{text.candidateStory}</h3>
                    <p className="section-subcopy">{text.profileHint}</p>
                  </div>
                  <button className="ghost-button" onClick={() => setOverlay(null)} type="button">
                    Close
                  </button>
                </div>
                <div className="template-grid">
                  {demo.candidateTemplates.map((template) => (
                    <button
                      key={template}
                      className={`choice-chip ${candidateTemplate === template ? "is-selected" : ""}`}
                      onClick={() => setCandidateTemplate(template)}
                      type="button"
                    >
                      {template}
                    </button>
                  ))}
                </div>
                <article className="composer-preview candidate-story-preview">
                  <span className="story-chip">3 reasons to hire me</span>
                  <h4>{candidateTemplate}</h4>
                  <p>
                    English + Sinhala speaker, ready for walk-ins this week, and tagged to
                    support roles within a Colombo commute.
                  </p>
                </article>
                <div className="composer-checklist">
                  <span className="trust-badge tone-verified">Role-tagged</span>
                  <span className="trust-badge tone-cool">Expires in 24h</span>
                  <span className="trust-badge tone-watch">Reportable by employers</span>
                </div>
              </>
            ) : (
              <>
                <div className="section-heading">
                  <div>
                    <h3>{text.employerStory}</h3>
                    <p className="section-subcopy">{text.employerHint}</p>
                  </div>
                  <button className="ghost-button" onClick={() => setOverlay(null)} type="button">
                    Close
                  </button>
                </div>
                <div className="template-grid">
                  {demo.employerTemplates.map((template) => (
                    <button
                      key={template}
                      className={`choice-chip ${employerTemplate === template ? "is-selected" : ""}`}
                      onClick={() => setEmployerTemplate(template)}
                      type="button"
                    >
                      {template}
                    </button>
                  ))}
                </div>
                <article className="composer-preview employer-story-preview">
                  <span className="story-chip">Verified employer story</span>
                  <h4>{employerTemplate}</h4>
                  <p>
                    20 trainee seats, Colombo 03 venue proof, salary visible, and deadline
                    shown before posting.
                  </p>
                </article>
                <div className="composer-checklist">
                  <span className="trust-badge tone-verified">Verification required</span>
                  <span className="trust-badge tone-hot">Deadline first</span>
                  <span className="trust-badge tone-cool">Salary cue included</span>
                </div>
              </>
            )}
          </div>
        </div>
      ) : null}
    </main>
  );
}

export default App;

function StoryTile({
  story,
  onOpen,
  onReport,
}: {
  story: StoryCard;
  onOpen: () => void;
  onReport: () => void;
}) {
  return (
    <article
      className={`story-card-v2 accent-${story.accent} ${story.seen ? "is-seen" : "is-fresh"}`}
    >
      <div className="story-card-topline">
        <span className="story-author-ring">{story.authorName.slice(0, 2).toUpperCase()}</span>
        <div className="story-author-meta">
          <strong>{story.authorName}</strong>
          <span>{story.authorMeta}</span>
        </div>
        <span className="story-countdown">{story.expiresInLabel}</span>
      </div>

      <div className="story-media-label">{story.mediaLabel}</div>

      <div className="story-card-body">
        <span className="story-chip">{story.templateLabel}</span>
        <h4>{story.title}</h4>
        <p>{story.body}</p>
      </div>

      <div className="story-card-footer">
        <span className="trust-badge tone-verified">{story.trustLabel}</span>
        <span className="micro-badge">{story.priorityNote}</span>
      </div>

      <div className="story-actions">
        <button className="primary-inline" onClick={onOpen} type="button">
          {story.actionLabel ?? "Open"}
        </button>
        <button className="ghost-button" onClick={onReport} type="button">
          Report
        </button>
      </div>
    </article>
  );
}

function JobTile({
  job,
  isSelected,
  onOpen,
  onReport,
}: {
  job: JobCard;
  isSelected: boolean;
  onOpen: () => void;
  onReport: () => void;
}) {
  return (
    <article className={`job-card-v2 ${isSelected ? "is-selected" : ""} tone-${job.trustTone ?? "verified"}`}>
      <div className="job-topline">
        <div>
          <div className="job-overline">
            <span className={`trust-badge tone-${job.trustTone ?? "verified"}`}>{job.trustLabel}</span>
            <span className="micro-badge">{job.sourceLabel}</span>
          </div>
          <h4>{job.title}</h4>
          <p className="job-subtitle">
            {job.employerName} · {job.locationLabel}
          </p>
        </div>
        <span className="freshness-pill">{job.freshnessLabel}</span>
      </div>

      <div className="delta-badge-row">
        {job.deltaBadges?.map((badge) => (
          <span className="job-badge" key={badge}>
            {badge}
          </span>
        ))}
      </div>

      <div className="job-meta-grid">
        <span className="meta-pill salary-pill">{job.salaryLabel}</span>
        <span className="meta-pill">{job.applyModeLabel}</span>
        <span className="meta-pill">{job.responseLabel}</span>
      </div>

      <p className="job-summary">{job.summary}</p>

      <div className="why-now-list">
        {job.whyNow?.map((reason) => (
          <div className="why-now-item" key={reason}>
            {reason}
          </div>
        ))}
      </div>

      {job.suspiciousFlags.length > 0 ? (
        <div className="warning-stack">
          {job.suspiciousFlags.map((warning) => (
            <div className="warning-card" key={warning}>
              {warning}
            </div>
          ))}
        </div>
      ) : null}

      <div className="job-actions">
        <button className="primary-inline" onClick={onOpen} type="button">
          Open pulse
        </button>
        <button className="ghost-button" onClick={onReport} type="button">
          Report
        </button>
      </div>
    </article>
  );
}

function SavedSearchTile({ search }: { search: SavedSearchCard }) {
  return (
    <article className="search-card">
      <div className="section-heading">
        <strong>{search.title}</strong>
        <span className="micro-badge">{search.alertMode}</span>
      </div>
      <p>{search.summary}</p>
      <div className="search-stats">
        <span>{search.matchCount} matches</span>
        <span>{search.urgentCount} urgent</span>
      </div>
      <div className="search-foot">
        <strong>{search.freshnessLabel}</strong>
        <span>{search.nextPulse}</span>
      </div>
    </article>
  );
}

function AlertTile({
  alert,
  onOpen,
}: {
  alert: AlertCard;
  onOpen: () => void;
}) {
  return (
    <article className={`alert-card mode-${alert.mode}`}>
      <div className="section-heading">
        <span
          className={`trust-badge tone-${alert.mode === "act_now" ? "hot" : alert.mode === "review" ? "watch" : "cool"}`}
        >
          {alert.reason}
        </span>
        <span className="micro-badge">{alert.timeLabel}</span>
      </div>
      <strong>{alert.title}</strong>
      <p>{alert.body}</p>
      <button className="ghost-button" onClick={onOpen} type="button">
        Open
      </button>
    </article>
  );
}

function JobDetailSurface({
  job,
  employer,
  onReport,
  text,
  trustPillars,
}: {
  job: JobCard;
  employer?: EmployerProfile;
  onReport: () => void;
  text: UIStrings;
  trustPillars: TrustPillar[];
}) {
  return (
    <>
      <section className="detail-card-v2">
        <div className="detail-topline">
          <span className={`trust-badge tone-${job.trustTone ?? "verified"}`}>{job.trustLabel}</span>
          <button className="ghost-button" onClick={onReport} type="button">
            {text.report}
          </button>
        </div>

        <h3>{job.title}</h3>
        <p className="detail-subtitle">
          {job.employerName} · {job.locationLabel}
        </p>

        <div className="detail-cta-row">
          <button className="primary-inline" type="button">
            {text.apply}
          </button>
          <button className="ghost-button" type="button">
            {text.save}
          </button>
        </div>

        <div className="detail-chip-row">
          <span className="detail-chip">{job.salaryLabel}</span>
          <span className="detail-chip">{job.deadlineLabel}</span>
          <span className="detail-chip">{job.lastVerifiedLabel}</span>
        </div>

        <section className="detail-section">
          <div className="section-heading">
            <h4>{text.why}</h4>
            <span className="micro-badge">{job.rankingReason}</span>
          </div>
          <div className="detail-list">
            {job.whyNow?.map((reason) => (
              <div className="detail-list-item" key={reason}>
                {reason}
              </div>
            ))}
          </div>
        </section>

        <section className="detail-section">
          <div className="section-heading">
            <h4>{text.trust}</h4>
            <span className="micro-badge">{job.sourceLabel}</span>
          </div>
          <div className="detail-list">
            {buildTrustWarnings(job)
              .concat(job.trustSignals ?? [])
              .map((warning) => (
                <div className="detail-list-item" key={warning}>
                  {warning}
                </div>
              ))}
          </div>
        </section>

        <section className="detail-section">
          <div className="section-heading">
            <h4>{text.detail}</h4>
            <span className="micro-badge">{job.employerActiveLabel}</span>
          </div>
          <div className="status-rail">
            {job.statusTimeline.map((step) => (
              <div className="status-item" key={step.label}>
                <span className={`status-dot status-${step.tone}`} />
                <div>
                  <strong>{step.label}</strong>
                  <p>{step.time}</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        {job.screeningPreview && job.screeningPreview.length > 0 ? (
          <section className="detail-section">
            <div className="section-heading">
              <h4>Screening preview</h4>
              <span className="micro-badge">{job.applyModeLabel}</span>
            </div>
            <div className="detail-list">
              {job.screeningPreview.map((question) => (
                <div className="detail-list-item" key={question}>
                  {question}
                </div>
              ))}
            </div>
          </section>
        ) : null}
      </section>

      {employer ? (
        <section className="rail-card">
          <div className="section-heading">
            <h3>{text.employer}</h3>
            <span className="micro-badge">{employer.verificationLabel}</span>
          </div>
          <strong>{employer.companyName}</strong>
          <p>{employer.headline}</p>
          <div className="delta-badge-row">
            {employer.badges.map((badge) => (
              <span className="job-badge" key={badge}>
                {badge}
              </span>
            ))}
          </div>
          <div className="detail-list">
            <div className="detail-list-item">{employer.responseLabel}</div>
            <div className="detail-list-item">{employer.activeLabel}</div>
            <div className="detail-list-item">{employer.salaryDisciplineLabel}</div>
            <div className="detail-list-item">{employer.officeProofLabel}</div>
          </div>
        </section>
      ) : null}

      <section className="rail-card">
        <div className="section-heading">
          <h3>Trust infrastructure</h3>
          <span className="micro-badge">Visible, not hidden</span>
        </div>
        <div className="rail-stack">
          {trustPillars.map((pillar) => (
            <article className="trust-note" key={pillar.title}>
              <strong>{pillar.title}</strong>
              <p>{pillar.body}</p>
            </article>
          ))}
        </div>
      </section>
    </>
  );
}
