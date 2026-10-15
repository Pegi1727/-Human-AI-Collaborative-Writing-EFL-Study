############################################################
##  NCAL-2026-1259 : EFL AI Writing Study (R replication)  ##
##  Script : 01 - Validate R environment
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

need(c("tidyverse", "readr", "dplyr", "car", "emmeans", "ggplot2", "rstatix"))

cat("R version :", R.version.string, "\n")
cat("Platform  :", R.version$platform, "\n\n")

pkgs <- c("readr", "dplyr", "tidyr", "ggplot2", "car", "emmeans", "rstatix")
for (p in pkgs) {
  ok <- requireNamespace(p, quietly = TRUE)
  cat(sprintf("%-10s : %s\n", p,
      if (ok) as.character(packageVersion(p)) else "NOT INSTALLED"))
}

## smoke test: data must load and have expected structure
d <- load_data()
stopifnot(all(c("ID", "Group", "Writing_Pre", "Writing_Post",
                "SRL_Pre", "SRL_Post", "AI_Pre", "AI_Post") %in% names(d)))
cat("\nData loaded OK:", nrow(d), "rows x", ncol(d), "cols.\n")
print(table(d$Group))
cat("\nEnvironment validation PASSED.\n")
