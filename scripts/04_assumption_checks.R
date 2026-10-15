############################################################
##  NCAL-2026-1259 : EFL AI Writing Study (R replication)  ##
##  Script : 04 - Assumption checks (normality, homogeneity)
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

need(c("car"))
d <- if (file.exists("outputs/clean_data.rds")) readRDS("outputs/clean_data.rds") else load_data()

res <- data.frame()
for (cl in c("Writing_Post", "SRL_Post", "AI_Post")) {
  pre  <- sub("_Post", "_Pre", cl)
  f <- as.formula(paste(cl, "~ Group +", pre))
  m  <- lm(f, data = d)
  ## normality of residuals
  sw <- tryCatch(shapiro.test(residuals(m))$p.value, error = function(e) NA)
  ## homogeneity of variance
  lv <- tryCatch(leveneTest(as.formula(paste(cl, "~ Group")), data = d)$`Pr(>F)`[1],
                 error = function(e) NA)
  res <- rbind(res, data.frame(Outcome = cl,
                               Shapiro_Wilk_p = round(sw, 4),
                               Levene_p = round(lv, 4)))
}
print(res)
write.csv(res, "outputs/assumption_checks.csv", row.names = FALSE)
cat("Saved outputs/assumption_checks.csv\n")
cat("alpha = .05 : p > .05 supports the assumption.\n")
