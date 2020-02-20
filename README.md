# hmi-time-series-analysis

## Introduction
The rapid emergence of magnetic flux and free magnetic energy on the solar photosphere often indicates an increased probability of future flaring activity. For example, two active regions with the same total unsigned flux but different flux emergence rates may have different flaring activity. However, the nature of this change remains poorly understood. What patterns surround flux emergence and the **temporal evolution of other magnetic variables** governing eruptive activity? And how can we use these patterns to improve our predictions of solar flares?

## Motivation
There are two main physics-related motivations for this project.

First, solar flares have a direct effect on space and earth; they can produce particles in the solar wind which can alter the earth’s magnetic field and emit radiation that affects spacecraft. Solar flares are often accompanied by coronal mass ejections that can affect satellites and power grids on earth. A better understanding of the factors that cause solar flares could allow for more accurate predictions of solar weather to keep satellites and grids functional, as well as improve planning for space travel.

Second, understanding the factors behind solar flares and how the magnetically active regions of the sun change would increase our knowledge of other stars. Many stars have starspots (and therefore magnetic field patterns) similar to the sun and understanding how the active region of the sun changes would provide insight into how these other stars behave.

## Results
We found that over time, the testing accuracies for the single-variable models increase over time.
This shows that there is signal encoded in the time series element of these variables.
Training on a model with all the HMI features aggregated consistently performs better than any single feature.
The highest-performing variables are total magnetic flux, total electric current, and free energy.
The lowest-performing variables are mean electric current and polarity inversion line flux.


---

The code for this project is included in this repo as an Jupyter notebook. Also check out my [blog post](https://www.lucaspauker.ml/projects/14) on this project!

---

Contributors: [Lucas Pauker](https://github.com/lucaspauker) (Stanford University), [Monica Bobra](https://github.com/mbobra) (Stanford University), [Eric Jonas](https://github.com/ericmjonas) (University of Chicago)
