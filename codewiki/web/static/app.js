"use strict";

const LOCALE_STORAGE_KEY = "codewiki.locale";
const SUPPORTED_LOCALES = new Set(["en", "ko"]);
const KO_MESSAGES = Object.freeze({
  "Explore CodeWiki Specs and their implementation traceability.": "CodeWiki 스펙과 구현 추적 관계를 살펴보세요.",
  "CodeWiki · Spec Traceability": "CodeWiki · 스펙 추적성",
  "Skip to content": "본문으로 건너뛰기",
  "CodeWiki Overview": "CodeWiki 개요",
  "Specs to code": "스펙에서 코드까지",
  "Primary navigation": "기본 탐색",
  "Overview": "개요",
  "Explorer": "탐색기",
  "Changes": "변경 사항",
  "Search requirements, acceptance criteria, and Specs": "요구사항, 인수 기준 및 스펙 검색",
  "Search requirements, Specs, or code": "요구사항, 스펙 또는 코드 검색",
  "Search": "검색",
  "Open CodeWiki status": "CodeWiki 상태 열기",
  "Loading status": "상태 불러오는 중",
  "Language": "언어",
  "Loading CodeWiki": "CodeWiki 불러오는 중",
  "Loading the Spec map…": "스펙 맵을 불러오는 중…",
  "The CodeWiki Web Viewer requires JavaScript. The CLI remains fully available.": "CodeWiki 웹 뷰어에는 JavaScript가 필요합니다. CLI는 계속 사용할 수 있습니다.",
  "English": "영어",
  "Korean": "한국어",
  "Current language: {language}.": "현재 표시 언어: {language}.",
  "The viewer received an invalid server response.": "뷰어가 올바르지 않은 서버 응답을 받았습니다.",
  "Request failed ({status}).": "요청에 실패했습니다({status}).",
  "Synchronized": "동기화됨",
  "Potentially stale": "최신 상태가 아닐 수 있음",
  "Working tree changed": "작업 트리 변경됨",
  "Freshness unknown": "최신 여부 알 수 없음",
  "Unknown": "알 수 없음",
  "{status}. Open Changes.": "{status}. 변경 사항 열기.",
  "Loading…": "불러오는 중…",
  "An unexpected viewer error occurred.": "예상하지 못한 뷰어 오류가 발생했습니다.",
  "Request failed": "요청 실패",
  "CodeWiki could not load this view": "CodeWiki가 이 화면을 불러오지 못했습니다",
  "Return to Overview": "개요로 돌아가기",
  "Project memory": "프로젝트 메모리",
  "Domain Spec": "도메인 스펙",
  "Policy Spec": "정책 스펙",
  "Spec": "스펙",
  "Acceptance Criterion": "인수 기준",
  "Requirement": "요구사항",
  "Unavailable": "사용할 수 없음",
  "Spec-first workspace": "스펙 중심 워크스페이스",
  "See what should happen—and where it happens.": "무엇이 일어나야 하고, 어디에서 구현되는지 확인하세요.",
  "Start with a Spec. Move through requirements, acceptance criteria, and the exact implementation without losing context.": "스펙에서 시작해 요구사항, 인수 기준, 정확한 구현으로 이어지는 맥락을 한눈에 확인하세요.",
  "Explore requirements": "요구사항 살펴보기",
  "Review changes": "변경 사항 검토하기",
  "CodeWiki exploration flow": "CodeWiki 탐색 흐름",
  "Approved intent": "승인된 의도",
  "Expected behavior": "기대 동작",
  "Acceptance": "인수 기준",
  "Observable proof": "확인 가능한 증거",
  "Code": "코드",
  "Current implementation": "현재 구현",
  "CodeWiki summary": "CodeWiki 요약",
  "Spec documents": "스펙 문서",
  "Project, domain, and policy Specs": "프로젝트, 도메인 및 정책 스펙",
  "Requirements": "요구사항",
  "Normative behavior statements": "규범적 동작 명세",
  "Acceptance Criteria": "인수 기준",
  "Observable verification outcomes": "확인 가능한 검증 결과",
  "Traceability": "추적성",
  "{traced} of {total} entities linked": "엔터티 {total}개 중 {traced}개 연결됨",
  "Current CodeWiki state": "현재 CodeWiki 상태",
  "Freshness cannot be established from the available Git and coverage data. CodeWiki does not guess.": "사용 가능한 Git 및 커버리지 데이터로 최신 여부를 확인할 수 없습니다. CodeWiki는 추측하지 않습니다.",
  "Synchronization is derived from reference/coverage.json and the current Git state.": "동기화 상태는 reference/coverage.json과 현재 Git 상태를 기준으로 계산됩니다.",
  "Validation": "검증",
  "Valid": "유효함",
  "{count} failed": "{count}개 실패",
  "Indexed revision": "인덱싱된 리비전",
  "Current revision": "현재 리비전",
  "See change impact": "변경 영향 보기",
  "Traceability gaps": "추적성 공백",
  "Unlinked Requirements and Criteria": "연결되지 않은 요구사항과 인수 기준",
  "{count} unlinked": "{count}개 연결 안 됨",
  "Complete": "완료",
  "No recorded implementation": "기록된 구현 없음",
  "Every parsed entity has a recorded feature trace.": "파싱된 모든 엔터티에 기능 추적 정보가 기록되어 있습니다.",
  " Open any Spec to inspect its exact evidence.": " 스펙을 열어 정확한 근거를 확인하세요.",
  "Functional structure": "기능 구조",
  "Specs": "스펙",
  "Select a Spec to continue in Explorer.": "탐색기에서 계속하려면 스펙을 선택하세요.",
  "No Specs found": "스펙을 찾지 못했습니다",
  "The Wiki has no managed Spec documents yet.": "Wiki에 아직 관리되는 스펙 문서가 없습니다.",
  "{traced}/{total} linked": "{traced}/{total} 연결됨",
  "No summary is recorded for this Spec.": "이 스펙에 기록된 요약이 없습니다.",
  "Criteria": "인수 기준",
  "{title} trace coverage": "{title} 추적 범위",
  "Explore Spec": "스펙 살펴보기",
  "Implementation traceability": "구현 추적성",
  "Implementation Traceability": "구현 추적성",
  "Select a Requirement or Acceptance Criterion": "요구사항 또는 인수 기준을 선택하세요",
  "Choose a Spec entity": "스펙 엔터티 선택",
  "Traceability is shown locally for the selected Requirement or Acceptance Criterion.": "선택한 요구사항 또는 인수 기준의 로컬 추적 관계를 표시합니다.",
  "Spec Explorer": "스펙 탐색기",
  "Spec Index": "스펙 색인",
  "Navigate by behavior, not files": "파일이 아닌 동작을 기준으로 탐색하세요",
  "Specs and requirements": "스펙과 요구사항",
  "Spec overview": "스펙 개요",
  "Implementation trace recorded": "구현 추적 정보 있음",
  "No implementation trace": "구현 추적 정보 없음",
  "traced": "추적됨",
  "untraced": "추적되지 않음",
  "Spec View": "스펙 보기",
  "Structured Spec information": "구조화된 스펙 정보",
  "Spec not found": "스펙을 찾지 못했습니다",
  "Choose a Spec from the index.": "색인에서 스펙을 선택하세요.",
  "{title} Spec overview": "{title} 스펙 개요",
  "No summary is recorded.": "기록된 요약이 없습니다.",
  "No Requirements are parsed from this Spec.": "이 스펙에서 파싱된 요구사항이 없습니다.",
  "No Acceptance Criteria are parsed from this Spec.": "이 스펙에서 파싱된 인수 기준이 없습니다.",
  "Open in Explorer →": "탐색기에서 열기 →",
  "{id} Spec detail": "{id} 스펙 상세",
  "Spec location": "스펙 위치",
  "Normative requirement": "규범적 요구사항",
  "Observable outcome": "확인 가능한 결과",
  "No body is recorded.": "기록된 본문이 없습니다.",
  "Observable outcomes related by the Core parser": "Core 파서가 연결한 확인 가능한 결과",
  "Related Requirements": "관련 요구사항",
  "Requirements in the owning Spec": "소유 스펙의 요구사항",
  "Owning Spec": "소유 스펙",
  "{count} feature link": "기능 링크 {count}개",
  "{count} feature links": "기능 링크 {count}개",
  "{count} code reference": "코드 참조 {count}개",
  "{count} code references": "코드 참조 {count}개",
  "{features} · {references}": "{features} · {references}",
  "Implementation": "구현",
  "Recorded feature traces": "기록된 기능 추적 정보",
  "Direct": "직접",
  "Via requirement": "요구사항 경유",
  "Spec Basis: {ids}": "스펙 근거: {ids}",
  "No Spec Basis is recorded.": "기록된 스펙 근거가 없습니다.",
  "No feature in CodeWiki currently links this entity to implementation.": "현재 CodeWiki에서 이 엔터티를 구현에 연결하는 기능이 없습니다.",
  "Code references": "코드 참조",
  "Related tests": "관련 테스트",
  "Actual code": "실제 코드",
  "Bounded source excerpts from Core": "Core가 제공한 범위 제한 소스 발췌",
  "No readable source excerpt is available for the recorded references.": "기록된 참조에서 읽을 수 있는 소스 발췌를 찾지 못했습니다.",
  "Selected entity only": "선택한 엔터티만",
  "Local Trace Map": "로컬 추적 맵",
  "Local": "로컬",
  "Requirement to actual code flow": "요구사항에서 실제 코드까지의 흐름",
  "Actual Code": "실제 코드",
  "Showing {shown} local code nodes of {total}.": "로컬 코드 노드 {total}개 중 {shown}개를 표시합니다.",
  "No recorded link": "기록된 연결 없음",
  "Verification surfaces recorded in coverage": "커버리지에 기록된 검증 지점",
  "Files, symbols, routes, and models": "파일, 심볼, 라우트 및 모델",
  "file": "파일",
  "symbol": "심볼",
  "route": "라우트",
  "model": "모델",
  "Missing": "누락",
  "Exists": "존재함",
  "Recorded": "기록됨",
  "Source excerpt": "소스 발췌",
  "Source excerpt {location}": "소스 발췌 {location}",
  "Copy": "복사",
  "Copied": "복사됨",
  "The indexed source revision and current repository state are synchronized.": "인덱싱된 소스 리비전과 현재 저장소 상태가 동기화되어 있습니다.",
  "Committed source changed after the indexed revision. Recorded Specs may need review.": "인덱싱된 리비전 이후 커밋된 소스가 변경되었습니다. 기록된 스펙을 검토해야 할 수 있습니다.",
  "Uncommitted source changes are outside the indexed revision. Impact is shown only where a recorded trace exists.": "커밋되지 않은 소스 변경은 인덱싱된 리비전 밖에 있습니다. 기록된 추적 관계가 있는 영향만 표시합니다.",
  "CodeWiki cannot establish source freshness from the available repository data, so it does not infer stale Specs.": "사용 가능한 저장소 데이터로 소스 최신 여부를 확인할 수 없어 CodeWiki는 오래된 스펙을 추정하지 않습니다.",
  "Repository freshness is unavailable.": "저장소 최신 여부를 확인할 수 없습니다.",
  "Changed files": "변경된 파일",
  "Affected entities": "영향받는 엔터티",
  "Validation findings": "검증 결과",
  "Evidence-based impact": "근거 기반 영향",
  "Changed file → affected Spec": "변경된 파일 → 영향받는 스펙",
  "Only recorded Core trace relationships are shown.": "Core에 기록된 추적 관계만 표시합니다.",
  "No changed source files": "변경된 소스 파일 없음",
  "No reliable change set is available for this repository.": "이 저장소에서 신뢰할 수 있는 변경 집합을 확인할 수 없습니다.",
  "The indexed source scope has no current changes.": "인덱싱된 소스 범위에 현재 변경 사항이 없습니다.",
  "Requirements and Criteria": "요구사항과 인수 기준",
  "Recorded trace intersects a changed file": "기록된 추적 관계가 변경 파일과 연결됨",
  "No Spec entity is marked potentially affected. This is not a claim that unrecorded relationships do not exist.": "영향 가능성이 표시된 스펙 엔터티가 없습니다. 기록되지 않은 관계도 없다는 의미는 아닙니다.",
  "Repository basis": "저장소 기준",
  "Revision state": "리비전 상태",
  "Indexed": "인덱싱됨",
  "Current": "현재",
  "Committed changes": "커밋된 변경",
  "Uncommitted changes": "커밋되지 않은 변경",
  "Core validation": "Core 검증",
  "Current findings": "현재 결과",
  "Review needed": "검토 필요",
  "pass": "통과",
  "fail": "실패",
  "warn": "경고",
  "All validation checks passed.": "모든 검증 항목을 통과했습니다.",
  " The recorded trace structure currently resolves.": " 현재 기록된 추적 구조가 올바르게 연결됩니다.",
  "Repository impact": "저장소 영향",
  "Review source changes through recorded Spec ↔ Code relationships. Unknown impact is kept explicit rather than guessed.": "기록된 스펙 ↔ 코드 관계를 통해 소스 변경을 검토하세요. 알 수 없는 영향은 추측하지 않고 명확하게 표시합니다.",
  "Refresh": "새로고침",
  "Changed file": "변경된 파일",
  "Recorded affected entities": "기록상 영향받는 엔터티",
  "Trace unavailable": "추적 정보 사용 불가",
  "No recorded Spec trace": "기록된 스펙 추적 정보 없음",
  "Core lexical search": "Core 어휘 검색",
  "Results are ranked by the same deterministic search used by the CodeWiki CLI. Only Requirements, Acceptance Criteria, and Spec documents are shown.": "CodeWiki CLI와 동일한 결정적 검색 순서로 결과를 표시합니다. 요구사항, 인수 기준 및 스펙 문서만 표시됩니다.",
  "Search CodeWiki entities": "CodeWiki 엔터티 검색",
  "Try an ID, behavior, path, or symbol": "ID, 동작, 경로 또는 심볼을 입력해 보세요",
  "Search by intent": "의도로 검색하기",
  "Enter a Requirement ID, Acceptance Criterion, Spec phrase, path, or recorded symbol.": "요구사항 ID, 인수 기준, 스펙 문구, 경로 또는 기록된 심볼을 입력하세요.",
  "No Spec entities found": "스펙 엔터티를 찾지 못했습니다",
  "The Core search returned no matching Requirement, Acceptance Criterion, or Spec document.": "Core 검색에서 일치하는 요구사항, 인수 기준 또는 스펙 문서를 찾지 못했습니다.",
  "Search results": "검색 결과",
  "{count} Spec result for “{query}”": "“{query}”에 대한 스펙 결과 {count}개",
  "{count} Spec results for “{query}”": "“{query}”에 대한 스펙 결과 {count}개",
  "Ranked by Core": "Core 순위",
  "Spec Document": "스펙 문서",
  "Rank {rank}": "순위 {rank}",
  "No matching excerpt is available.": "일치하는 발췌문이 없습니다.",
  "id_exact": "ID 정확히 일치",
  "path_or_symbol_exact": "경로 또는 심볼 정확히 일치",
  "title_exact": "제목 정확히 일치",
  "phrase": "문구 일치",
  "all_tokens": "모든 단어 일치",
  "some_tokens": "일부 단어 일치",
  "score {score}": "점수 {score}",
  "{page} · CodeWiki": "{page} · CodeWiki",
  "Loading {page}…": "{page} 불러오는 중…",
  "{page} loaded.": "{page} 화면을 불러왔습니다.",
  "The requested CodeWiki view could not be loaded.": "요청한 CodeWiki 화면을 불러오지 못했습니다.",
  "CodeWiki failed to initialize.": "CodeWiki를 초기화하지 못했습니다."
});

