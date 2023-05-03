# Code for corresponding plots
# Reference: http://www.cookbook-r.com/Graphs/Plotting_means_and_error_bars_(ggplot2)/

library(tidyverse)
library(ggnuplot)
library(cowplot)
library(ggpubr)
library(extrafont)
library(RColorBrewer)
library("gridExtra")
library(ggtext)


yang_robust_results <- read_csv("results_yangetal.csv") %>%
  mutate(distribution=recode(distribution,
                             `Dist g` = "Dist G",
                             `Dist h` = "Dist H",
                             `Dist i` = "Dist I")) %>% dplyr::rename(Distribution = distribution)


distributions_k_CI <- read_csv("varyingitemnum_distribution_results.csv") %>%
  mutate(distribution=recode(distribution,
                             `Dist a`="Dist A",
                             `Dist b`= "Dist B",
                             `Dist c`= "Dist C",
                             `Dist d` = "Dist D",
                             `Dist e` = "Dist E",
                             `Dist f` = "Dist F",
                             `Dist g` = "Dist G",
                             `Dist h` = "Dist H",
                             `Dist i` = "Dist I"))%>% dplyr::rename(Distribution = distribution)%>%
  mutate(item_counts=recode(item_counts,
                            `100`="100",
                            `1000`= "1k",
                            `10000`= "10k",
                            `100000` = "100k"))
distributions_k_CI$item_counts <- as.factor(distributions_k_CI$item_counts)
distributions_k_CI$item_counts <- factor(distributions_k_CI$item_counts, levels=c("100", "1k", "10k", "100k"))





case_results <- read_csv("all_distribution_results.csv") %>%
  mutate(distribution=recode(distribution,
                             `Dist a`="Dist A",
                             `Dist b`= "Dist B",
                             `Dist c`= "Dist C",
                             `Dist d` = "Dist D",
                             `Dist e` = "Dist E",
                             `Dist f` = "Dist F",
                             `Dist g` = "Dist G",
                             `Dist h` = "Dist H",
                             `Dist i` = "Dist I"))%>% dplyr::rename(Distribution = distribution)



multi <- case_results %>%
  filter(Distribution != "Dist G" & 
           Distribution != "Dist H" & 
           Distribution != "Dist I" )

bi <- case_results %>%
  filter(Distribution != "Dist A" & 
           Distribution != "Dist B" & 
           Distribution != "Dist C" &
           Distribution != "Dist D" & 
           Distribution != "Dist E" & 
           Distribution != "Dist F")




pt_size <- 2.5 #3
title_size <- 10
linesize <- 1
axistext <- 14




multi_colors <- c('darkviolet', '#009e73', '#56b4e9','#e69f00', '#f0e442', 'red')


multi_shapes <- c(15, 16, 18, 8, 5, 1)


bi_colors <- c('burlywood', '#3ca8bc', 'deeppink')

all_colors <- c('darkviolet', '#009e73', '#56b4e9','#e69f00', '#f0e442', 'red', 'burlywood', '#3ca8bc', 'deeppink')
bi_shapes <- c(17, 16, 18)

k_colors <- c('#a1d99b', '#74c476', '#238b45', '#005a32')
k_shapes <- c(15, 16, 8, 5)

x_string <- "\u03A6 (Gains Unfairness)"



CI_width <- 0.1

