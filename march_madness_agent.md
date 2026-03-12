# March Madness Bracket Predictor Agent Guide (R)

## Agent Instructions
1. Read this for mission, principles, quickstart, and pitfalls.
2. Parse `march_madness_agent.json` for structured data, feature definitions, model configs, validation cases, and code examples. Do not parse this Markdown.
3. This agent is **R-first** — all code, packages, and workflows use R and the tidyverse/tidymodels ecosystem.
4. This agent is **complex** — use all sections including Core Concepts.

---

## Mission (core)

**What it does**: Predicts NCAA March Madness tournament outcomes game-by-game using machine learning in R, producing an optimized 63-game bracket with win probabilities for every matchup.

**Why it exists**: Bracket prediction is notoriously hard — a #1 seed losing to a #16 seed is rare but real. Pure intuition fails; pure stats miss momentum. This agent fuses historical tournament data, team efficiency metrics, and game-context features inside R's tidymodels ecosystem to outperform both human pickers and naive seed-based baselines.

**Who uses it**: R-native data scientists, sports analysts, and hobbyists building ML-powered bracket predictions for ESPN/Yahoo/office pools or academic research.

**Primary stack**: R + tidyverse + tidymodels + xgboost + probably (calibration) + future (parallelism)

**Example**: "Given 2025 team stats, seed matchups, and KenPom ratings in a CSV, fit an XGBoost workflow with tidymodels and simulate the full 64-team bracket with 10,000 Monte Carlo iterations."

---

## Agent Quickstart (core)

1. **[Load Data]**: Pull historical tournament results + current season team stats into tibbles
   - Sources: `sports-reference.com`, KenPom, ESPN BPI, Kaggle NCAA datasets — see `march_madness_agent.json` → `primary_data.sources`
   - R package: `hoopR` for live NCAA data, `readr`/`readxl` for CSVs

2. **[Engineer Features]**: Build per-matchup feature tibble using `dplyr` mutate + joins
   - Key features: seed differential, adjusted efficiency margin delta, SOS delta, recent form — see JSON → `feature_engineering`

3. **[Train Model]**: Fit tidymodels workflow with XGBoost + Logistic Regression ensemble on 2000–2024 data
   - Use `tune_grid()` + `vfold_cv()` for tuning; see JSON → `implementation.models`

4. **[Simulate Bracket]**: Run round-by-round Monte Carlo simulation using `purrr::map()` + `future`
   - Accounts for path dependency — who you play depends on who won earlier rounds

5. **[Validate]**: Check Brier score < 0.22, log-loss < 0.65, upset detection rate > 40%
   - Use `yardstick::brier_class()`, `yardstick::mn_log_loss()` — see JSON → `validation`

6. **[Output]**: Bracket tibble with win probabilities, predicted champion, Final Four, and upset alerts

For R code snippets, feature lists, and model configs, see `march_madness_agent.json`.

---

## File Organization: JSON vs MD (core)

### This Markdown File (.md) Contains:
- Mission and purpose
- Design philosophy and principles
- Core concepts (why features matter, how upsets happen)
- Common pitfalls explained narratively
- Resources and R package guidance

### The JSON File (.json) Contains:
- Full feature list with descriptions and R column types
- Model hyperparameters and tidymodels workflow configs
- Data source schemas and loading patterns
- Validation checklists and historical benchmarks
- R code snippets for data loading, feature engineering, model training, bracket simulation
- Round-by-round upset rate tables

**Rule of Thumb**: If the agent needs to parse it → JSON. If you need to understand *why* a feature matters → MD.

---

## Key Principles (core)

### 1. Matchup-Relative Features Over Absolute Stats
**Description**: Always express features as differences between the two teams, not raw team values.

**Why**: A team with 115 offensive efficiency looks great — until they face a defense rated 118. The *gap* is what determines outcomes.