function normalizeLocale(value) {
  return String(value || "").toLowerCase().startsWith("ko") ? "ko" : "en";
}

function preferredLocale() {
  try {
    const stored = window.localStorage.getItem(LOCALE_STORAGE_KEY);
    if (SUPPORTED_LOCALES.has(stored)) return stored;
  } catch (_error) {
    // Storage can be unavailable in hardened or private browser contexts.
  }
  const browserLocale = navigator.languages?.[0] || navigator.language || "en";
  return normalizeLocale(browserLocale);
}

function t(message, values = {}) {
  const template = state.locale === "ko" ? (KO_MESSAGES[message] || message) : message;
  return template.replace(/\{([A-Za-z][A-Za-z0-9]*)\}/g, (_match, name) =>
    Object.prototype.hasOwnProperty.call(values, name) ? String(values[name]) : `{${name}}`
  );
}

function countMessage(count, singular, plural, values = {}) {
  return t(count === 1 ? singular : plural, { count, ...values });
}


class ApiError extends Error {
  constructor(message, status, code, details = {}) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.code = code;
    this.details = details;
  }
}

const state = {
  locale: preferredLocale(),
  index: null,
  status: null,
  validation: null,
  renderToken: 0,
};

const main = document.querySelector("#main-content");
const announcer = document.querySelector("#app-announcer");
const searchForm = document.querySelector("#global-search");
const searchInput = document.querySelector("#global-search-input");
const headerStatus = document.querySelector("#header-status");
const languageSelect = document.querySelector("#language-select");

