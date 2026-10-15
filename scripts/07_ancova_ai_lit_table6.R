############################################################
##  NCAL-2026-1259 : EFL AI Writing Study (R replication)  ##
##  Script : 07 - ANCOVA - AI literacy (Table 6)
##  Mirrors the Python pipeline; runs with base R,
##  and uses tidyverse/car/emmeans/ggplot2 when available.
############################################################

## ---- Robust data path resolution ------------------------------------
find_data <- function() {
  candidates <- c("data/raw/Hypothetical_EFL_AI_Study_Data.csv",
                  "Hypothetical_EFL_AI_Study_Data.csv",
                  "/mnt/data/Hypothetical_EFL_AI_Study_Data.csv",
                  "data/Hypothetical_EFL_AI_Study_Data.csv")
  hit <- candidates[file.exists(candidates)]
  if (length(hit) == 0) stop("Data file not found in any known path.")
  hit[1]
}

## ---- Optional package loader -----------------------------------------
need <- function(pkgs) {
  for (p in pkgs) {
    if (!requireNamespace(p, quietly = TRUE))
      warning(sprintf("Package '%s' not installed; using base-R fallback.", p))
  }
  invisible(NULL)
}

## ---- Data loader ------------------------------------------------------
load_data <- function() {
  p <- find_data()
  cat("Reading data from:", p, "\n")
  d <- tryCatch(
    readr::read_csv(p, show_col_types = FALSE),
    error = function(e) read.csv(p, stringsAsFactors = FALSE)
  )
  d <- as.data.frame(d)
  d$Group <- factor(d$Group, levels = c("Control", "Experimental"))
  d
}

## ---- generic ANCOVA runner (base R fallback if car/emmeans missing) ----
run_ancova <- function(d, post, pre, label) {
  d$Post <- d[[post]]; d$Pre <- d[[pre]]
  m <- lm(Post ~ Group + Pre, data = d)
  a <- Anova(m, type = "III")
  p_group <- a$"Pr(>F)"["Group"]
  p_pre   <- a$"Pr(>F)"["Pre"]
  ## partial eta squared
  pes_group <- a$"Sum Sq"["Group"] /
    (a$"Sum Sq"["Group"] + a$"Sum Sq"["Residuals"])
  ## adjusted means
  adj <- if (requireNamespace("emmeans", quietly = TRUE)) {
    em <- as.data.frame(emmeans::emmeans(m, ~ Group))
    data.frame(Group = em$Group, Adjusted_Mean = round(em$emmean, 2),
               SE = round(em$SE, 2))
  } else {
    ## base-R fallback: predictions at grand-mean covariate
    nd <- data.frame(Group = levels(d$Group),
                     Pre = mean(d$Pre, na.rm = TRUE))
    pr <- predict(m, newdata = nd, se.fit = TRUE)
    data.frame(Group = nd$Group,
               Adjusted_Mean = round(pr$fit, 2), SE = round(pr$se.fit, 2))
  }
  ## Cohen's d on change scores (practical effect size)
  x1 <- d$Post[d$Group == "Experimental"] - d$Pre[d$Group == "Experimental"]
  x2 <- d$Post[d$Group == "Control"] - d$Pre[d$Group == "Control"]
  sp <- sqrt(((length(x1) - 1) * var(x1) + (length(x2) - 1) * var(x2)) /
             (length(x1) + length(x2) - 2))
  dz <- (mean(x1) - mean(x2)) / sp
  cat("\n===", label, "===\n")
  print(a)
  print(adj)
  cat(sprintf("Group effect: F p = %.4f | partial eta^2 = %.3f | Cohen's d (gain) = %.2f\n",
              p_group, pes_group, dz))
  list(model = m, anova = a, adjusted = adj,
       summary = data.frame(Outcome = label, F_p = p_group,
                            partial_eta_sq = pes_group, cohens_d = dz))
}

need(c("car", "emmeans"))
d <- if (file.exists("outputs/clean_data.rds")) readRDS("outputs/clean_data.rds") else load_data()
res <- run_ancova(d, "AI_Post", "AI_Pre", "AI Literacy")
write.csv(res$summary, "outputs/table6_ancova_ai_lit.csv", row.names = FALSE)
write.csv(res$adjusted, "outputs/table6_adjusted_means_ai_lit.csv", row.names = FALSE)
cat("Saved Table 6 outputs.\n")