**How**: Use `dplyr::mutate()` to compute `team_a_stat - team_b_stat` for every efficiency metric. The model sees deltas, not raw values. See JSON → `feature_engineering.matchup_delta_features`.

### 2. Seed Is a Signal, Not a Sentence
**Description**: Seeds encode committee wisdom but are noisy proxies. Never let seed alone dominate the model.

**Why**: Seeds correlate with quality but are compressed to 1–16. Two teams seeded #5 can have wildly different efficiency margins and SOS. Cinderella runs happen precisely when seed understates a team's true quality.

**How**: Include `seed_delta` as a feature alongside efficiency metrics, momentum, and coaching tenure. See JSON → `feature_engineering.seed_features`.

### 3. Tournament Context Is Different from Regular Season
**Description**: Regular season stats require tournament-specific adjustments.

**Why**: Pace slows in tournament games (higher stakes → more deliberate offense). Home court disappears. Teams with high SOS in major conferences are better calibrated than mid-majors with inflated records.

**How**: Use KenPom's pace-adjusted AdjO/AdjD, weight recent 10-game form more heavily than full-season, and include conference strength as a feature.

### 4. Simulate, Don't Just Predict
**Description**: A bracket isn't 63 independent games — it's a path-dependent sequence. Use Monte Carlo simulation via `purrr`.

**Why**: Optimizing each game in isolation misses chalk scenarios and dark-horse paths (an upset in round 1 changes who you face in round 2).

**How**: Run 10,000+ Monte Carlo simulations over the full bracket using `purrr::rerun()` or `future_map()`. Track championship probability per team, not just next-game win probability.

### 5. Calibrate Probabilities, Not Just Accuracy
**Description**: Aim for well-calibrated win probabilities, not just high accuracy. Use the `probably` package.

**Why**: Bracket scoring rewards confidence. A well-calibrated model lets you make strategic high-leverage upset picks.

**How**: Use `probably::cal_estimate_isotonic()` post-training. Evaluate with `yardstick::brier_class()` and calibration plots from `probably::cal_plot_breaks()`.

---

## Core Concepts (optional for complex agents)

### How Upsets Actually Happen
March Madness upsets aren't random — they cluster around specific conditions:
- **Pace mismatch**: Slow-paced mid-majors neutralize high-powered offenses by reducing possessions
- **Three-point variance**: Teams that live/die by the arc have high game-to-game variance; in single-elimination, variance favors underdogs
- **Coaching experience**: First-time tournament coaches vs. veterans with 10+ tournament games
- **Rest/travel**: Teams that won their conference tournament in exhausting fashion vs. teams that clinched early and rested

The agent captures these via pace_delta, three_pt_rate_delta, coach_exp_delta, and days_rest_delta features.

### Why KenPom Metrics Are the Gold Standard
Ken Pomeroy's adjusted efficiency metrics (AdjO, AdjD, AdjEM, AdjT) control for pace and opponent strength. They predict tournament outcomes better than raw points-per-game because:
1. They're pace-neutral
2. They adjust for strength of schedule
3. They've been validated over 20+ tournament cycles

`AdjEM = AdjO - AdjD` is the single strongest individual predictor of tournament outcomes.

### R Ecosystem for This Problem
The R sports analytics ecosystem has matured significantly:
- **`hoopR`**: Live NCAA basketball data via ESPN APIs — current season stats, game-by-game logs
- **`tidymodels`**: End-to-end ML workflow (recipes + parsnip + workflows + tune + yardstick)
- **`xgboost`** (via parsnip `boost_tree()`): Primary model engine
- **`probably`**: Probability calibration, calibration plots
- **`future` + `furrr`**: Parallel Monte Carlo simulation
- **Kaggle NCAA dataset**: Pre-cleaned historical tournament data, easily imported with `readr`