function applyStaticTranslations() {
  document.documentElement.lang = state.locale;
  languageSelect.value = state.locale;
  for (const element of document.querySelectorAll("[data-i18n]")) {
    element.textContent = t(element.dataset.i18n);
  }
  for (const [dataName, attribute] of [
    ["i18nAriaLabel", "aria-label"],
    ["i18nPlaceholder", "placeholder"],
    ["i18nContent", "content"],
  ]) {
    for (const element of document.querySelectorAll(`[data-${dataName.replace(/[A-Z]/g, (letter) => `-${letter.toLowerCase()}`)}]`)) {
      element.setAttribute(attribute, t(element.dataset[dataName]));
    }
  }
  document.title = t("CodeWiki · Spec Traceability");
}

function node(tag, attributes = {}, ...children) {
  const element = document.createElement(tag);
  for (const [name, value] of Object.entries(attributes)) {
    if (value === null || value === undefined || value === false) continue;
    if (name === "class") {
      element.className = value;
    } else if (name === "text") {
      element.textContent = value;
    } else if (name.startsWith("on") && typeof value === "function") {
      element.addEventListener(name.slice(2).toLowerCase(), value);
    } else if (value === true) {
      element.setAttribute(name, "");
    } else {
      element.setAttribute(name, String(value));
    }
  }
  appendChildren(element, children);
  return element;
}

function appendChildren(parent, children) {
  for (const child of children.flat(Infinity)) {
    if (child === null || child === undefined || child === false) continue;
    parent.append(child instanceof Node ? child : document.createTextNode(String(child)));
  }
}

function fragment(...children) {
  const value = document.createDocumentFragment();
  appendChildren(value, children);
  return value;
}

async function api(path, parameters = {}) {
  const url = new URL(path, window.location.origin);
  for (const [name, value] of Object.entries(parameters)) {
    if (value !== null && value !== undefined) url.searchParams.set(name, String(value));
  }
  const response = await fetch(url, {
    headers: { Accept: "application/json" },
    credentials: "same-origin",
  });
  let payload;
  try {
    payload = await response.json();
  } catch (_error) {
    throw new ApiError(t("The viewer received an invalid server response."), response.status, "invalid_response");
  }
  if (!response.ok) {
    const error = payload.error || {};
    throw new ApiError(error.message || t("Request failed ({status}).", { status: response.status }), response.status, error.code || "request_failed", error.details || {});
  }
  return payload;
}

function readRoute() {
  const raw = window.location.hash ? window.location.hash.slice(1) : "/overview";
  const parsed = new URL(raw.startsWith("/") ? raw : `/${raw}`, "http://codewiki.local");
  const page = parsed.pathname.split("/").filter(Boolean)[0] || "overview";
  return {
    page: ["overview", "explorer", "changes", "search"].includes(page) ? page : "overview",
    parameters: parsed.searchParams,
  };
}

function routeHref(page, parameters = {}) {
  const query = new URLSearchParams();
  for (const [name, value] of Object.entries(parameters)) {
    if (value !== null && value !== undefined && value !== "") query.set(name, value);
  }
  const suffix = query.toString() ? `?${query.toString()}` : "";
  return `#/${page}${suffix}`;
}

function entityHref(id) {
  return routeHref("explorer", { id });
}

function documentHref(path) {
  return routeHref("explorer", { doc: path });
}

function statusTone(value) {
  if (value === "synchronized" || value === "pass") return "pass";
  if (value === "stale" || value === "fail") return "fail";
  if (value === "working_tree_changed" || value === "warn") return "warn";
  return "neutral";
}

function statusLabel(value) {
  return {
    synchronized: t("Synchronized"),
    stale: t("Potentially stale"),
    working_tree_changed: t("Working tree changed"),
    unknown: t("Freshness unknown"),
  }[value] || value || t("Unknown");
}

function badge(label, tone = "neutral") {
  return node("span", { class: `badge badge-${tone}` }, label);
}