# Reference: http://www.cookbook-r.com/Graphs/Plotting_means_and_error_bars_(ggplot2)/
## Gives count, mean, standard deviation, standard error of the mean, and confidence interval (default 95%).
##   data: a data frame.
##   measurevar: the name of a column that contains the variable to be summariezed
##   groupvars: a vector containing names of columns that contain grouping variables
##   na.rm: a boolean that indicates whether to ignore NA's
##   conf.interval: the percent range of the confidence interval (default is 95%)
summarySE <- function(data=NULL, measurevar, groupvars=NULL, na.rm=FALSE,
                      conf.interval=.95, .drop=TRUE) {
  library(plyr)
  
  # New version of length which can handle NA's: if na.rm==T, don't count them
  length2 <- function (x, na.rm=FALSE) {
    if (na.rm) sum(!is.na(x))
    else       length(x)
  }
  
  # This does the summary. For each group's data frame, return a vector with
  # N, mean, and sd
  datac <- ddply(data, groupvars, .drop=.drop,
                 .fun = function(xx, col) {
                   c(N    = length2(xx[[col]], na.rm=na.rm),
                     mean = mean   (xx[[col]], na.rm=na.rm),
                     sd   = sd     (xx[[col]], na.rm=na.rm)
                   )
                 },
                 measurevar
  )
  
  # Rename the "mean" column    
  datac <- rename(datac, c("mean" = measurevar))
  
  datac$se <- datac$sd / sqrt(datac$N)  # Calculate standard error of the mean
  
  # Confidence interval multiplier for standard error
  # Calculate t-statistic for confidence interval: 
  # e.g., if conf.interval is .95, use .975 (above/below), and use df=N-1
  ciMult <- qt(conf.interval/2 + .5, datac$N-1)
  datac$ci <- datac$se * ciMult
  
  return(datac)
}

## Norms the data within specified groups in a data frame; it normalizes each
## subject (identified by idvar) so that they have the same mean, within each group
## specified by betweenvars.
##   data: a data frame.
##   idvar: the name of a column that identifies each subject (or matched subjects)
##   measurevar: the name of a column that contains the variable to be summariezed
##   betweenvars: a vector containing names of columns that are between-subjects variables
##   na.rm: a boolean that indicates whether to ignore NA's
normDataWithin <- function(data=NULL, idvar, measurevar, betweenvars=NULL,
                           na.rm=FALSE, .drop=TRUE) {
  library(plyr)
  
  # Measure var on left, idvar + between vars on right of formula.
  data.subjMean <- ddply(data, c(idvar, betweenvars), .drop=.drop,
                         .fun = function(xx, col, na.rm) {
                           c(subjMean = mean(xx[,col], na.rm=na.rm))
                         },
                         measurevar,
                         na.rm
  )
  
  # Put the subject means with original data
  data <- merge(data, data.subjMean)
  
  # Get the normalized data in a new column
  measureNormedVar <- paste(measurevar, "_norm", sep="")
  data[,measureNormedVar] <- data[,measurevar] - data[,"subjMean"] +
    mean(data[,measurevar], na.rm=na.rm)
  
  # Remove this subject mean column
  data$subjMean <- NULL
  
  return(data)
}

## Summarizes data, handling within-subjects variables by removing inter-subject variability.
## It will still work if there are no within-S variables.
## Gives count, un-normed mean, normed mean (with same between-group mean),
##   standard deviation, standard error of the mean, and confidence interval.
## If there are within-subject variables, calculate adjusted values using method from Morey (2008).
##   data: a data frame.
##   measurevar: the name of a column that contains the variable to be summariezed
##   betweenvars: a vector containing names of columns that are between-subjects variables
##   withinvars: a vector containing names of columns that are within-subjects variables
##   idvar: the name of a column that identifies each subject (or matched subjects)
##   na.rm: a boolean that indicates whether to ignore NA's
##   conf.interval: the percent range of the confidence interval (default is 95%)
summarySEwithin <- function(data=NULL, measurevar, betweenvars=NULL, withinvars=NULL,
                            idvar=NULL, na.rm=FALSE, conf.interval=.95, .drop=TRUE) {
  
  # Ensure that the betweenvars and withinvars are factors
  factorvars <- vapply(data[, c(betweenvars, withinvars), drop=FALSE],
                       FUN=is.factor, FUN.VALUE=logical(1))
  
  if (!all(factorvars)) {
    nonfactorvars <- names(factorvars)[!factorvars]
    message("Automatically converting the following non-factors to factors: ",
            paste(nonfactorvars, collapse = ", "))
    data[nonfactorvars] <- lapply(data[nonfactorvars], factor)
  }
  
  # Get the means from the un-normed data
  datac <- summarySE(data, measurevar, groupvars=c(betweenvars, withinvars),
                     na.rm=na.rm, conf.interval=conf.interval, .drop=.drop)
  
  # Drop all the unused columns (these will be calculated with normed data)
  datac$sd <- NULL
  datac$se <- NULL
  datac$ci <- NULL
  
  # Norm each subject's data
  ndata <- normDataWithin(data, idvar, measurevar, betweenvars, na.rm, .drop=.drop)
  
  # This is the name of the new column
  measurevar_n <- paste(measurevar, "_norm", sep="")
  
  # Collapse the normed data - now we can treat between and within vars the same
  ndatac <- summarySE(ndata, measurevar_n, groupvars=c(betweenvars, withinvars),
                      na.rm=na.rm, conf.interval=conf.interval, .drop=.drop)
  
  # Apply correction from Morey (2008) to the standard error and confidence interval
  #  Get the product of the number of conditions of within-S variables
  nWithinGroups    <- prod(vapply(ndatac[,withinvars, drop=FALSE], FUN=nlevels,
                                  FUN.VALUE=numeric(1)))
  correctionFactor <- sqrt( nWithinGroups / (nWithinGroups-1) )
  
  # Apply the correction factor
  ndatac$sd <- ndatac$sd * correctionFactor
  ndatac$se <- ndatac$se * correctionFactor
  ndatac$ci <- ndatac$ci * correctionFactor
  
  # Combine the un-normed means with the normed results
  merge(datac, ndatac)
}


