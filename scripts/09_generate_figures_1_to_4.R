############################################################
##  NCAL-2026-1259 : EFL AI Writing Study (R replication)  ##
##  Script : 09 - Figures 1-4 (bar/interaction, gains, effect sizes)
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

need(c("ggplot2", "dplyr"))
d <- if (file.exists("outputs/clean_data.rds")) readRDS("outputs/clean_data.rds") else load_data()
dir.create("outputs/figures", showWarnings = FALSE)
has_gg <- requireNamespace("ggplot2", quietly = TRUE)

## helper for base-R plots if ggplot2 unavailable
save_base_bar <- function(pre, post, ylab, file) {
  ms <- tapply(d[[post]], d$Group, mean)
  ses <- tapply(d[[post]], d$Group, function(x) sd(x) / sqrt(length(x)))
  png(file.path("outputs/figures", file), width = 1200, height = 900, res = 160)
  bp <- barplot(ms, ylim = c(0, max(ms + ses) * 1.15), ylab = ylab,
                col = c("grey70", "steelblue"), border = NA)
  arrows(bp, ms - ses, bp, ms + ses, angle = 90, code = 3, length = 0.05)
  dev.off()
}

## ---- Figure 1: Writing quality pre/post by group ----------------------
if (has_gg) {
  p1 <- ggplot(d, aes(Group, Writing_Post, fill = Group)) +
    stat_summary(fun = mean, geom = "col") +
    stat_summary(fun.data = mean_se, geom = "errorbar", width = 0.2) +
    scale_fill_manual(values = c(Control = "grey70", Experimental = "steelblue")) +
    labs(title = "Figure 1. Writing Quality (Post) by Group",
         y = "Writing quality (post-test)") +
    theme_classic(base_size = 13) + theme(legend.position = "none")
  ggsave("outputs/figures/figure1_writing.png", p1, width = 6, height = 4.5, dpi = 300)
} else save_base_bar("Writing_Pre", "Writing_Post", "Writing quality", "figure1_writing.png")

## ---- Figure 2: SRL pre/post by group ----------------------------------
if (has_gg) {
  long <- rbind(
    data.frame(Group = d$Group, Time = "Pre",  Score = d$SRL_Post * 0 + d$SRL_Pre),
    data.frame(Group = d$Group, Time = "Post", Score = d$SRL_Post))
  p2 <- ggplot(long, aes(Time, Score, fill = Group)) +
    stat_summary(fun = mean, geom = "col", position = position_dodge()) +
    stat_summary(fun.data = mean_se, geom = "errorbar",
                 position = position_dodge(width = 0.9), width = 0.2) +
    scale_fill_manual(values = c(Control = "grey70", Experimental = "steelblue")) +
    labs(title = "Figure 2. SRL by Group and Time", y = "SRL score") +
    theme_classic(base_size = 13)
  ggsave("outputs/figures/figure2_srl.png", p2, width = 6, height = 4.5, dpi = 300)
}

## ---- Figure 3: AI literacy pre/post by group ---------------------------
if (has_gg) {
  long <- rbind(
    data.frame(Group = d$Group, Time = "Pre",  Score = d$AI_Pre),
    data.frame(Group = d$Group, Time = "Post", Score = d$AI_Post))
  p3 <- ggplot(long, aes(Time, Score, fill = Group)) +
    stat_summary(fun = mean, geom = "col", position = position_dodge()) +
    stat_summary(fun.data = mean_se, geom = "errorbar",
                 position = position_dodge(width = 0.9), width = 0.2) +
    scale_fill_manual(values = c(Control = "grey70", Experimental = "steelblue")) +
    labs(title = "Figure 3. AI Literacy by Group and Time", y = "AI literacy score") +
    theme_classic(base_size = 13)
  ggsave("outputs/figures/figure3_ai_lit.png", p3, width = 6, height = 4.5, dpi = 300)
}

## ---- Figure 4: effect-size / gain summary ------------------------------
gains <- data.frame(
  Outcome = c("Writing", "SRL", "AI Literacy"),
  Control = c(mean(d$Writing_Gain[d$Group == "Control"]),
              mean(d$SRL_Gain[d$Group == "Control"]),
              mean(d$AI_Gain[d$Group == "Control"])),
  Experimental = c(mean(d$Writing_Gain[d$Group == "Experimental"]),
                   mean(d$SRL_Gain[d$Group == "Experimental"]),
                   mean(d$AI_Gain[d$Group == "Experimental"])))
print(round(gains, 2))
write.csv(gains, "outputs/figure4_gain_summary.csv", row.names = FALSE)

if (has_gg) {
  lg <- reshape(gains, direction = "long", varying = 2:3,
                v.names = "Gain", times = c("Control", "Experimental"),
                timevar = "Group")
  p4 <- ggplot(lg, aes(Outcome, Gain, fill = Group)) +
    geom_col(position = position_dodge()) +
    scale_fill_manual(values = c(Control = "grey70", Experimental = "steelblue")) +
    labs(title = "Figure 4. Pre-to-Post Gains by Group and Outcome", y = "Gain score") +
    theme_classic(base_size = 13)
  ggsave("outputs/figures/figure4_gains.png", p4, width = 6.5, height = 4.5, dpi = 300)
}
cat("Figures saved under outputs/figures/\n")