function iconLabel(symbol, label) {
  return node("span", { class: "icon-label" }, node("span", { "aria-hidden": "true" }, symbol), label);
}

function loadingPanel(label = t("Loading…")) {
  return node("section", { class: "loading-page", "aria-label": label },
    node("div", { class: "loading-mark", "aria-hidden": "true" }, "CW"),
    node("p", {}, label),
  );
}

function emptyState(title, message) {
  return node("div", { class: "empty-state" },
    node("span", { class: "empty-icon", "aria-hidden": "true" }, "◇"),
    node("h3", {}, title),
    node("p", {}, message),
  );
}

function renderError(error) {
  const message = error instanceof Error ? error.message : t("An unexpected viewer error occurred.");
  return node("section", { class: "error-page" },
    badge(t("Request failed"), "fail"),
    node("h1", {}, t("CodeWiki could not load this view")),
    node("p", {}, message),
    error instanceof ApiError ? node("code", {}, error.code) : null,
    node("a", { class: "button button-primary", href: "#/overview" }, t("Return to Overview")),
  );
}

function setActiveNavigation(page) {
  for (const link of document.querySelectorAll("[data-nav]")) {
    const active = link.dataset.nav === page || (page === "search" && false);
    link.classList.toggle("active", active);
    if (active) link.setAttribute("aria-current", "page");
    else link.removeAttribute("aria-current");
  }
}

function updateHeaderStatus() {
  const value = state.status?.state || "unknown";
  const tone = statusTone(value);
  headerStatus.className = `header-status status-${tone}`;
  headerStatus.replaceChildren(
    node("span", { class: "status-dot", "aria-hidden": "true" }),
    node("span", {}, statusLabel(value)),
  );
  headerStatus.setAttribute("aria-label", t("{status}. Open Changes.", { status: statusLabel(value) }));
}

function specEntityIds(spec) {
  return [...(spec.requirement_ids || []), ...(spec.acceptance_criterion_ids || [])];
}

function firstEntityId() {
  for (const spec of state.index.specs || []) {
    const id = (spec.requirement_ids || [])[0] || (spec.acceptance_criterion_ids || [])[0];
    if (id) return id;
  }
  return null;
}

function findSpecByEntity(id) {
  return (state.index.specs || []).find((spec) => specEntityIds(spec).includes(id));
}

function findSpecByPath(path) {
  return (state.index.specs || []).find((spec) => spec.path === path);
}

function formatDocumentType(value) {
  return {
    project_spec: t("Project memory"),
    domain_spec: t("Domain Spec"),
    policy_spec: t("Policy Spec"),
    spec: t("Spec"),
  }[value] || t("Spec");
}

function formatEntityType(value) {
  return value === "acceptance_criterion" ? t("Acceptance Criterion") : t("Requirement");
}

function formatReferenceKind(value) {
  return ["file", "symbol", "route", "model"].includes(value) ? t(value) : value.replaceAll("_", " ");
}

function formatMatchType(value) {
  return t(value).replaceAll("_", " ");
}

function formatValidationStatus(value) {
  return ["pass", "fail", "warn"].includes(value) ? t(value) : value;
}

function routeLabel(page) {
  return {
    overview: t("Overview"),
    explorer: t("Explorer"),
    changes: t("Changes"),
    search: t("Search"),
  }[page] || page;
}

function shortRevision(value) {
  if (!value) return t("Unavailable");
  return value.length > 12 ? value.slice(0, 12) : value;
}

function pageHeading(eyebrow, title, description, actions = []) {
  return node("header", { class: "page-heading" },
    node("div", {},
      node("p", { class: "eyebrow" }, eyebrow),
      node("h1", {}, title),
      node("p", { class: "page-description" }, description),
    ),
    actions.length ? node("div", { class: "page-actions" }, actions) : null,
  );
}

function metricCard(label, value, detail, tone = "default") {
  return node("article", { class: `metric-card metric-${tone}` },
    node("p", { class: "metric-label" }, label),
    node("strong", { class: "metric-value" }, String(value)),
    node("p", { class: "metric-detail" }, detail),
  );
}

function renderOverview() {
  const index = state.index;
  const total = index.entity_count || 0;
  const traced = index.traced_entity_count || 0;
  const tracePercent = total ? Math.round((traced / total) * 100) : 0;
  const untraced = index.untraced_entity_ids || [];
  const validationTone = state.validation?.valid ? "pass" : "fail";
  const status = state.status;

  const hero = node("section", { class: "overview-hero" },
    node("div", { class: "hero-copy" },
      badge(t("Spec-first workspace"), "accent"),
      node("h1", {}, t("See what should happen—and where it happens.")),
      node("p", {}, t("Start with a Spec. Move through requirements, acceptance criteria, and the exact implementation without losing context.")),
      node("div", { class: "hero-actions" },
        node("a", { class: "button button-primary", href: routeHref("explorer", { id: firstEntityId() || "" }) }, t("Explore requirements")),
        node("a", { class: "button button-weak", href: "#/changes" }, t("Review changes")),
      ),
    ),
    node("ol", { class: "intent-flow", "aria-label": t("CodeWiki exploration flow") },
      node("li", {}, node("span", {}, "1"), node("strong", {}, t("Spec")), node("small", {}, t("Approved intent"))),
      node("li", {}, node("span", {}, "2"), node("strong", {}, t("Requirement")), node("small", {}, t("Expected behavior"))),
      node("li", {}, node("span", {}, "3"), node("strong", {}, t("Acceptance")), node("small", {}, t("Observable proof"))),
      node("li", {}, node("span", {}, "4"), node("strong", {}, t("Code")), node("small", {}, t("Current implementation"))),
    ),
  );

  const metrics = node("section", { class: "metric-grid", "aria-label": t("CodeWiki summary") },
    metricCard(t("Spec documents"), index.specs.length, t("Project, domain, and policy Specs")),
    metricCard(t("Requirements"), index.requirement_count || 0, t("Normative behavior statements"), "accent"),
    metricCard(t("Acceptance Criteria"), index.acceptance_criterion_count || 0, t("Observable verification outcomes")),
    metricCard(t("Traceability"), `${tracePercent}%`, t("{traced} of {total} entities linked", { traced, total }), tracePercent === 100 ? "pass" : "warn"),
  );

  const health = node("section", { class: "health-strip" },
    node("div", {},
      node("p", { class: "section-kicker" }, t("Current CodeWiki state")),
      node("h2", {}, statusLabel(status.state)),
      node("p", {}, status.state === "unknown" ? t("Freshness cannot be established from the available Git and coverage data. CodeWiki does not guess.") : t("Synchronization is derived from reference/coverage.json and the current Git state.")),
    ),
    node("dl", { class: "health-facts" },
      node("div", {}, node("dt", {}, t("Validation")), node("dd", {}, badge(state.validation.valid ? t("Valid") : t("{count} failed", { count: state.validation.failed }), validationTone))),
      node("div", {}, node("dt", {}, t("Indexed revision")), node("dd", {}, shortRevision(status.indexed_revision))),
      node("div", {}, node("dt", {}, t("Current revision")), node("dd", {}, shortRevision(status.current_revision))),
    ),
    node("a", { class: "text-link", href: "#/changes" }, t("See change impact"), node("span", { "aria-hidden": "true" }, " →")),
  );

  const gaps = node("section", { class: "content-section" },
    node("div", { class: "section-heading" },
      node("div", {}, node("p", { class: "section-kicker" }, t("Traceability gaps")), node("h2", {}, t("Unlinked Requirements and Criteria"))),
      badge(untraced.length ? t("{count} unlinked", { count: untraced.length }) : t("Complete"), untraced.length ? "warn" : "pass"),
    ),
    untraced.length
      ? node("div", { class: "entity-chip-list" }, untraced.map((id) => node("a", { class: "entity-chip chip-unlinked", href: entityHref(id) }, id, node("span", {}, t("No recorded implementation")))))
      : node("div", { class: "success-callout" }, node("span", { "aria-hidden": "true" }, "✓"), node("p", {}, node("strong", {}, t("Every parsed entity has a recorded feature trace.")), t(" Open any Spec to inspect its exact evidence."))),
  );

  const specCards = node("section", { class: "content-section" },
    node("div", { class: "section-heading" },
      node("div", {}, node("p", { class: "section-kicker" }, t("Functional structure")), node("h2", {}, t("Specs"))),
      node("p", { class: "section-aside" }, t("Select a Spec to continue in Explorer.")),
    ),
    index.specs.length
      ? node("div", { class: "spec-card-grid" }, index.specs.map(renderSpecCard))
      : emptyState(t("No Specs found"), t("The Wiki has no managed Spec documents yet.")),
  );

  return node("div", { class: "overview-page" }, hero, metrics, health, gaps, specCards);
}