####### CASE STUDY PLOTS

ER_multi_ci <- summarySEwithin(multi, measurevar="ers", withinvars=c("phis", "Distribution"), idvar="trials")

ER_ci_mp <- ggplot(ER_multi_ci, aes(color = Distribution, x  = as.numeric(as.character(phis)), y = ers, shape = Distribution)) +
  geom_point(size = pt_size)+
  geom_line(size = linesize)+
  geom_errorbar(width=CI_width, aes(ymin=ers-ci, ymax=ers+ci))+
  theme_gnuplot()+
  xlab(x_string)+
  ylab("ER")+
  theme_gnuplot()+
  theme(legend.position = "top",
        legend.direction = "horizontal",
        axis.title.y = element_text(size = axistext),
        axis.title.x = element_text(size = axistext))+
  ggtitle("ER")+
  scale_shape_manual(values=multi_shapes)+
  scale_color_manual(values=multi_colors)+
  guides(color=guide_legend(nrow=1))+
  guides(shape = guide_legend(nrow = 1))


AWRF_multi_ci <- summarySEwithin(multi, measurevar="awrfs", withinvars=c("phis", "Distribution"), idvar="trials")

AWRF_ci_mp <- ggplot(AWRF_multi_ci, aes(color = Distribution, x  = as.numeric(as.character(phis)), y = awrfs, shape = Distribution)) +
  geom_point(size = pt_size)+
  geom_line(size = linesize)+
  geom_errorbar(width=CI_width, aes(ymin=awrfs-ci, ymax=awrfs+ci))+
  theme_gnuplot()+
  xlab(x_string)+
  ylab("AWRF")+
  theme_gnuplot()+
  theme(legend.position = "top",
        legend.direction = "horizontal",
        axis.title.y = element_text(size = axistext),
        axis.title.x = element_text(size = axistext))+
  ggtitle("AWRF")+
  scale_shape_manual(values=multi_shapes)+
  scale_color_manual(values=multi_colors)+
  guides(color=guide_legend(nrow=1))+
  guides(shape = guide_legend(nrow = 1))


NDKL_multi_ci <- summarySEwithin(multi, measurevar="ndkls", withinvars=c("phis", "Distribution"), idvar="trials")

