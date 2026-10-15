############################################################
##  NCAL-2026-1259 : EFL AI Writing Study (R replication)  ##
##  Script : 10 - Graphical abstract
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

need(c("ggplot2"))
d <- if (file.exists("outputs/clean_data.rds")) readRDS("outputs/clean_data.rds") else load_data()
dir.create("outputs", showWarnings = FALSE)

## composite 2x2 abstract: gains + key outcomes
gain_long <- do.call(rbind, lapply(list(
  c("Writing_Post", "Writing_Pre", "Writing"),
  c("SRL_Post", "SRL_Pre", "SRL"),
  c("AI_Post", "AI_Pre", "AI Literacy")), function(s) {
  data.frame(Outcome = s[3], Group = d$Group,
             Gain = d[[s[1]]] - d[[s[2]]])
}))

if (requireNamespace("ggplot2", quietly = TRUE)) {
  p <- ggplot(gain_long, aes(Outcome, Gain, fill = Group)) +
    stat_summary(fun = mean, geom = "col", position = position_dodge(0.9)) +
    stat_summary(fun.data = mean_se, geom = "errorbar",
                 position = position_dodge(0.9), width = 0.2) +
    scale_fill_manual(values = c(Control = "grey70", Experimental = "steelblue"),
                      name = NULL) +
    labs(title = "AI-Assisted vs. Conventional EFL Writing Instruction",
         subtitle = "Adjusted gains in writing quality, SRL, and AI literacy (NCAL-2026-1259)",
         y = "Mean gain (post - pre)", x = NULL) +
    theme_classic(base_size = 14) +
    theme(plot.title = element_text(face = "bold"))
  ggsave("outputs/graphical_abstract.png", p, width = 9, height = 5.5, dpi = 300)
  cat("Saved outputs/graphical_abstract.png\n")
} else {
  agg <- tapply(gain_long$Gain, list(gain_long$Outcome, gain_long$Group), mean)
  png("outputs/graphical_abstract.png", width = 2000, height = 1200, res = 200)
  barplot(agg, beside = TRUE, col = c("grey70", "steelblue"),
          legend = colnames(agg), ylab = "Mean gain")
  title("AI-Assisted vs. Conventional EFL Writing Instruction")
  dev.off()
  cat("Saved outputs/graphical_abstract.png (base R)\n")
}