function renderSpecCard(spec) {
  const requirements = spec.requirement_ids || [];
  const criteria = spec.acceptance_criterion_ids || [];
  const entityCount = requirements.length + criteria.length;
  const traced = (spec.traced_entity_ids || []).length;
  const destination = requirements[0] || criteria[0]
    ? entityHref(requirements[0] || criteria[0])
    : documentHref(spec.path);
  return node("a", { class: "spec-card", href: destination },
    node("div", { class: "spec-card-top" },
      badge(formatDocumentType(spec.document_type), "neutral"),
      node("span", { class: `trace-indicator ${traced === entityCount ? "complete" : "partial"}` }, t("{traced}/{total} linked", { traced, total: entityCount })),
    ),
    node("h3", {}, spec.title),
    node("p", { class: "spec-description" }, spec.description || t("No summary is recorded for this Spec.")),
    node("dl", { class: "spec-counts" },
      node("div", {}, node("dt", {}, t("Requirements")), node("dd", {}, String(requirements.length))),
      node("div", {}, node("dt", {}, t("Criteria")), node("dd", {}, String(criteria.length))),
    ),
    node("progress", { max: Math.max(entityCount, 1), value: traced, "aria-label": t("{title} trace coverage", { title: spec.title }) }),
    node("span", { class: "card-link" }, t("Explore Spec"), node("span", { "aria-hidden": "true" }, " →")),
  );
}

async function renderExplorer(parameters) {
  let selectedId = parameters.get("id");
  let selectedDocument = parameters.get("doc");
  if (!selectedId && !selectedDocument) selectedId = firstEntityId();

  let detail = null;
  let context = null;
  let selectedPath = selectedDocument;
  if (selectedId) {
    [detail, context] = await Promise.all([
      api("/api/spec", { id: selectedId }),
      api("/api/context", { target: selectedId }),
    ]);
    selectedPath = detail.entity.spec_path;
  }

  const spec = findSpecByPath(selectedPath) || (selectedId ? findSpecByEntity(selectedId) : null);
  const indexPane = renderSpecIndex(selectedId, selectedPath);
  const specPane = detail
    ? renderEntityDetail(detail)
    : renderDocumentDetail(spec);
  const tracePane = detail
    ? renderTraceability(detail, context)
    : node("aside", { class: "pane trace-pane", "aria-label": t("Implementation traceability") },
        paneHeader(t("Implementation Traceability"), t("Select a Requirement or Acceptance Criterion")),
        emptyState(t("Choose a Spec entity"), t("Traceability is shown locally for the selected Requirement or Acceptance Criterion.")),
      );

  return node("section", { class: "explorer-layout", "aria-label": t("Spec Explorer") }, indexPane, specPane, tracePane);
}

function paneHeader(title, subtitle) {
  return node("header", { class: "pane-header" }, node("h2", {}, title), node("p", {}, subtitle));
}

function renderSpecIndex(selectedId, selectedPath) {
  return node("aside", { class: "pane spec-index-pane", "aria-label": t("Spec Index") },
    paneHeader(t("Spec Index"), t("Navigate by behavior, not files")),
    node("nav", { class: "spec-index", "aria-label": t("Specs and requirements") },
      (state.index.specs || []).map((spec) => {
        const requirements = spec.requirement_ids || [];
        const criteria = spec.acceptance_criterion_ids || [];
        const isSelected = spec.path === selectedPath;
        return node("details", { class: "spec-index-group", open: isSelected || (!selectedPath && spec === state.index.specs[0]) },
          node("summary", {},
            node("span", { class: "summary-title" }, spec.title),
            node("span", { class: "summary-count" }, String(requirements.length + criteria.length)),
          ),
          node("div", { class: "index-group-body" },
            node("a", { class: `document-link ${isSelected && !selectedId ? "current" : ""}`, href: documentHref(spec.path), "aria-current": isSelected && !selectedId ? "page" : null },
              node("span", { "aria-hidden": "true" }, "◫"), t("Spec overview")),
            requirements.length ? node("p", { class: "index-label" }, t("Requirements")) : null,
            requirements.map((id) => renderIndexEntity(spec, id, selectedId)),
            criteria.length ? node("p", { class: "index-label" }, t("Acceptance Criteria")) : null,
            criteria.map((id) => renderIndexEntity(spec, id, selectedId)),
          ),
        );
      }),
    ),
  );
}

function renderIndexEntity(spec, id, selectedId) {
  const linked = (spec.traced_entity_ids || []).includes(id);
  const current = id === selectedId;
  return node("a", { class: `index-entity ${current ? "current" : ""}`, href: entityHref(id), "aria-current": current ? "page" : null },
    node("span", { class: `trace-dot ${linked ? "linked" : "unlinked"}`, title: linked ? t("Implementation trace recorded") : t("No implementation trace"), "aria-label": linked ? t("traced") : t("untraced") }),
    node("span", {}, id),
  );
}

function renderDocumentDetail(spec) {
  if (!spec) {
    return node("article", { class: "pane spec-detail-pane" }, paneHeader(t("Spec View"), t("Structured Spec information")), emptyState(t("Spec not found"), t("Choose a Spec from the index.")));
  }
  const requirements = spec.requirement_ids || [];
  const criteria = spec.acceptance_criterion_ids || [];
  return node("article", { class: "pane spec-detail-pane", "aria-label": t("{title} Spec overview", { title: spec.title }) },
    paneHeader(t("Spec View"), spec.path),
    node("div", { class: "detail-content" },
      node("header", { class: "entity-heading" }, badge(formatDocumentType(spec.document_type)), node("h1", {}, spec.title), node("p", { class: "entity-lead" }, spec.description || t("No summary is recorded."))),
      renderEntityLinkSection(t("Requirements"), requirements, t("No Requirements are parsed from this Spec.")),
      renderEntityLinkSection(t("Acceptance Criteria"), criteria, t("No Acceptance Criteria are parsed from this Spec.")),
    ),
  );
}