NDKL_ci_mp <- ggplot(NDKL_multi_ci, aes(color = Distribution, x  = as.numeric(as.character(phis)), y = ndkls, shape = Distribution)) +
  geom_point(size = pt_size)+
  geom_line(size = linesize)+
  geom_errorbar(width=CI_width, aes(ymin=ndkls-ci, ymax=ndkls+ci))+
  theme_gnuplot()+
  xlab(x_string)+
  ylab("NDKL")+
  theme_gnuplot()+
  theme(legend.position = "top",
        legend.direction = "horizontal",
        axis.title.y = element_text(size = axistext),
        axis.title.x = element_text(size = axistext))+
  ggtitle("NDKL")+
  scale_shape_manual(values=multi_shapes)+
  scale_color_manual(values=multi_colors)+
  guides(color=guide_legend(nrow=1))+
  guides(shape = guide_legend(nrow = 1))

EED_multi_ci <- summarySEwithin(multi, measurevar="eeds", withinvars=c("phis", "Distribution"), idvar="trials")

EED_ci_mp <- ggplot(EED_multi_ci, aes(color = Distribution, x  = as.numeric(as.character(phis)), y = eeds, shape = Distribution)) +
  geom_point(size = pt_size)+
  geom_line(size = linesize)+
  geom_errorbar(width=CI_width, aes(ymin=eeds-ci, ymax=eeds+ci))+
  theme_gnuplot()+
  xlab(x_string)+
  ylab("EE-D")+
  ylim(0, NA)+
  theme_gnuplot()+
  theme(legend.position = "top",
        legend.direction = "horizontal",
        axis.title.y = element_text(size = axistext),
        axis.title.x = element_text(size = axistext))+
  ggtitle("EE-D")+
  scale_shape_manual(values=multi_shapes)+
  scale_color_manual(values=multi_colors)+
  guides(color=guide_legend(nrow=1))+
  guides(shape = guide_legend(nrow = 1))

ARP_multi_ci <- summarySEwithin(multi, measurevar="arps", withinvars=c("phis", "Distribution"), idvar="trials")

ARP_ci_mp <- ggplot(ARP_multi_ci, aes(color = Distribution, x  = as.numeric(as.character(phis)), y = arps, shape = Distribution)) +
  geom_point(size = pt_size)+
  geom_line(size = linesize)+
  geom_errorbar(width=CI_width, aes(ymin=arps-ci, ymax=arps+ci))+
  theme_gnuplot()+
  xlab(x_string)+
  ylab("ARP")+
  theme_gnuplot()+
  theme(legend.position = "top",
        legend.direction = "horizontal",
        axis.title.y = element_text(size = axistext),
        axis.title.x = element_text(size = axistext))+
  ggtitle("ARP")+
  scale_shape_manual(values=multi_shapes)+
  scale_color_manual(values=multi_colors)+
  guides(color=guide_legend(nrow=1))+
  guides(shape = guide_legend(nrow = 1))


pdfwidth <- 14
pdfheight <- 3.2


fig_ci_multi <- ggarrange(ER_ci_mp, AWRF_ci_mp,NDKL_ci_mp, EED_ci_mp, ARP_ci_mp,
                          ncol = 5, nrow = 1, common.legend = TRUE, legend = "top")

ggsave(fig_ci_multi, filename = "plots/ci_multi_distributions.pdf", device = cairo_pdf,
       width = pdfwidth, height = pdfheight, units = "in")



#### BINARY GROUPS CONFIDENCE INTERVALS

ER_bi_ci <- summarySEwithin(bi, measurevar="ers", withinvars=c("phis", "Distribution"), idvar="trials")

ER_ci_bp <- ggplot(ER_bi_ci, aes(color = Distribution, x  = as.numeric(as.character(phis)), y = ers, shape = Distribution)) +
  geom_point(size = pt_size)+
  geom_line(size = linesize)+
  geom_errorbar(width=CI_width, aes(ymin=ers-ci, ymax=ers+ci))+
  theme_gnuplot()+
  xlab(x_string)+
  ylab("ER")+
  theme_gnuplot()+
  theme(legend.position = "top",
        legend.direction = "horizontal",
        axis.title.y = element_text(size = axistext),
        axis.title.x = element_text(size = axistext))+
  ggtitle("ER")+
  scale_shape_manual(values=bi_shapes)+
  scale_color_manual(values=bi_colors)+
  guides(color=guide_legend(nrow=1))+
  guides(shape = guide_legend(nrow = 1))


