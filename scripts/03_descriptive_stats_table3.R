############################################################
##  NCAL-2026-1259 : EFL AI Writing Study (R replication)  ##
##  Script : 03 - Descriptive statistics (Table 3)
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

## helper: one-sample t style descriptives per group
desc_by_group <- function(d, cols) {
  do.call(rbind, lapply(cols, function(cl) {
    do.call(rbind, lapply(levels(d$Group), function(g) {
      x <- d[[cl]][d$Group == g]; x <- x[is.finite(x)]
      data.frame(Outcome = cl, Group = g, n = length(x),
                 Mean = mean(x), SD = sd(x),
                 SE = sd(x) / sqrt(length(x)),
                 Median = median(x), Min = min(x), Max = max(x))
    }))
  }))
}

need(c("dplyr"))
d <- if (file.exists("outputs/clean_data.rds")) readRDS("outputs/clean_data.rds") else load_data()

cols <- c("Writing_Pre", "Writing_Post", "SRL_Pre", "SRL_Post", "AI_Pre", "AI_Post")
tab <- desc_by_group(d, cols)
tab_out <- transform(tab, Mean = round(Mean, 2), SD = round(SD, 2),
                     SE = round(SE, 2), Median = round(Median, 2),
                     Min = round(Min, 2), Max = round(Max, 2))
print(tab_out)

write.csv(tab_out, "outputs/table3_descriptives.csv", row.names = FALSE)
cat("Saved outputs/table3_descriptives.csv\n")