function renderEntityLinkSection(title, ids, fallback) {
  return node("section", { class: "detail-section" },
    node("div", { class: "detail-section-heading" }, node("h2", {}, title), badge(String(ids.length))),
    ids.length ? node("div", { class: "entity-link-grid" }, ids.map((id) => node("a", { href: entityHref(id), class: "entity-link-card" }, node("strong", {}, id), node("span", {}, t("Open in Explorer →"))))) : node("p", { class: "muted" }, fallback),
  );
}

function renderEntityDetail(detail) {
  const entity = detail.entity;
  const relatedCriteria = detail.related_entities.filter((item) => item.entity_type === "acceptance_criterion");
  const relatedRequirements = detail.related_entities.filter((item) => item.entity_type === "requirement");
  return node("article", { class: "pane spec-detail-pane", "aria-label": t("{id} Spec detail", { id: entity.id }) },
    paneHeader(t("Spec View"), entity.spec_title),
    node("div", { class: "detail-content" },
      node("nav", { class: "breadcrumb", "aria-label": t("Spec location") },
        node("a", { href: documentHref(entity.spec_path) }, entity.spec_title),
        node("span", { "aria-hidden": "true" }, "/"),
        node("span", {}, entity.section),
      ),
      node("header", { class: "entity-heading" },
        badge(formatEntityType(entity.entity_type), entity.entity_type === "requirement" ? "accent" : "purple"),
        node("h1", {}, entity.id),
        node("p", { class: "entity-context" }, entity.section),
      ),
      node("section", { class: "entity-statement", "aria-labelledby": "statement-title" },
        node("p", { class: "section-kicker", id: "statement-title" }, entity.entity_type === "requirement" ? t("Normative requirement") : t("Observable outcome")),
        node("div", { class: "entity-body" }, entity.body || t("No body is recorded.")),
      ),
      relatedCriteria.length ? renderRelatedEntities(t("Acceptance Criteria"), t("Observable outcomes related by the Core parser"), relatedCriteria) : null,
      relatedRequirements.length ? renderRelatedEntities(t("Related Requirements"), t("Requirements in the owning Spec"), relatedRequirements) : null,
      node("section", { class: "detail-section related-spec" },
        node("p", { class: "section-kicker" }, t("Owning Spec")),
        node("a", { href: documentHref(entity.spec_path) }, node("strong", {}, entity.spec_title), node("code", {}, entity.spec_path), node("span", { "aria-hidden": "true" }, "→")),
      ),
    ),
  );
}

function renderRelatedEntities(title, description, entities) {
  return node("section", { class: "detail-section" },
    node("div", { class: "detail-section-heading" }, node("div", {}, node("h2", {}, title), node("p", {}, description)), badge(String(entities.length))),
    node("div", { class: "related-entity-list" }, entities.map((entity) => node("a", { class: "related-entity", href: entityHref(entity.id) },
      node("div", {}, badge(formatEntityType(entity.entity_type), entity.entity_type === "requirement" ? "accent" : "purple"), node("strong", {}, entity.id)),
      node("p", {}, entity.body || t("No body is recorded.")),
      node("span", { class: "related-arrow", "aria-hidden": "true" }, "→"),
    ))),
  );
}

function renderTraceability(detail, context) {
  const links = detail.feature_links || [];
  const references = detail.code_references || [];
  const excerpts = context.source_excerpts || [];
  const testReferences = references.filter(isTestReference);
  const implementationReferences = references.filter((reference) => !isTestReference(reference));
  return node("aside", { class: "pane trace-pane", "aria-label": t("Implementation traceability") },
    paneHeader(t("Implementation Traceability"), t("{features} · {references}", { features: countMessage(links.length, "{count} feature link", "{count} feature links"), references: countMessage(references.length, "{count} code reference", "{count} code references") })),
    node("div", { class: "trace-content" },
      renderLocalTraceMap(detail),
      links.length ? node("section", { class: "trace-section" },
        traceSectionHeading(t("Implementation"), t("Recorded feature traces"), links.length),
        node("div", { class: "feature-list" }, links.map((link) => node("article", { class: "feature-card" },
          node("div", {}, badge(link.relation === "direct" ? t("Direct") : t("Via requirement"), link.relation === "direct" ? "accent" : "purple"), node("h3", {}, link.feature_id)),
          node("p", {}, link.via_spec_ids.length ? t("Spec Basis: {ids}", { ids: link.via_spec_ids.join(", ") }) : t("No Spec Basis is recorded.")),
          link.reference_path ? node("code", {}, link.reference_path) : null,
        ))),
      ) : emptyState(t("No implementation trace"), t("No feature in CodeWiki currently links this entity to implementation.")),
      implementationReferences.length ? renderReferenceSection(t("Code references"), implementationReferences) : null,
      testReferences.length ? renderReferenceSection(t("Related tests"), testReferences) : null,
      excerpts.length ? node("section", { class: "trace-section" },
        traceSectionHeading(t("Actual code"), t("Bounded source excerpts from Core"), excerpts.length),
        node("div", { class: "excerpt-list" }, excerpts.map(renderExcerpt)),
      ) : node("section", { class: "trace-section" }, traceSectionHeading(t("Actual code"), t("Bounded source excerpts from Core"), 0), node("p", { class: "muted" }, t("No readable source excerpt is available for the recorded references."))),
    ),
  );
}

function renderLocalTraceMap(detail) {
  const entity = detail.entity;
  const related = detail.related_entities || [];
  const requirements = entity.entity_type === "requirement" ? [entity] : related.filter((item) => item.entity_type === "requirement");
  const criteria = entity.entity_type === "acceptance_criterion" ? [entity] : related.filter((item) => item.entity_type === "acceptance_criterion");
  const features = (detail.feature_links || []).map((link) => link.feature_id);
  const allCodeNodes = uniqueValues((detail.code_references || []).map((reference) => reference.kind === "symbol" ? reference.value : (reference.path || reference.value)));
  const codeNodes = allCodeNodes.slice(0, 12);
  return node("section", { class: "local-trace-section", "aria-labelledby": "local-trace-title" },
    node("div", { class: "trace-section-heading" },
      node("div", {}, node("p", { class: "section-kicker" }, t("Selected entity only")), node("h2", { id: "local-trace-title" }, t("Local Trace Map"))),
      badge(t("Local"), "accent"),
    ),
    node("ol", { class: "local-trace-map", "aria-label": t("Requirement to actual code flow") },
      traceStage(t("Requirement"), requirements.map((item) => item.id), "requirement"),
      traceStage(t("Acceptance Criteria"), criteria.map((item) => item.id), "criterion"),
      traceStage(t("Implementation"), uniqueValues(features), "feature"),
      traceStage(t("Actual Code"), codeNodes, "code"),
    ),
    codeNodes.length < allCodeNodes.length ? node("p", { class: "map-note" }, t("Showing {shown} local code nodes of {total}.", { shown: codeNodes.length, total: allCodeNodes.length })) : null,
  );
}