AWRF_bi_ci <- summarySEwithin(bi, measurevar="awrfs", withinvars=c("phis", "Distribution"), idvar="trials")

AWRF_ci_bp <- ggplot(AWRF_bi_ci, aes(color = Distribution, x  = as.numeric(as.character(phis)), y = awrfs, shape = Distribution)) +
  geom_point(size = pt_size)+
  geom_line(size = linesize)+
  geom_errorbar(width=CI_width, aes(ymin=awrfs-ci, ymax=awrfs+ci))+
  theme_gnuplot()+
  xlab(x_string)+
  ylab("AWRF")+
  theme_gnuplot()+
  theme(legend.position = "top",
        legend.direction = "horizontal",
        axis.title.y = element_text(size = axistext),
        axis.title.x = element_text(size = axistext))+
  ggtitle("AWRF")+
  scale_shape_manual(values=bi_shapes)+
  scale_color_manual(values=bi_colors)+
  guides(color=guide_legend(nrow=1))+
  guides(shape = guide_legend(nrow = 1))


NDKL_bi_ci <- summarySEwithin(bi, measurevar="ndkls", withinvars=c("phis", "Distribution"), idvar="trials")

NDKL_ci_bp <- ggplot(NDKL_bi_ci, aes(color = Distribution, x  = as.numeric(as.character(phis)), y = ndkls, shape = Distribution)) +
  geom_point(size = pt_size)+
  geom_line(size = linesize)+
  geom_errorbar(width=CI_width, aes(ymin=ndkls-ci, ymax=ndkls+ci))+
  theme_gnuplot()+
  xlab(x_string)+
  ylab("NDKL")+
  theme_gnuplot()+
  theme(legend.position = "top",
        legend.direction = "horizontal",
        axis.title.y = element_text(size = axistext),
        axis.title.x = element_text(size = axistext))+
  ggtitle("NDKL")+
  scale_shape_manual(values=bi_shapes)+
  scale_color_manual(values=bi_colors)+
  guides(color=guide_legend(nrow=1))+
  guides(shape = guide_legend(nrow = 1))

EED_bi_ci <- summarySEwithin(bi, measurevar="eeds", withinvars=c("phis", "Distribution"), idvar="trials")

EED_ci_bp <- ggplot(EED_bi_ci, aes(color = Distribution, x  = as.numeric(as.character(phis)), y = eeds, shape = Distribution)) +
  geom_point(size = pt_size)+
  geom_line(size = linesize)+
  geom_errorbar(width=CI_width, aes(ymin=eeds-ci, ymax=eeds+ci))+
  theme_gnuplot()+
  xlab(x_string)+
  ylab("EE-D")+
  ylim(0, NA)+
  theme_gnuplot()+
  theme(legend.position = "top",
        legend.direction = "horizontal",
        axis.title.y = element_text(size = axistext),
        axis.title.x = element_text(size = axistext))+
  ggtitle("EE-D")+
  scale_shape_manual(values=bi_shapes)+
  scale_color_manual(values=bi_colors)+
  guides(color=guide_legend(nrow=1))+
  guides(shape = guide_legend(nrow = 1))

ARP_bi_ci <- summarySEwithin(bi, measurevar="arps", withinvars=c("phis", "Distribution"), idvar="trials")

ARP_ci_bp <- ggplot(ARP_bi_ci, aes(color = Distribution, x  = as.numeric(as.character(phis)), y = arps, shape = Distribution)) +
  geom_point(size = pt_size)+
  geom_line(size = linesize)+
  geom_errorbar(width=CI_width, aes(ymin=arps-ci, ymax=arps+ci))+
  theme_gnuplot()+
  xlab(x_string)+
  ylab("ARP")+
  theme_gnuplot()+
  theme(legend.position = "top",
        legend.direction = "horizontal",
        axis.title.y = element_text(size = axistext),
        axis.title.x = element_text(size = axistext))+
  ggtitle("ARP")+
  scale_shape_manual(values=bi_shapes)+
  scale_color_manual(values=bi_colors)+
  guides(color=guide_legend(nrow=1))+
  guides(shape = guide_legend(nrow = 1))