### Round-Specific Dynamics
- **Round of 64**: 12-over-5 seeds upset ~35% of the time; 11-over-6 ~37%; 8-vs-9 is ~50/50
- **Round of 32**: Variance increases; fatigue sets in
- **Sweet 16+**: Experience and coaching matter most; defensive efficiency becomes primary predictor

See `march_madness_agent.json` → `domain_specific_patterns.round_dynamics` for full upset rate tables.

---

## How to Use This Agent (core)

### Prerequisites
```r
# Install required packages
install.packages(c(
  "tidyverse", "tidymodels", "xgboost", "probably",
  "future", "furrr", "hoopR", "vip", "ggplot2"
))
# hoopR for live NCAA data
remotes::install_github("sportsdataverse/hoopR")
```

### Basic Usage

**Step 1: Load and prepare data**
```r
library(tidyverse)
library(tidymodels)
library(hoopR)

# Load historical tournament results from Kaggle dataset
tourney_results <- read_csv("data/MNCAATourneyDetailedResults.csv")
team_stats      <- read_csv("data/kenpom_2000_2024.csv")

# Or use hoopR for current season
current_teams <- hoopR::load_mbb_team_box(seasons = 2025)
```

**Step 2: Engineer matchup features**
```r
source("R/feature_engineering.R")  # contains build_matchup_features()

matchup_df <- tourney_results |>
  left_join(team_stats, by = c("WTeamID" = "team_id", "Season" = "season")) |>
  left_join(team_stats, by = c("LTeamID" = "team_id", "Season" = "season"),
            suffix = c("_a", "_b")) |>
  mutate(
    adj_em_delta      = adj_em_a - adj_em_b,
    adj_o_delta       = adj_o_a  - adj_o_b,
    adj_d_delta       = adj_d_b  - adj_d_a,   # flipped: lower = better D
    pace_delta        = adj_t_a  - adj_t_b,
    sos_delta         = sos_a    - sos_b,
    seed_delta        = seed_b   - seed_a,
    recent_form_delta = form_a   - form_b,
    team_a_wins       = 1L
  )
```

**Step 3: Build and train tidymodels workflow**
```r
source("R/model.R")  # contains build_workflow(), tune_workflow()

set.seed(42)
splits <- initial_time_split(matchup_df, prop = 0.85)  # temporal split

wf <- build_workflow()   # recipe + XGBoost spec
tuned <- tune_workflow(wf, training(splits))
final_fit <- fit_best(tuned, training(splits))
```

**Step 4: Simulate bracket**
```r
source("R/simulation.R")  # contains simulate_bracket()

bracket_2025 <- read_csv("data/2025_tournament_teams.csv")
results <- simulate_bracket(
  teams    = bracket_2025,
  model    = final_fit,
  team_stats = current_teams,
  n_sim    = 10000
)

results$champion_probs |> arrange(desc(prob)) |> head(10)
```

**Step 5: Verify output**
- Check `results$brier_score < 0.22`
- Review `results$upset_alerts` for high-value first-round picks
- See JSON `validation.success_criteria`

---

## Common Pitfalls and Solutions (core)

### 1. Using Raw Season Stats Instead of Adjusted Metrics

**Problem**: Model trained on raw PPG/RPG underperforms a seed-only baseline.

**Why it happens**: Raw stats conflate pace and opponent strength.

**Solution**: Always use KenPom AdjO/AdjD/AdjEM, or BPI equivalent.

```r
# ❌ Wrong
matchup_df <- matchup_df |> mutate(off_rating = ppg_a)

# ✅ Correct — pace-adjusted, opponent-adjusted delta
matchup_df <- matchup_df |>
  mutate(
    adj_em_delta = adj_em_a - adj_em_b,
    adj_o_delta  = adj_o_a  - adj_o_b
  )
```

### 2. Using `initial_split()` Instead of `initial_time_split()`

**Problem**: Model achieves suspiciously high accuracy (>75%) — classic data leakage.

