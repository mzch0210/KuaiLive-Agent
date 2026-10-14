# N12-C0 | N11 152段落与图表迁移台账（只读现稿）

> **版本状态**：迁移台账已建立、正文未迁移、没有任何实验重跑。下表中的摘要用于逐段定位；真实引用和准确科学定义始终以冻结N11 LaTeX及公开A4/A5为准。

- 冻结主稿Git blob：`8ca7dc67ade90048eb0b12059ec8bec75c85194f`
- 冻结补充材料Git blob：`9b83a31d82f08d1a212f59f99b60975ad902e8e6`
- 源块：152；标签：59；主文表：13；图：3；现有章节：8；目标章节：7。

## 全段落迁移登记

| 序号 | N11所在章/节 | 原始行 | 标签或起始文本 | 目标位置 | 处理 |
| --- | --- | ---: | --- | --- | --- |
| N11-001 | Front matter | 1 | \documentclass[preprint,12pt]{elsarticle} | Front matter/references and technical metadata | PRESERVE_FORMAT |
| N11-002 | Front matter | 3 | \usepackage[T1]{fontenc} \usepackage[utf8]{inputenc} \usepackage{amsma | Front matter/references and technical metadata | PRESERVE_FORMAT |
| N11-003 | Front matter | 15 | \journal{Knowledge-Based Systems} | Front matter/references and technical metadata | PRESERVE_FORMAT |
| N11-004 | Front matter | 17 | \begin{document} | Front matter/references and technical metadata | PRESERVE_FORMAT |
| N11-005 | Front matter | 19 | \begin{frontmatter} | Front matter/references and technical metadata | PRESERVE_FORMAT |
| N11-006 | Front matter | 21 | \title{When Does Relationship Memory Help? Base-Relative Evidence Valu | Front matter/references and technical metadata | PRESERVE_FORMAT |
| N11-007 | Front matter | 23 | \author{Anonymous Authors} | Front matter/references and technical metadata | PRESERVE_FORMAT |
| N11-008 | Front matter | 25 | \begin{abstract} Persistent viewer--creator relationships may compleme | Front matter/references and technical metadata | PRESERVE_FORMAT |
| N11-009 | Front matter | 29 | \begin{keyword} live-streaming recommendation \sep sequential recommen | Front matter/references and technical metadata | PRESERVE_FORMAT |
| N11-010 | Front matter | 33 | \end{frontmatter} | Front matter/references and technical metadata | PRESERVE_FORMAT |
| N11-011 | Introduction | 35 | \section{Introduction} | 1 Introduction | REWRITE_FOCUSED |
| N11-012 | Introduction | 37 | Sequential recommenders infer preferences from behavioral sequences, i | 1 Introduction | REWRITE_FOCUSED |
| N11-013 | Introduction | 39 | The answer must be comparative. A high-scoring memory-based recommende | 1 Introduction | REWRITE_FOCUSED |
| N11-014 | Introduction | 41 | Two features of live recommendation make this valuation especially inf | 1 Introduction | REWRITE_FOCUSED |
| N11-015 | Introduction | 43 | These considerations define one connected research problem: characteri | 1 Introduction | REWRITE_FOCUSED |
| N11-016 | Introduction | 45 | Across the held-out Twitch and M3 evaluations, predicted relative util | 1 Introduction | REWRITE_FOCUSED |
| N11-017 | Introduction | 47 | We make three connected empirical contributions, each tied to an obser | 1 Introduction | REWRITE_FOCUSED |
| N11-018 | Introduction | 54 | `fig:knowledge-value-chain` | 1 Introduction non-causal branching claim/evidence diagram | REDRAW_NO_FALSE_CAUSAL_CHAIN |
| N11-019 | Related Work | 77 | \section{Related Work} | 2 Related Work | CONSOLIDATE |
| N11-020 | Related Work / Sequential Recommendation and Relationship Knowledge | 79 | \subsection{Sequential Recommendation and Relationship Knowledge} | 2 Related Work | CONSOLIDATE |
| N11-021 | Related Work / Sequential Recommendation and Relationship Knowledge | 81 | Sequential models learn representations of evolving behavioral prefere | 2 Related Work | CONSOLIDATE |
| N11-022 | Related Work / Sequential Recommendation and Relationship Knowledge | 83 | The distinction is also relevant to memory-augmented recommendation. Z | 2 Related Work | CONSOLIDATE |
| N11-023 | Related Work / Learning to Defer and Adaptive Specialist Selection | 85 | \subsection{Learning to Defer and Adaptive Specialist Selection} | 2 Related Work | CONSOLIDATE |
| N11-024 | Related Work / Learning to Defer and Adaptive Specialist Selection | 87 | Learning-to-Defer studies when a prediction should be delegated to a c | 2 Related Work | CONSOLIDATE |
| N11-025 | Related Work / Learning to Defer and Adaptive Specialist Selection | 89 | Adaptive routing has also entered recommendation models directly. DS-F | 2 Related Work | CONSOLIDATE |
| N11-026 | Related Work / Learning to Defer and Adaptive Specialist Selection | 91 | Different selection scores test different information about the same d | 2 Related Work | CONSOLIDATE |
| N11-027 | Related Work / Live-Streaming Ranking and Candidate-Dependent Evaluation | 93 | \subsection{Live-Streaming Ranking and Candidate-Dependent Evaluation} | 2 Related Work | CONSOLIDATE |
| N11-028 | Related Work / Live-Streaming Ranking and Candidate-Dependent Evaluation | 95 | Live recommendation couples persistent viewer interests with time-vary | 2 Related Work | CONSOLIDATE |
| N11-029 | Related Work / Live-Streaming Ranking and Candidate-Dependent Evaluation | 97 | Candidate composition also changes the meaning of ranking metrics. Kri | 2 Related Work | CONSOLIDATE |
| N11-030 | Related Work / Live-Streaming Ranking and Candidate-Dependent Evaluation | 99 | Together, these literatures establish the distinct precedents for lear | 2 Related Work | CONSOLIDATE |
| N11-031 | Problem Formulation / Live-Streaming Ranking and Candidate-Dependent Evaluation | 101 | `sec:problem` | 3.1-3.3 Value and candidate definitions | MERGE_3_4 |
| N11-032 | Problem Formulation / Live-Streaming Ranking and Candidate-Dependent Evaluation | 104 | Let the value of a relationship-memory specialist be the change in eve | 3.1-3.3 Value and candidate definitions | MERGE_3_4 |
| N11-033 | Problem Formulation / Recommendation Setting and Event-Level Ranking Utility | 106 | `sec:event-utility` | 3.1-3.3 Value and candidate definitions | MERGE_3_4 |
| N11-034 | Problem Formulation / Recommendation Setting and Event-Level Ranking Utility | 109 | For user $u$, time $t$ and regime $r$, define the pre-outcome context  | 3.1-3.3 Value and candidate definitions | MERGE_3_4 |
| N11-035 | Problem Formulation / Recommendation Setting and Event-Level Ranking Utility | 111 | `eq:event-ndcg` | 3.1-3.3 Value and candidate definitions | MERGE_3_4 |
| N11-036 | Problem Formulation / Base-Relative Specialist Utility | 122 | `sec:relative-utility` | 3.1-3.3 Value and candidate definitions | MERGE_3_4 |
| N11-037 | Problem Formulation / Base-Relative Specialist Utility | 125 | `eq:delta-memory` | 3.1-3.3 Value and candidate definitions | MERGE_3_4 |
| N11-038 | Problem Formulation / Conditional Relative Utility | 132 | `sec:conditional-utility` | 3.3-3.4 Candidate-aligned conditional value | MERGE_3_4 |
| N11-039 | Problem Formulation / Conditional Relative Utility | 135 | `eq:eta` | 3.3-3.4 Candidate-aligned conditional value | MERGE_3_4 |
| N11-040 | Problem Formulation / Conditional Relative Utility | 143 | `eq:candidate-supervision-transfer` | 3.3-3.4 Candidate-aligned conditional value | MERGE_3_4 |
| N11-041 | Problem Formulation / Conditional Relative Utility | 151 | `eq:expected-selective-gain` | 3.3-3.4 Candidate-aligned conditional value | MERGE_3_4 |
| N11-042 | Problem Formulation / Selective Invocation and Invocation-Count Constraints | 160 | `sec:decision-rule` | 3.5 Invocation and eligibility policy | MERGE_3_4 |
| N11-043 | Problem Formulation / Selective Invocation and Invocation-Count Constraints | 163 | `eq:utility-threshold` | 3.5 Invocation and eligibility policy | MERGE_3_4 |
| N11-044 | Problem Formulation / Regime-Level Utility Decomposition | 172 | `sec:regime-decomposition` | 3.5 Diagnostic-only decomposition; S10 expanded | CONDENSE_SUPPLEMENT |
| N11-045 | Problem Formulation / Regime-Level Utility Decomposition | 175 | `eq:regime-decomposition` | 3.5 Diagnostic-only decomposition; S10 expanded | CONDENSE_SUPPLEMENT |
| N11-046 | Problem Formulation / Regime-Level Utility Decomposition | 184 | `sec:framework` | 3.5 Diagnostic-only decomposition; S10 expanded | CONDENSE_SUPPLEMENT |
| N11-047 | Base-Relative Evidence Valuation Framework / Regime-Level Utility Decomposition | 188 | The framework connects a trained sequential incumbent, an explicit fix | 3.5 Invocation and policy comparators | MERGE_3_4 |
| N11-048 | Base-Relative Evidence Valuation Framework / Regime-Level Utility Decomposition | 190 | `fig:framework` | 3.5 Selective knowledge-use architecture, online/offline separation | KEEP_EDIT_CAPTION |
| N11-049 | Base-Relative Evidence Valuation Framework / Strong Sequential Base Recommenders | 216 | `sec:framework-base` | 3.2 Fixed base and explicit Memory | MERGE_3_4 |
| N11-050 | Base-Relative Evidence Valuation Framework / Strong Sequential Base Recommenders | 219 | The Base represents the recommendation capability to which relationshi | 3.2 Fixed base and explicit Memory | MERGE_3_4 |
| N11-051 | Base-Relative Evidence Valuation Framework / Transparent Relationship-Memory Specialist | 221 | `sec:framework-memory` | 3.2 Fixed base and explicit Memory | MERGE_3_4 |
| N11-052 | Base-Relative Evidence Valuation Framework / Transparent Relationship-Memory Specialist | 224 | `eq:memory-scoring` | 3.2 Fixed base and explicit Memory | MERGE_3_4 |
| N11-053 | Base-Relative Evidence Valuation Framework / Transparent Relationship-Memory Specialist | 233 | These weights define the fixed specialist rather than a per-event trai | 3.2 Fixed base and explicit Memory | MERGE_3_4 |
| N11-054 | Base-Relative Evidence Valuation Framework / Base-Relative Relationship-Evidence States | 235 | `sec:framework-states` | 3.5 Brief diagnostic states and Supplement | CONDENSE_SUPPLEMENT |
| N11-055 | Base-Relative Evidence Valuation Framework / Base-Relative Relationship-Evidence States | 238 | `eq:diagnostic-states` | 3.5 Brief diagnostic states and Supplement | CONDENSE_SUPPLEMENT |
| N11-056 | Base-Relative Evidence Valuation Framework / Observable Features and Conditional Relative-Utility Estimation | 250 | `sec:framework-estimation` | 3.4 Decision-time observable features and estimator | MERGE_3_4 |
| N11-057 | Base-Relative Evidence Valuation Framework / Observable Features and Conditional Relative-Utility Estimation | 253 | The decision vector $Z$ combines historical relationship descriptors w | 3.4 Decision-time observable features and estimator | MERGE_3_4 |
| N11-058 | Base-Relative Evidence Valuation Framework / Observable Features and Conditional Relative-Utility Estimation | 255 | The Twitch implementation uses six history and eight Base-score descri | 3.4 Decision-time observable features and estimator | MERGE_3_4 |
| N11-059 | Base-Relative Evidence Valuation Framework / Specialist Selection and Comparator Policies | 257 | `sec:framework-controls` | 3.5 Invocation and policy comparators | MERGE_3_4 |
| N11-060 | Base-Relative Evidence Valuation Framework / Specialist Selection and Comparator Policies | 260 | At inference, the Base produces the default ranking and its observable | 3.5 Invocation and policy comparators | MERGE_3_4 |
| N11-061 | Base-Relative Evidence Valuation Framework / Specialist Selection and Comparator Policies | 262 | `sec:experimental-setup` | 3.5 Invocation and policy comparators | MERGE_3_4 |
| N11-062 | Experimental Setup / Specialist Selection and Comparator Policies | 266 | Table~\ref{tab:exp-datasets} defines the distinct ranked units, candid | 4.6 Implementation summary; Supplement exact settings | CONDENSE_SUPPLEMENT |
| N11-063 | Experimental Setup / Datasets and Prediction Tasks | 268 | `sec:exp-data` | 4.1 Dataset task and evidence-tier protocol | RESTRUCTURE |
| N11-064 | Experimental Setup / Datasets and Prediction Tasks | 271 | \paragraph{Twitch/LiveRec.} We use the availability-aware LiveRec prot | 4.1 Dataset task and evidence-tier protocol | RESTRUCTURE |
| N11-065 | Experimental Setup / Datasets and Prediction Tasks | 274 | \paragraph{Original KuaiLive.} We rank a time-bounded live \emph{room} | 4.1 Dataset task and evidence-tier protocol | RESTRUCTURE |
| N11-066 | Experimental Setup / Datasets and Prediction Tasks | 277 | \paragraph{KuaiLive-M3.} The M3 evaluation ranks persistent \texttt{au | 4.1 Dataset task and evidence-tier protocol | RESTRUCTURE |
| N11-067 | Experimental Setup / Datasets and Prediction Tasks | 280 | `tab:exp-datasets` | 4.1 Evidence tiers | REBUILD_IN_MAIN |
| N11-068 | Experimental Setup / Baselines and Compared Methods | 297 | `sec:exp-comparators` | 4.2 Rankers and policy comparator scope | RESTRUCTURE |
| N11-069 | Experimental Setup / Baselines and Compared Methods | 300 | Within every task, the two fixed scorers rank the same available candi | 4.2 Rankers and policy comparator scope | RESTRUCTURE |
| N11-070 | Experimental Setup / Baselines and Compared Methods | 302 | The original KuaiLive candidate analysis uses the same fixed Dual-ID B | 4.2 Rankers and policy comparator scope | RESTRUCTURE |
| N11-071 | Experimental Setup / Baselines and Compared Methods | 304 | M3 uses SASRec and GRU4Rec author-level Base families with three fitte | 4.2 Rankers and policy comparator scope | RESTRUCTURE |
| N11-072 | Experimental Setup / Baselines and Compared Methods | 306 | For M3, 12 available descriptors comprise five Base-score summaries (t | 4.2 Rankers and policy comparator scope | RESTRUCTURE |
| N11-073 | Experimental Setup / Baselines and Compared Methods | 308 | `tab:exp-methods` | Supplement Methods comparator table | MOVE_TO_SUPPLEMENT |
| N11-074 | Experimental Setup / Experimental Protocols | 326 | `sec:exp-freeze`, `sec:exp-regimes` | 4.3-4.5 Freeze, candidate, source-null protocols | RESTRUCTURE |
| N11-075 | Experimental Setup / Experimental Protocols | 330 | \paragraph{Training, out-of-fold estimation and policy freeze.} All in | 4.3-4.5 Freeze, candidate, source-null protocols | RESTRUCTURE |
| N11-076 | Experimental Setup / Experimental Protocols | 333 | Each of the six M3 Base checkpoints is selected on the common sampled- | 4.3-4.5 Freeze, candidate, source-null protocols | RESTRUCTURE |
| N11-077 | Experimental Setup / Experimental Protocols | 335 | The five M3 selection objectives consequently share a \emph{developmen | 4.3-4.5 Freeze, candidate, source-null protocols | RESTRUCTURE |
| N11-078 | Experimental Setup / Experimental Protocols | 337 | \paragraph{Forward-time information boundary.} M3 evaluation proceeds  | 4.3-4.5 Freeze, candidate, source-null protocols | RESTRUCTURE |
| N11-079 | Experimental Setup / Experimental Protocols | 340 | `eq:paired-regime-shift`, `eq:factorial-allocations` | 4.3-4.5 Freeze, candidate, source-null protocols | RESTRUCTURE |
| N11-080 | Experimental Setup / Experimental Protocols | 357 | \paragraph{Exploratory candidate-supervision and relationship-source c | 4.3-4.5 Freeze, candidate, source-null protocols | RESTRUCTURE |
| N11-081 | Experimental Setup / Experimental Protocols | 360 | \paragraph{Time-preserving relationship-identity control.} To distingu | 4.3-4.5 Freeze, candidate, source-null protocols | RESTRUCTURE |
| N11-082 | Experimental Setup / Experimental Protocols | 363 | \paragraph{Additional same-period, pre-outcome-frozen target evaluatio | 4.3-4.5 Freeze, candidate, source-null protocols | RESTRUCTURE |
| N11-083 | Experimental Setup / Experimental Protocols | 366 | The nested historical comparison retains the original Full Memory rank | 4.3-4.5 Freeze, candidate, source-null protocols | RESTRUCTURE |
| N11-084 | Experimental Setup / Evaluation Metrics and Statistical Analysis | 368 | `sec:exp-statistics` | 4.4 Evaluation weights and inference | RESTRUCTURE |
| N11-085 | Experimental Setup / Evaluation Metrics and Statistical Analysis | 371 | The primary endpoint is event-level NDCG@10 (Eq.~\eqref{eq:event-ndcg} | 4.4 Evaluation weights and inference | RESTRUCTURE |
| N11-086 | Experimental Setup / Evaluation Metrics and Statistical Analysis | 373 | Twitch TEST confidence intervals are based on 5,000 user-paired bootst | 4.4 Evaluation weights and inference | RESTRUCTURE |
| N11-087 | Experimental Setup / Implementation Details | 375 | `sec:exp-implementation` | 4.6 Implementation summary; Supplement exact settings | CONDENSE_SUPPLEMENT |
| N11-088 | Experimental Setup / Implementation Details | 378 | The original KuaiLive room/creator Base uses 64-dimensional ReChorus S | 4.6 Implementation summary; Supplement exact settings | CONDENSE_SUPPLEMENT |
| N11-089 | Experimental Results / Implementation Details | 380 | `sec:results` | 5.4 Operational conditions and measured costs | CONDENSE |
| N11-090 | Experimental Results / Implementation Details | 383 | The results proceed from the incremental value of fixed relationship e | 5.4 Operational conditions and measured costs | CONDENSE |
| N11-091 | Experimental Results / Heterogeneous Utility of Relationship Memory | 385 | `sec:results-heterogeneity` | 5.1 RQ1 history and candidates | RESTRUCTURE |
| N11-092 | Experimental Results / Heterogeneous Utility of Relationship Memory | 388 | The ranking contribution of relationship memory is heterogeneous rathe | 5.1 RQ1 history and candidates | RESTRUCTURE |
| N11-093 | Experimental Results / Heterogeneous Utility of Relationship Memory | 390 | Figure~\ref{fig:results-evidence-states} and Table~\ref{tab:results-ev | 5.1 RQ1 history and candidates | RESTRUCTURE |
| N11-094 | Experimental Results / Heterogeneous Utility of Relationship Memory | 392 | In the distinct KuaiLive-M3 author-ranking TEST, Memory reaches NDCG@1 | 5.1 RQ1 history and candidates | RESTRUCTURE |
| N11-095 | Experimental Results / Heterogeneous Utility of Relationship Memory | 394 | `fig:results-evidence-states` | Supplement detailed Twitch state plot (subject to RQ1 density review) | REVIEW_MOVE_TO_SUPPLEMENT |
| N11-096 | Experimental Results / Heterogeneous Utility of Relationship Memory | 426 | `tab:results-evidence-states` | Supplement Twitch outcome-state details | MOVE_TO_SUPPLEMENT |
| N11-097 | Experimental Results / Heterogeneous Utility of Relationship Memory | 443 | `sec:results-regimes` | 5.1 RQ1 history and candidates | RESTRUCTURE |
| N11-098 | Experimental Results / Candidate-Regime Dependence of Relative Utility | 447 | Because ranking utility is defined over competing alternatives, the ca | 5.1 RQ1 history and candidates | RESTRUCTURE |
| N11-099 | Experimental Results / Candidate-Regime Dependence of Relative Utility | 449 | The crossed candidate-membership and Base score-normalization referenc | 5.1 RQ1 history and candidates | RESTRUCTURE |
| N11-100 | Experimental Results / Candidate-Regime Dependence of Relative Utility | 451 | `tab:results-factorial` | 5.1 RQ1 candidate regime | KEEP_MAIN |
| N11-101 | Experimental Results / Candidate-Regime Dependence of Relative Utility | 467 | The reversal remains directionally stable across three separately trai | 5.1 RQ1 history and candidates | RESTRUCTURE |
| N11-102 | Experimental Results / Candidate-Regime Dependence of Relative Utility | 469 | The matched M3 author-ranking development analysis tests the decision  | 5.1 RQ1 history and candidates | RESTRUCTURE |
| N11-103 | Experimental Results / Candidate-Regime Dependence of Relative Utility | 471 | `tab:results-m3-dev-regime-transfer` | Supplement DEV candidate transfer details | MOVE_TO_SUPPLEMENT |
| N11-104 | Experimental Results / Decision Value of Predicting Relative Utility | 492 | `sec:results-decision` | 5.2 RQ2 aligned supervision and selection | RESTRUCTURE |
| N11-105 | Experimental Results / Decision Value of Predicting Relative Utility | 495 | The candidate comparisons motivate a consequential test: whether a sel | 5.2 RQ2 aligned supervision and selection | RESTRUCTURE |
| N11-106 | Experimental Results / Decision Value of Predicting Relative Utility | 497 | Memory contributes $+0.05136$ NDCG@10 on Utility-selected Twitch reque | 5.2 RQ2 aligned supervision and selection | RESTRUCTURE |
| N11-107 | Experimental Results / Decision Value of Predicting Relative Utility | 499 | `tab:results-twitch-policy` | 5.2 RQ2 compact Twitch evidence; full table in supplement | CONDENSE_MAIN_DETAIL_SUPPLEMENT |
| N11-108 | Experimental Results / Decision Value of Predicting Relative Utility | 518 | On the prospectively frozen KuaiLive-M3 full-active author TEST, Utili | 5.2 RQ2 aligned supervision and selection | RESTRUCTURE |
| N11-109 | Experimental Results / Decision Value of Predicting Relative Utility | 520 | This advantage extends across the three independently trained seeds of | 5.2 RQ2 aligned supervision and selection | RESTRUCTURE |
| N11-110 | Experimental Results / Decision Value of Predicting Relative Utility | 522 | For the primary SASRec fit, the predeclared Utility comparisons are ag | 5.2 RQ2 aligned supervision and selection | RESTRUCTURE |
| N11-111 | Experimental Results / Decision Value of Predicting Relative Utility | 524 | `tab:results-m3-policy` | 5.2 RQ2 initial M3 frozen choice | KEEP_MAIN |
| N11-112 | Experimental Results / Decision Value of Predicting Relative Utility | 545 | `tab:results-m3-robustness` | 5.2 RQ2 six-fit compact robust summary | CONDENSE_MAIN_DETAIL_SUPPLEMENT |
| N11-113 | Experimental Results / Decision Value of Predicting Relative Utility | 565 | For the primary M3 fit, random uniform allocation at $30\%$ calls has  | 5.2 RQ2 aligned supervision and selection | RESTRUCTURE |
| N11-114 | Experimental Results / Decision Value of Predicting Relative Utility | 567 | The additional 30,000-target same-period evaluation tests the conseque | 5.2 RQ2 aligned supervision and selection | RESTRUCTURE |
| N11-115 | Experimental Results / Decision Value of Predicting Relative Utility | 569 | `tab:results-m3-b4a-supervision` | 5.2 RQ2 frozen 30000 additional-target H1 | KEEP_MAIN |
| N11-116 | Experimental Results / Decision Value of Predicting Relative Utility | 585 | `sec:results-robustness` | 5.2 RQ2 aligned supervision and selection | RESTRUCTURE |
| N11-117 | Experimental Results / Relationship Sources and Observable Signals | 589 | The source of historical knowledge is also relevant to its measured ra | 5.3 RQ3 authentic history and source controls | RESTRUCTURE |
| N11-118 | Experimental Results / Relationship Sources and Observable Signals | 591 | On 1,024 stratified M3 DEV requests, valid historical-author nulls ret | 5.3 RQ3 authentic history and source controls | RESTRUCTURE |
| N11-119 | Experimental Results / Relationship Sources and Observable Signals | 593 | `tab:results-m3-dev-source` | Supplement mechanism DEV source components | MOVE_TO_SUPPLEMENT |
| N11-120 | Experimental Results / Relationship Sources and Observable Signals | 612 | `tab:results-m3-additional-relation-identity` | 5.3 RQ3 fixed-candidate 4096 H2 | KEEP_MAIN |
| N11-121 | Experimental Results / Relationship Sources and Observable Signals | 632 | In the nested 4,096-target M3 evaluation, authentic Full Memory exceed | 5.3 RQ3 authentic history and source controls | RESTRUCTURE |
| N11-122 | Experimental Results / Relationship Sources and Observable Signals | 634 | The feasibility of predictive selection depends on pre-outcome descrip | 5.3 RQ3 authentic history and source controls | RESTRUCTURE |
| N11-123 | Experimental Results / Relationship Sources and Observable Signals | 636 | `tab:results-feature-ablation` | Supplement Twitch DEV features | MOVE_TO_SUPPLEMENT |
| N11-124 | Experimental Results / Relationship Sources and Observable Signals | 653 | Additional DEV-only diagnostics indicate how that relative value varie | 5.3 RQ3 authentic history and source controls | RESTRUCTURE |
| N11-125 | Experimental Results / Relationship Sources and Observable Signals | 655 | `sec:results-efficiency` | 5.3 RQ3 authentic history and source controls | RESTRUCTURE |
| N11-126 | Experimental Results / Invocation Constraints and Measured Scoring Cost | 659 | The M3 Utility rules realize $27.72$--$29.21\%$ Memory calls on TEST a | 5.4 Operational conditions and measured costs | CONDENSE |
| N11-127 | Experimental Results / Invocation Constraints and Measured Scoring Cost | 661 | In a matched, exploratory nested M3 DEV sensitivity analysis, raising  | 5.4 Operational conditions and measured costs | CONDENSE |
| N11-128 | Experimental Results / Invocation Constraints and Measured Scoring Cost | 663 | A first warmed RTX 3090 DEV replay on 256 M3 requests found a faster u | 5.4 Operational conditions and measured costs | CONDENSE |
| N11-129 | Experimental Results / Invocation Constraints and Measured Scoring Cost | 667 | A second, counterbalanced DEV measurement repeats the same 256 full-ac | 5.4 Operational conditions and measured costs | CONDENSE |
| N11-130 | Experimental Results / Invocation Constraints and Measured Scoring Cost | 669 | `tab:results-n10-cost` | 5.4 Operating conditions short cost summary; full S10.17 | CONDENSE_MAIN_DETAIL_SUPPLEMENT |
| N11-131 | Experimental Results / Invocation Constraints and Measured Scoring Cost | 687 | The selector invokes Memory on 80 of 256 distinct DEV requests (31.25\ | 5.4 Operational conditions and measured costs | CONDENSE |
| N11-132 | Discussion / Invocation Constraints and Measured Scoring Cost | 689 | `sec:discussion` | 6.3 Source validity, policy and transfer conditions | CONSOLIDATE |
| N11-133 | Discussion / The Relative Value of Relationship Knowledge | 692 | `sec:discussion-operational-value` | 6.1 Knowledge system contribution | CONSOLIDATE |
| N11-134 | Discussion / The Relative Value of Relationship Knowledge | 695 | The central object of this study is the incremental utility of an expl | 6.1 Knowledge system contribution | CONSOLIDATE |
| N11-135 | Discussion / The Relative Value of Relationship Knowledge | 697 | This contribution complements prior work on scene-conditioned memory a | 6.1 Knowledge system contribution | CONSOLIDATE |
| N11-136 | Discussion / Candidate Context Defines the Value Being Predicted | 699 | `sec:discussion-candidate-regimes` | 6.2 Candidate regime and evaluation meaning | CONSOLIDATE |
| N11-137 | Discussion / Candidate Context Defines the Value Being Predicted | 702 | A relative-ranking utility label is not intrinsic to the knowledge sou | 6.2 Candidate regime and evaluation meaning | CONSOLIDATE |
| N11-138 | Discussion / Candidate Context Defines the Value Being Predicted | 704 | The historical-source controls distinguish that supervision effect fro | 6.2 Candidate regime and evaluation meaning | CONSOLIDATE |
| N11-139 | Discussion / Predicted Marginal Value as a Selection Signal | 706 | `sec:discussion-selective-decisions` | 6.3 Source validity, policy and transfer conditions | CONSOLIDATE |
| N11-140 | Discussion / Predicted Marginal Value as a Selection Signal | 709 | Conditional relative utility links evidence valuation to a testable ch | 6.3 Source validity, policy and transfer conditions | CONSOLIDATE |
| N11-141 | Discussion / Predicted Marginal Value as a Selection Signal | 711 | The decision target should not be confused with a new estimation princ | 6.3 Source validity, policy and transfer conditions | CONSOLIDATE |
| N11-142 | Discussion / Invocation Allocation and System Cost Are Distinct | 713 | `sec:discussion-validity` | 6.3 Source validity, policy and transfer conditions | CONSOLIDATE |
| N11-143 | Discussion / Invocation Allocation and System Cost Are Distinct | 716 | Choosing fewer Memory invocations is not the same as reducing latency  | 6.3 Source validity, policy and transfer conditions | CONSOLIDATE |
| N11-144 | Discussion / Invocation Allocation and System Cost Are Distinct | 718 | Thus the positive selection finding is a \emph{conditional allocation} | 6.3 Source validity, policy and transfer conditions | CONSOLIDATE |
| N11-145 | Discussion / Transferability and Implications for Knowledge-Based Recommendation | 720 | `sec:discussion-implications` | 6.3 Source validity, policy and transfer conditions | CONSOLIDATE |
| N11-146 | Discussion / Transferability and Implications for Knowledge-Based Recommendation | 723 | The experiments provide complementary, not interchangeable, evidence.  | 6.3 Source validity, policy and transfer conditions | CONSOLIDATE |
| N11-147 | Discussion / Transferability and Implications for Knowledge-Based Recommendation | 725 | For knowledge-enhanced recommendation, the resulting evaluation discip | 6.3 Source validity, policy and transfer conditions | CONSOLIDATE |
| N11-148 | Conclusion / Transferability and Implications for Knowledge-Based Recommendation | 727 | `sec:conclusion` | 7 Conclusion | REWRITE_POSITIVE |
| N11-149 | Conclusion / Transferability and Implications for Knowledge-Based Recommendation | 730 | A fixed relationship-memory ranker has no context-free incremental val | 7 Conclusion | REWRITE_POSITIVE |
| N11-150 | Conclusion / Transferability and Implications for Knowledge-Based Recommendation | 732 | The research contribution is a reproducible framework for \emph{evalua | 7 Conclusion | REWRITE_POSITIVE |
| N11-151 | Conclusion / Transferability and Implications for Knowledge-Based Recommendation | 734 |  \bibliographystyle{elsarticle-num} \bibliography{kbs_references} | 7 Conclusion | REWRITE_POSITIVE |
| N11-152 | Conclusion / Transferability and Implications for Knowledge-Based Recommendation | 738 | \end{document} | 7 Conclusion | REWRITE_POSITIVE |

## 必须完成的表格/图形落地门禁

- `MOVE_TO_SUPPLEMENT`及`CONDENSE_MAIN_DETAIL_SUPPLEMENT`不能简单删除：须在原S10相应小节保留完整表格、数值和原估计协议，同时在新主文增加精准引用。
- 无法自动确定价值的某些长式补充图，只能在N12-1证据分配审核后迁移，不允许暂存丢失。
- 图示中P3为知识来源有效性旁路检验，不用P1→P2→P3单向因果箭头。
- 源块FNV32只作编辑身份识别；用于冻结证据的Git SHA必须与N11仓库实际对象一致。
- 主稿标题、作者声明和任何私有原始数据不属于编辑重构时可以自动替换的研究事实。