pdfwidth <- 14
pdfheight <- 3.2


fig_ci_bi <- ggarrange(ER_ci_bp, AWRF_ci_bp,NDKL_ci_bp, EED_ci_bp, ARP_ci_bp,
                       ncol = 5, nrow = 1, common.legend = TRUE, legend = "top")

ggsave(fig_ci_bi, filename = "plots/ci_binary_distributions.pdf", device = cairo_pdf,
       width = pdfwidth, height = pdfheight, units = "in")





# TWO GROUPS - YANG ET AL METHOD WITH CI
ER_biyang_ci <- summarySEwithin(yang_robust_results, measurevar="ers", withinvars=c("phis", "Distribution"), idvar="trials")

x_string_yang <- "Fairness Probability f"
ER_yang_ci <- ggplot(ER_biyang_ci, aes(color = Distribution, x  = as.numeric(as.character(phis)), y = ers, shape = Distribution)) +
  geom_point(size = pt_size)+
  geom_line(size = linesize)+
  geom_errorbar(width=CI_width, aes(ymin=ers-ci, ymax=ers+ci))+
  theme_gnuplot()+
  xlab(x_string_yang)+
  ylab("ER")+
  theme_gnuplot()+
  theme(legend.position = "top",
        legend.direction = "horizontal",
        axis.title.y = element_text(size = axistext),
        axis.title.x = element_text(size = axistext))+
  ggtitle("ER")+
  scale_shape_manual(values=bi_shapes)+
  scale_color_manual(values=bi_colors)

AWRF_biyang_ci <- summarySEwithin(yang_robust_results, measurevar="awrfs", withinvars=c("phis", "Distribution"), idvar="trials")

AWRF_yang_ci <- ggplot(AWRF_biyang_ci, aes(color = Distribution, x  = as.numeric(as.character(phis)), y = awrfs, shape = Distribution)) +
  geom_point(size = pt_size)+
  geom_line(size = linesize)+
  geom_errorbar(width=CI_width, aes(ymin=awrfs-ci, ymax=awrfs+ci))+
  theme_gnuplot()+
  xlab(x_string_yang)+
  ylab("AWRF")+
  theme_gnuplot()+
  theme(legend.position = "top",
        legend.direction = "horizontal",
        axis.title.y = element_text(size = axistext),
        axis.title.x = element_text(size = axistext))+
  ggtitle("AWRF")+
  scale_shape_manual(values=bi_shapes)+
  scale_color_manual(values=bi_colors)

NDKL_biyang_ci <- summarySEwithin(yang_robust_results, measurevar="ndkls", withinvars=c("phis", "Distribution"), idvar="trials")
NDKL_yang_ci <- ggplot(NDKL_biyang_ci, aes(color = Distribution, x  = as.numeric(as.character(phis)), y = ndkls, shape = Distribution)) +
  geom_point(size = pt_size)+
  geom_line(size = linesize)+
  geom_errorbar(width=CI_width, aes(ymin=ndkls-ci, ymax=ndkls+ci))+
  theme_gnuplot()+
  xlab(x_string_yang)+
  ylab("NDKL")+
  theme_gnuplot()+
  theme(legend.position = "top",
        legend.direction = "horizontal",
        axis.title.y = element_text(size = axistext),
        axis.title.x = element_text(size = axistext))+
  ggtitle("NDKL")+
  scale_shape_manual(values=bi_shapes)+
  scale_color_manual(values=bi_colors)

EED_biyang_ci <- summarySEwithin(yang_robust_results, measurevar="eeds", withinvars=c("phis", "Distribution"), idvar="trials")
EED_yang_ci <- ggplot(EED_biyang_ci, aes(color = Distribution, x  = as.numeric(as.character(phis)), y = eeds, shape = Distribution)) +
  geom_point(size = pt_size)+
  geom_line(size = linesize)+
  geom_errorbar(width=CI_width, aes(ymin=eeds-ci, ymax=eeds+ci))+
  theme_gnuplot()+
  xlab(x_string_yang)+
  ylab("EE-D")+
  ylim(0, NA)+
  theme_gnuplot()+
  theme(legend.position = "top",
        legend.direction = "horizontal",
        axis.title.y = element_text(size = axistext),
        axis.title.x = element_text(size = axistext))+
  ggtitle("EE-D")+
  scale_shape_manual(values=bi_shapes)+
  scale_color_manual(values=bi_colors)