**Why it happens**: `initial_split()` randomly shuffles rows, mixing future seasons into training. A model trained on 2024 data that "predicts" 2022 games isn't predicting — it's cheating.

**Solution**: Always use `rsample::initial_time_split()` or manually filter by year for train/val splits.

```r
# ❌ Wrong — random split leaks future data
splits <- initial_split(matchup_df, prop = 0.8)

# ✅ Correct — temporal split
splits <- matchup_df |>
  mutate(split = if_else(season <= 2021, "train", "test")) |>
  # or:
  initial_time_split(prop = 0.85)
```

### 3. Forgetting `step_normalize()` Before Logistic Regression

**Problem**: Logistic regression predictions cluster near 0.5; XGBoost alone carries the ensemble.

**Why it happens**: Logistic regression is sensitive to feature scale. `adj_em_delta` ranges ~(-30, 30) while `is_classic_upset` is 0/1.

**Solution**: Add `step_normalize(all_numeric_predictors())` in the recipe, scoped to the logistic regression model via a model-specific recipe or branch workflow.

```r
# ✅ Correct recipe
rec <- recipe(team_a_wins ~ ., data = train_df) |>
  step_normalize(all_numeric_predictors()) |>
  step_dummy(all_nominal_predictors())
```

### 4. Ignoring Path Dependency in Bracket Simulation

**Problem**: You predict 63 games independently, producing an internally inconsistent bracket.

**Solution**: Simulate rounds sequentially. In R, use `purrr::reduce()` over rounds, passing survivors forward.

```r
# ✅ Correct: reduce over rounds
simulate_single <- function(teams, model, stats) {
  purrr::reduce(1:6, function(survivors, round_num) {
    # pair up teams, predict each game, return winners
    predict_round(survivors, model, stats, round_num)
  }, .init = teams)
}
```

### 5. Including 2021 Bubble Tournament Without a Flag

**Problem**: Model behaves erratically on recent validation years.

**Why it happens**: 2021 was a controlled-environment tournament with no fans — dramatically different pace, variance, and performance patterns.

**Solution**: Add `is_bubble_year` as a binary feature, or exclude 2021 from training.

```r
matchup_df <- matchup_df |>
  mutate(is_bubble_year = as.integer(season == 2021))
# or simply:
matchup_df <- matchup_df |> filter(season != 2021)
```

---

## Examples (core)

### Example 1: Predict a Single Matchup

**Scenario**: #1 seed Houston vs. #8 seed Utah State, Round of 32.

```r
library(tidymodels)

new_game <- tibble(
  adj_em_delta      =  9.3,
  adj_o_delta       =  2.9,
  adj_d_delta       =  6.4,
  pace_delta        = -2.7,
  sos_delta         =  2.8,
  seed_delta        =  7L,
  three_pt_rate_delta = 0.02,
  recent_form_delta =  0.1,
  round             =  2L
)

predict(final_fit, new_game, type = "prob")
# .pred_1 = Houston win probability (~0.74)
```

### Example 2: Cinderella Detection

**Scenario**: Find which underdogs have >35% upset probability in Round 1.

```r
round1_games |>
  mutate(
    pred    = map2(team_a_stats, team_b_stats, ~predict_game(.x, .y, round = 1, model = final_fit)),
    prob_upset = map_dbl(pred, ~1 - .x$.pred_1)
  ) |>
  filter(prob_upset > 0.35) |>
  arrange(desc(prob_upset)) |>
  select(matchup, prob_upset)
```

### Example 3: Parallel Monte Carlo Simulation

```r
library(furrr)
plan(multisession, workers = 4)

sim_results <- future_map(
  seq_len(10000),
  ~simulate_single_bracket(bracket_teams, final_fit, team_stats_2025),
  .options = furrr_options(seed = TRUE)
)

champion_probs <- sim_results |>
  map_chr("champion") |>
  table() |>
  as_tibble() |>
  rename(team = 1, n = nn) |>
  mutate(prob = n / 10000) |>
  arrange(desc(prob))
```

