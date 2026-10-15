############################################################
##  NCAL-2026-1259 : EFL AI Writing Study (R replication)  ##
##  Script : 02 - Load and clean data
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

need(c("readr", "dplyr", "tidyr"))

dir.create("outputs", showWarnings = FALSE)

d <- load_data()

## --- cleaning rules ----------------------------------------------------
## 1. drop duplicate IDs
d0 <- nrow(d)
d <- d[!duplicated(d$ID), ]
cat("Duplicates removed:", d0 - nrow(d), "\n")

## 2. coerce numerics, flag impossible values
num_cols <- c("Writing_Pre", "Writing_Post", "SRL_Pre", "SRL_Post", "AI_Pre", "AI_Post")
for (cl in num_cols) d[[cl]] <- suppressWarnings(as.numeric(d[[cl]]))

bad <- rowSums(sapply(num_cols, function(cl) !is.finite(d[[cl]]))) > 0
cat("Rows with missing/non-finite values:", sum(bad), "\n")
d <- d[!bad, ]

## 3. logical range checks (Writing 0-100, SRL 1-5, AI literacy 1-5)
rng <- list(Writing_Pre = c(0, 100), Writing_Post = c(0, 100),
            SRL_Pre = c(1, 5), SRL_Post = c(1, 5),
            AI_Pre = c(1, 5), AI_Post = c(1, 5))
for (cl in names(rng)) {
  o <- d[[cl]] < rng[[cl]][1] | d[[cl]] > rng[[cl]][2]
  if (any(o)) cat("Out-of-range values in", cl, ":", sum(o), "\n")
}

## 4. gain scores
d$Writing_Gain <- d$Writing_Post - d$Writing_Pre
d$SRL_Gain     <- d$SRL_Post - d$SRL_Pre
d$AI_Gain      <- d$AI_Post - d$AI_Pre

cat("Final clean dataset:", nrow(d), "rows.\n")
print(by(d[, c("Writing_Post", "SRL_Post", "AI_Post")], d$Group, colMeans))

saveRDS(d, "outputs/clean_data.rds")
write.csv(d, "outputs/clean_data.csv", row.names = FALSE)
cat("Saved outputs/clean_data.rds and outputs/clean_data.csv\n")