function traceStage(label, values, kind) {
  return node("li", { class: `trace-stage stage-${kind}` },
    node("p", {}, label),
    node("div", { class: "trace-stage-nodes" },
      values.length ? values.map((value) => node("span", {}, value)) : node("span", { class: "trace-missing" }, t("No recorded link")),
    ),
  );
}

function traceSectionHeading(title, subtitle, count) {
  return node("div", { class: "trace-section-heading" }, node("div", {}, node("h2", {}, title), node("p", {}, subtitle)), badge(String(count)));
}

function isTestReference(reference) {
  if (reference.kind !== "file") return false;
  const path = reference.path || reference.value || "";
  return /(^|\/)(tests?|__tests__)(\/|$)/i.test(path) || /(^|\/)test_[^/]+\.[^/]+$/i.test(path);
}

function renderReferenceSection(title, references) {
  return node("section", { class: "trace-section" },
    traceSectionHeading(title, title === t("Related tests") ? t("Verification surfaces recorded in coverage") : t("Files, symbols, routes, and models"), references.length),
    node("div", { class: "reference-list" }, references.map((reference) => node("article", { class: "reference-item" },
      node("div", { class: "reference-icon", "aria-hidden": "true" }, reference.kind === "symbol" ? "ƒ" : reference.kind === "file" ? "▤" : "↗"),
      node("div", { class: "reference-copy" },
        node("p", {}, node("strong", {}, reference.value)),
        reference.path && reference.path !== reference.value ? node("code", {}, reference.path) : null,
        node("small", {}, `${formatReferenceKind(reference.kind)} · ${reference.source}`),
      ),
      reference.exists === false ? badge(t("Missing"), "fail") : reference.exists === true ? badge(t("Exists"), "pass") : badge(t("Recorded")),
    ))),
  );
}

function renderExcerpt(excerpt) {
  const location = `${excerpt.path}:${excerpt.start_line}–${excerpt.end_line}`;
  return node("article", { class: "source-excerpt" },
    node("header", {}, node("div", {}, node("strong", {}, excerpt.symbol || t("Source excerpt")), node("code", {}, location)), node("button", { type: "button", class: "copy-button", onClick: async (event) => copyExcerpt(excerpt.text, event.currentTarget) }, t("Copy"))),
    node("pre", { tabindex: "0", "aria-label": t("Source excerpt {location}", { location }) }, node("code", {}, excerpt.text)),
  );
}

async function copyExcerpt(text, button) {
  try {
    await navigator.clipboard.writeText(text);
    button.textContent = t("Copied");
    window.setTimeout(() => { button.textContent = t("Copy"); }, 1200);
  } catch (_error) {
    button.textContent = t("Unavailable");
  }
}

function uniqueValues(values) {
  return [...new Set(values.filter(Boolean))];
}

async function renderChanges() {
  const [status, validation] = await Promise.all([api("/api/status"), api("/api/validate")]);
  state.status = status;
  state.validation = validation;
  updateHeaderStatus();

  const impacts = await Promise.all((status.changed_files || []).map(async (path) => {
    try {
      const trace = await api("/api/trace", { target: path });
      return { path, trace, error: null };
    } catch (error) {
      if (error instanceof ApiError && error.status === 404) return { path, trace: null, error: null };
      return { path, trace: null, error };
    }
  }));

  const affected = status.potentially_affected_specs || [];
  const stateDescription = {
    synchronized: t("The indexed source revision and current repository state are synchronized."),
    stale: t("Committed source changed after the indexed revision. Recorded Specs may need review."),
    working_tree_changed: t("Uncommitted source changes are outside the indexed revision. Impact is shown only where a recorded trace exists."),
    unknown: t("CodeWiki cannot establish source freshness from the available repository data, so it does not infer stale Specs."),
  }[status.state] || t("Repository freshness is unavailable.");

  const summary = node("section", { class: `change-summary summary-${statusTone(status.state)}` },
    node("div", {}, badge(statusLabel(status.state), statusTone(status.state)), node("h2", {}, stateDescription)),
    node("dl", {},
      node("div", {}, node("dt", {}, t("Changed files")), node("dd", {}, String((status.changed_files || []).length))),
      node("div", {}, node("dt", {}, t("Affected entities")), node("dd", {}, String(affected.length))),
      node("div", {}, node("dt", {}, t("Validation findings")), node("dd", {}, String((validation.failed || 0) + (validation.warnings || 0)))),
    ),
  );

  const impactFlow = node("section", { class: "content-section" },
    node("div", { class: "section-heading" },
      node("div", {}, node("p", { class: "section-kicker" }, t("Evidence-based impact")), node("h2", {}, t("Changed file → affected Spec"))),
      node("p", { class: "section-aside" }, t("Only recorded Core trace relationships are shown.")),
    ),
    impacts.length ? node("div", { class: "change-list" }, impacts.map(renderChangeImpact)) : emptyState(t("No changed source files"), status.state === "unknown" ? t("No reliable change set is available for this repository.") : t("The indexed source scope has no current changes.")),
  );

  const potentiallyStale = node("section", { class: "content-section split-section" },
    node("div", {},
      node("div", { class: "section-heading compact" }, node("div", {}, node("p", { class: "section-kicker" }, t("Potentially stale")), node("h2", {}, t("Requirements and Criteria"))), badge(String(affected.length), affected.length ? "warn" : "pass")),
      affected.length ? node("div", { class: "entity-chip-list vertical" }, affected.map((id) => node("a", { class: "entity-chip", href: entityHref(id) }, id, node("span", {}, t("Recorded trace intersects a changed file"))))) : node("p", { class: "muted-block" }, t("No Spec entity is marked potentially affected. This is not a claim that unrecorded relationships do not exist.")),
    ),
    node("div", {},
      node("div", { class: "section-heading compact" }, node("div", {}, node("p", { class: "section-kicker" }, t("Repository basis")), node("h2", {}, t("Revision state")))),
      node("dl", { class: "revision-list" },
        node("div", {}, node("dt", {}, t("Indexed")), node("dd", {}, node("code", {}, shortRevision(status.indexed_revision)))),
        node("div", {}, node("dt", {}, t("Current")), node("dd", {}, node("code", {}, shortRevision(status.current_revision)))),
        node("div", {}, node("dt", {}, t("Committed changes")), node("dd", {}, String((status.committed_changed_files || []).length))),
        node("div", {}, node("dt", {}, t("Uncommitted changes")), node("dd", {}, String((status.uncommitted_changed_files || []).length))),
      ),
      (status.warnings || []).length ? node("ul", { class: "warning-list" }, status.warnings.map((warning) => node("li", {}, warning))) : null,
    ),
  );

  const findings = (validation.checks || []).filter((check) => check.status !== "pass");
  const validationSection = node("section", { class: "content-section" },
    node("div", { class: "section-heading" }, node("div", {}, node("p", { class: "section-kicker" }, t("Core validation")), node("h2", {}, t("Current findings"))), badge(validation.valid ? t("Valid") : t("Review needed"), validation.valid ? "pass" : "fail")),
    findings.length ? node("div", { class: "finding-list" }, findings.map((finding) => node("article", { class: `finding finding-${statusTone(finding.status)}` }, badge(formatValidationStatus(finding.status), statusTone(finding.status)), node("div", {}, node("h3", {}, finding.check), node("p", {}, finding.message), finding.target ? node("code", {}, finding.target) : null)))) : node("div", { class: "success-callout" }, node("span", { "aria-hidden": "true" }, "✓"), node("p", {}, node("strong", {}, t("All validation checks passed.")), t(" The recorded trace structure currently resolves."))),
  );

  return node("div", { class: "standard-page changes-page" }, pageHeading(t("Repository impact"), t("Changes"), t("Review source changes through recorded Spec ↔ Code relationships. Unknown impact is kept explicit rather than guessed."), [node("button", { class: "button button-secondary", type: "button", onClick: () => renderCurrentRoute() }, t("Refresh"))]), summary, impactFlow, potentiallyStale, validationSection);
}