---

## Validation and Testing (core)

### Quick Validation
```r
library(yardstick)

# On hold-out years 2022-2024
preds <- augment(final_fit, test_df)

# Brier score (lower is better; beat 0.24 seed-only baseline)
brier_class(preds, truth = team_a_wins, .pred_1)

# Log loss
mn_log_loss(preds, truth = team_a_wins, .pred_1)

# Calibration plot
library(probably)
cal_plot_breaks(preds, truth = team_a_wins, .pred_1)
```

### Targets
| Metric | Target | Baseline |
|--------|--------|----------|
| Brier score | < 0.22 | Seed-only ~0.24 |
| Log-loss | < 0.65 | Random 50/50 ~0.69 |
| Upset recall | > 40% | — |
| Cal. error (MAE) | < 0.05 | — |

Full checklist and benchmark comparisons in `march_madness_agent.json` → `validation`.

---

## Performance Considerations (optional)

- Feature engineering on 25 years × ~63 games: <1s with `dplyr`
- XGBoost training via tidymodels on ~1,600 games: <15s
- Monte Carlo simulation (10,000 iterations) single-threaded: ~10–20s; with `furrr` (4 cores): ~4–6s
- For real-time tournament updates: cache team feature tibbles, recompute only matchup deltas

---

## Resources and References

### Agent Files
- **`march_madness_agent.json`**: Feature definitions, R model configs, code snippets, validation checklists
- **`R/feature_engineering.R`**: Reference feature-building functions
- **`R/model.R`**: tidymodels workflow builder + tuner
- **`R/simulation.R`**: Monte Carlo bracket simulator

### R Packages
| Package | Purpose |
|---------|---------|
| `hoopR` | Live NCAA basketball data (ESPN API) |
| `tidyverse` | Data wrangling + viz |
| `tidymodels` | ML workflows (recipes, parsnip, tune, yardstick) |
| `xgboost` | Gradient boosting engine (via parsnip) |
| `probably` | Probability calibration |
| `furrr` + `future` | Parallel Monte Carlo |
| `vip` | Variable importance plots |
| `ggplot2` | Bracket visualization |

### Data Sources
- [Sports Reference College Basketball](https://www.sports-reference.com/cbb/) — historical results
- [KenPom](https://kenpom.com/) — gold standard adjusted efficiency metrics
- [Kaggle: NCAA March Madness datasets](https://www.kaggle.com/competitions/march-machine-learning-mania-2024) — clean historical data
- [ESPN BPI](https://www.espn.com/mens-college-basketball/bpi) — free alternative to KenPom
- [hoopR docs](https://hoopr.sportsdataverse.org/) — R package for live NCAA data

### Community Resources
- [Kaggle March Machine Learning Mania notebooks](https://www.kaggle.com/competitions/march-machine-learning-mania-2024/code) — annual competition, many R notebooks
- [Sports Data Verse](https://www.sportsdataverse.org/) — R sports analytics ecosystem (hoopR, cfbfastR)

---

## Quick Reference Card

| Aspect | Value |
|--------|-------|
| **Purpose** | Predict NCAA tournament bracket via ML in R |
| **Input** | KenPom/BPI team stats CSV, seeds, historical results |
| **Output** | Win prob tibble, bracket predictions, upset alerts |
| **Language** | R |
| **Key Packages** | tidymodels, xgboost, probably, furrr, hoopR |
| **Model** | XGBoost (0.65) + LogReg (0.35) ensemble, isotonic calibration |
| **Simulation** | Monte Carlo, 10k iterations, parallel via furrr |
| **Key Metric** | Brier score < 0.22 (beats seed-only ~0.24) |
| **#1 Pitfall** | `initial_split()` instead of `initial_time_split()` → data leakage |
| **#2 Pitfall** | Raw PPG instead of KenPom AdjEM deltas |