ARP_biyang_ci <- summarySEwithin(yang_robust_results, measurevar="arps", withinvars=c("phis", "Distribution"), idvar="trials")

ARP_yang_ci <- ggplot(ARP_biyang_ci, aes(color = Distribution, x  = as.numeric(as.character(phis)), y = arps, shape = Distribution)) +
  geom_point(size = pt_size)+
  geom_line(size = linesize)+
  geom_errorbar(width=CI_width, aes(ymin=arps-ci, ymax=arps+ci))+
  theme_gnuplot()+
  xlab(x_string_yang)+
  ylab("ARP")+
  theme_gnuplot()+
  theme(legend.position = "top",
        legend.direction = "horizontal",
        axis.title.y = element_text(size = axistext),
        axis.title.x = element_text(size = axistext))+
  ggtitle("ARP")+
  scale_shape_manual(values=bi_shapes)+
  scale_color_manual(values=bi_colors)


pdfwidth <- 14
pdfheight <- 3.2


fig_ci_yang <- ggarrange(ER_yang_ci, AWRF_yang_ci,NDKL_yang_ci, EED_yang_ci, ARP_yang_ci,
                         ncol = 5, nrow = 1, common.legend = TRUE, legend = "top")

ggsave(fig_ci_yang, filename = "plots/yangetal_ci_distributions.pdf", device = cairo_pdf,
       width = pdfwidth, height = pdfheight, units = "in")



# DISTRIBUTIONS ACROSS K CI