function renderChangeImpact(impact) {
  const entities = impact.trace?.entities || [];
  return node("article", { class: "change-card" },
    node("div", { class: "changed-file" }, node("span", { "aria-hidden": "true" }, "Δ"), node("div", {}, node("p", {}, t("Changed file")), node("code", {}, impact.path))),
    node("div", { class: "change-arrow", "aria-hidden": "true" }, "→"),
    node("div", { class: "affected-entities" },
      node("p", {}, t("Recorded affected entities")),
      impact.error ? badge(t("Trace unavailable"), "fail") : entities.length ? node("div", { class: "impact-links" }, entities.map((entity) => node("a", { href: entityHref(entity.id) }, entity.id))) : node("span", { class: "no-impact" }, t("No recorded Spec trace")),
    ),
  );
}

async function renderSearch(parameters) {
  const query = parameters.get("q") || "";
  searchInput.value = query;
  const payload = await api("/api/search", { q: query, limit: 50 });
  const results = (payload.results || []).filter((result) => result.id || (result.entity_type === "document" && result.path.startsWith("specs/") && result.path !== "specs/index.md"));
  const heading = pageHeading(t("Core lexical search"), t("Search"), t("Results are ranked by the same deterministic search used by the CodeWiki CLI. Only Requirements, Acceptance Criteria, and Spec documents are shown."));
  const searchBox = node("form", { class: "search-page-form", role: "search", onSubmit: (event) => submitSearch(event, event.currentTarget.querySelector("input")) },
    node("label", { for: "search-page-input" }, t("Search CodeWiki entities")),
    node("div", {}, node("input", { id: "search-page-input", type: "search", name: "q", value: query, placeholder: t("Try an ID, behavior, path, or symbol") }), node("button", { class: "button button-primary", type: "submit" }, t("Search"))),
  );
  let content;
  if (!query.trim()) {
    content = emptyState(t("Search by intent"), t("Enter a Requirement ID, Acceptance Criterion, Spec phrase, path, or recorded symbol."));
  } else if (!results.length) {
    content = emptyState(t("No Spec entities found"), t("The Core search returned no matching Requirement, Acceptance Criterion, or Spec document."));
  } else {
    content = node("section", { class: "search-results", "aria-label": t("Search results") },
      node("div", { class: "search-result-summary" }, node("p", {}, countMessage(results.length, "{count} Spec result for “{query}”", "{count} Spec results for “{query}”", { query })), node("span", {}, t("Ranked by Core"))),
      results.map(renderSearchResult),
    );
  }
  return node("div", { class: "standard-page search-page" }, heading, searchBox, content);
}

function renderSearchResult(result) {
  const type = result.id ? formatEntityType(result.entity_type) : t("Spec Document");
  const href = result.id ? entityHref(result.id) : documentHref(result.path);
  return node("a", { class: "search-result", href },
    node("div", { class: "result-rank", "aria-label": t("Rank {rank}", { rank: result.rank }) }, String(result.rank)),
    node("div", { class: "result-copy" },
      node("div", { class: "result-title" }, badge(type, result.entity_type === "acceptance_criterion" ? "purple" : result.id ? "accent" : "neutral"), node("h2", {}, result.id || result.title)),
      node("p", {}, result.snippet || t("No matching excerpt is available.")),
      node("div", { class: "result-meta" }, node("code", {}, result.path), node("span", {}, formatMatchType(result.match_type)), node("span", {}, t("score {score}", { score: result.score }))),
    ),
    node("span", { class: "result-arrow", "aria-hidden": "true" }, "→"),
  );
}

function submitSearch(event, input) {
  event.preventDefault();
  const query = input.value.trim();
  window.location.hash = routeHref("search", { q: query }).slice(1);
}

async function renderCurrentRoute() {
  if (!state.index || !state.status || !state.validation) return;
  const token = ++state.renderToken;
  const route = readRoute();
  setActiveNavigation(route.page);
  main.dataset.view = route.page;
  const localizedPage = routeLabel(route.page);
  document.title = t("{page} · CodeWiki", { page: localizedPage });
  main.replaceChildren(loadingPanel(t("Loading {page}…", { page: localizedPage })));
  try {
    let view;
    if (route.page === "overview") view = renderOverview();
    else if (route.page === "explorer") view = await renderExplorer(route.parameters);
    else if (route.page === "changes") view = await renderChanges();
    else view = await renderSearch(route.parameters);
    if (token !== state.renderToken) return;
    main.replaceChildren(view);
    announcer.textContent = t("{page} loaded.", { page: localizedPage });
  } catch (error) {
    if (token !== state.renderToken) return;
    main.replaceChildren(renderError(error));
    announcer.textContent = t("The requested CodeWiki view could not be loaded.");
  }
}

async function bootstrap() {
  try {
    [state.index, state.status, state.validation] = await Promise.all([
      api("/api/index"),
      api("/api/status"),
      api("/api/validate"),
    ]);
    updateHeaderStatus();
    await renderCurrentRoute();
  } catch (error) {
    main.replaceChildren(renderError(error));
    announcer.textContent = t("CodeWiki failed to initialize.");
  }
}

function changeLocale(value) {
  const locale = normalizeLocale(value);
  if (locale === state.locale) return;
  state.locale = locale;
  try {
    window.localStorage.setItem(LOCALE_STORAGE_KEY, locale);
  } catch (_error) {
    // The language still changes for this page when storage is unavailable.
  }
  applyStaticTranslations();
  if (state.status) updateHeaderStatus();
  announcer.textContent = t("Current language: {language}.", {
    language: t(locale === "ko" ? "Korean" : "English"),
  });
  renderCurrentRoute();
}

applyStaticTranslations();
searchForm.addEventListener("submit", (event) => submitSearch(event, searchInput));
languageSelect.addEventListener("change", (event) => changeLocale(event.currentTarget.value));
window.addEventListener("hashchange", () => {
  renderCurrentRoute();
  main.focus({ preventScroll: true });
});

bootstrap();
