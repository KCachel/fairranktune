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


gc <- read_csv("law_synthetic_generation.csv")



gc_original <-  gc %>%
  filter(phis == "original")



gc_synthetic <- gc %>%
  filter(phis != "original")





CI_width <- .1
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


text_offset <- .8
text_vjust <- -.5
text_color <- "#ef2922"
points_color <- "#00B0F0"
text_string <- "original"

ERs_p <- summarySEwithin(gc_synthetic, measurevar="ers", withinvars=c("phis"), idvar="trials") %>%
  mutate(phis = as.numeric(as.character(phis))) %>%
  ggplot(aes(x = phis, y = ers)) +
  geom_point(size = pt_size, color = points_color)+
  geom_errorbar(width=CI_width, aes(ymin=ers-ci, ymax=ers+ci), color = points_color)+
  theme_gnuplot()+
  xlab(x_string)+
  ylab("ER")+
  theme(legend.position = "top",
        legend.direction = "horizontal",
        axis.title.y = element_text(size = axistext),
        axis.title.x = element_text(size = axistext))+
  ggtitle("ER")+
  geom_hline(aes(yintercept = gc_original$ers), color = text_color) +
  geom_text(aes(text_offset, gc_original$ers, label = text_string, vjust = text_vjust), color = text_color)


AWRF_p <- summarySEwithin(gc_synthetic, measurevar="awrfs", withinvars=c("phis"), idvar="trials") %>%
  mutate(phis = as.numeric(as.character(phis))) %>%
  ggplot(aes(x = phis, y = awrfs)) +
  geom_point(size = pt_size, color = points_color)+
  geom_errorbar(width=CI_width, aes(ymin=awrfs-ci, ymax=awrfs+ci), color = points_color)+
  theme_gnuplot()+
  xlab(x_string)+
  ylab("AWRF")+
  theme(legend.position = "top",
        legend.direction = "horizontal",
        axis.title.y = element_text(size = axistext),
        axis.title.x = element_text(size = axistext))+
  ggtitle("AWRF")+
  geom_hline(aes(yintercept = gc_original$awrfs), color = text_color) +
  geom_text(aes(text_offset, gc_original$awrfs, label = text_string, vjust = text_vjust), color = text_color)



NDKL_p <- summarySEwithin(gc_synthetic, measurevar="ndkls", withinvars=c("phis"), idvar="trials") %>%
  mutate(phis = as.numeric(as.character(phis))) %>%
  ggplot(aes(x = phis, y = ndkls)) +
  geom_point(size = pt_size, color = points_color)+
  geom_errorbar(width=CI_width, aes(ymin=ndkls-ci, ymax=ndkls+ci), color = points_color)+
  theme_gnuplot()+
  xlab(x_string)+
  ylab("NDKL")+
  theme(legend.position = "top",
        legend.direction = "horizontal",
        axis.title.y = element_text(size = axistext),
        axis.title.x = element_text(size = axistext))+
  ggtitle("NDKL")+
  geom_hline(aes(yintercept = gc_original$ndkls), color = text_color) +
  geom_text(aes(text_offset, gc_original$ndkls, label = text_string, vjust = text_vjust), color = text_color)



EED_p <- summarySEwithin(gc_synthetic, measurevar="eeds", withinvars=c("phis"), idvar="trials") %>%
  mutate(phis = as.numeric(as.character(phis))) %>%
  ggplot(aes(x = phis, y = eeds))+
  geom_point(size = pt_size, color = points_color)+
  geom_errorbar(width=CI_width, aes(ymin=eeds-ci, ymax=eeds+ci), color = points_color)+
  theme_gnuplot()+
  xlab(x_string)+
  ylab("EED")+
  theme(legend.position = "top",
        legend.direction = "horizontal",
        axis.title.y = element_text(size = axistext),
        axis.title.x = element_text(size = axistext))+
  ggtitle("EED")+
  geom_hline(aes(yintercept = gc_original$eeds), color = text_color) +
  geom_text(aes(text_offset, gc_original$eeds, label = text_string, vjust = text_vjust), color = text_color)


ARP_p <- summarySEwithin(gc_synthetic, measurevar="arps", withinvars=c("phis"), idvar="trials") %>%
  mutate(phis = as.numeric(as.character(phis))) %>%
  ggplot(aes(x = phis, y = arps)) +
  geom_point(size = pt_size, color = points_color)+
  geom_errorbar(width=CI_width, aes(ymin=arps-ci, ymax=arps+ci), color = points_color)+
  theme_gnuplot()+
  xlab(x_string)+
  ylab("ARP")+
  theme(legend.position = "top",
        legend.direction = "horizontal",
        axis.title.y = element_text(size = axistext),
        axis.title.x = element_text(size = axistext))+
  ggtitle("ARP")+
  geom_hline(aes(yintercept = gc_original$arps), color = text_color) +
  geom_text(aes(text_offset, gc_original$arps, label = text_string, vjust = text_vjust), color = text_color)



pdfwidth <- 14
pdfheight <- 3


fig <- ggarrange(ERs_p, AWRF_p,NDKL_p, EED_p, ARP_p,
                   ncol = 5, nrow = 1, common.legend = FALSE, legend = "top")

ggsave(fig, filename = "plots/law_plot.pdf", device = cairo_pdf,
       width = pdfwidth, height = pdfheight, units = "in")