make_plot_CI <- function(Distribution) {
  
  
  
  
  k_data <-  distributions_k_CI %>%
    filter(.data$Distribution == .env$Distribution) 

  
  ER_k_CI <- summarySEwithin(k_data, measurevar="ers", withinvars=c("phis", "item_counts"), idvar="trials") %>%
    ggplot(aes(color = item_counts, x  = as.numeric(as.character(phis)), y = ers, shape = item_counts)) +
    geom_point(size = pt_size)+
    geom_line(size = linesize)+
    geom_errorbar(width=CI_width, aes(ymin=ers-ci, ymax=ers+ci))+
    theme_gnuplot()+
    xlab(x_string)+
    ylab("ER")+
    theme_gnuplot()+
    theme(legend.position = "top",
          legend.direction = "horizontal",
          axis.title.y = element_text(size = axistext),
          axis.title.x = element_text(size = axistext))+
    ggtitle("ER")+
    scale_shape_manual("Ranked items:", values=k_shapes)+
    scale_color_manual("Ranked items:", values=k_colors)+
    guides(color=guide_legend(nrow=1))+
    guides(shape = guide_legend(nrow = 1))
  
  AWRF_k_CI <- summarySEwithin(k_data, measurevar="awrfs", withinvars=c("phis", "item_counts"), idvar="trials") %>%
    ggplot(aes(color = item_counts, x  = as.numeric(as.character(phis)), y = awrfs, shape = item_counts)) +
    geom_point(size = pt_size)+
    geom_line(size = linesize)+
    geom_errorbar(width=CI_width, aes(ymin=awrfs-ci, ymax=awrfs+ci))+
    theme_gnuplot()+
    xlab(x_string)+
    ylab("AWRF")+
    theme_gnuplot()+
    theme(legend.position = "top",
          legend.direction = "horizontal",
          axis.title.y = element_text(size = axistext),
          axis.title.x = element_text(size = axistext))+
    ggtitle("AWRF")+
    scale_shape_manual("Ranked items:", values=k_shapes)+
    scale_color_manual("Ranked items:", values=k_colors)+
    guides(color=guide_legend(nrow=1))+
    guides(shape = guide_legend(nrow = 1))
  
  
  NDKL_k_CI <- summarySEwithin(k_data, measurevar="ndkls", withinvars=c("phis", "item_counts"), idvar="trials") %>%
    ggplot(aes(color = item_counts, x  = as.numeric(as.character(phis)), y = ndkls, shape = item_counts)) +
    geom_point(size = pt_size)+
    geom_line(size = linesize)+
    geom_errorbar(width=CI_width, aes(ymin=ndkls-ci, ymax=ndkls+ci))+
    theme_gnuplot()+
    xlab(x_string)+
    ylab("NDKL")+
    theme_gnuplot()+
    theme(legend.position = "top",
          legend.direction = "horizontal",
          axis.title.y = element_text(size = axistext),
          axis.title.x = element_text(size = axistext))+
    ggtitle("NDKL")+
    scale_shape_manual("Ranked items:", values=k_shapes)+
    scale_color_manual("Ranked items:", values=k_colors)+
    guides(color=guide_legend(nrow=1))+
    guides(shape = guide_legend(nrow = 1))
  
  
  EED_k_CI <- summarySEwithin(k_data, measurevar="eeds", withinvars=c("phis", "item_counts"), idvar="trials") %>%
    ggplot(aes(color = item_counts, x  = as.numeric(as.character(phis)), y = eeds, shape = item_counts)) +
    geom_point(size = pt_size)+
    geom_line(size = linesize)+
    geom_errorbar(width=CI_width, aes(ymin=eeds-ci, ymax=eeds+ci))+
    theme_gnuplot()+
    xlab(x_string)+
    ylab("EED")+
    theme_gnuplot()+
    theme(legend.position = "top",
          legend.direction = "horizontal",
          axis.title.y = element_text(size = axistext),
          axis.title.x = element_text(size = axistext))+
    ggtitle("EED")+
    scale_shape_manual("Ranked items:", values=k_shapes)+
    scale_color_manual("Ranked items:", values=k_colors)+
    guides(color=guide_legend(nrow=1))+
    guides(shape = guide_legend(nrow = 1))
  
  
  ARP_k_CI <- summarySEwithin(k_data, measurevar="arps", withinvars=c("phis", "item_counts"), idvar="trials") %>%
    ggplot(aes(color = item_counts, x  = as.numeric(as.character(phis)), y = arps, shape = item_counts)) +
    geom_point(size = pt_size)+
    geom_line(size = linesize)+
    geom_errorbar(width=CI_width, aes(ymin=arps-ci, ymax=arps+ci))+
    theme_gnuplot()+
    xlab(x_string)+
    ylab("ARP")+
    theme_gnuplot()+
    theme(legend.position = "top",
          legend.direction = "horizontal",
          axis.title.y = element_text(size = axistext),
          axis.title.x = element_text(size = axistext))+
    ggtitle("ARP")+
    scale_shape_manual("Ranked items:", values=k_shapes)+
    scale_color_manual("Ranked items:", values=k_colors)+
    guides(color=guide_legend(nrow=1))+
    guides(shape = guide_legend(nrow = 1))
  
  pdfwidth <- 14
  pdfheight <- 3.2
  
  
  fig_k <- ggarrange(ER_k_CI, AWRF_k_CI,NDKL_k_CI, EED_k_CI, ARP_k_CI,
                     ncol = 5, nrow = 1, common.legend = TRUE, legend = "top")
  
  ggsave(fig_k, filename = glue::glue("plots/k_distributions_{Distribution}.pdf"), device = cairo_pdf,
         width = pdfwidth, height = pdfheight, units = "in")
  
  
  
  
}

make_plot_CI('Dist A')
#uncomment for appendix
# make_plot_CI('Dist B')
# make_plot_CI('Dist C')
# make_plot_CI('Dist D')
# make_plot_CI('Dist E')
# make_plot_CI('Dist F')
# make_plot_CI('Dist G')
# make_plot_CI('Dist H')
# make_plot_CI('Dist I')
