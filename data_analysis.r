library(KFAS)
library(purrr)
require(ggplot2)

solar_data <- read.csv("./data/for_r/8.csv")
solar_data <- within(solar_data, {
  Flared <- factor(y, levels = 0:1, labels = c("no", "yes"))
})
solar_data$unsigned_flux <- unlist(map(solar_data$unsigned_flux, ~ .x / 1e21))

Zt <- matrix(c(1, 0), 1, 2)
Ht <- matrix(NA)
Tt <- matrix(c(1, 0, 1, 1), 2, 2)
Rt <- matrix(c(1, 0), 2, 1)
Qt <- matrix(NA)
a1 <- matrix(c(1, 0), 2, 1)
P1 <- matrix(0, 2, 2)
P1inf <- diag(2)

model_gaussian <- SSModel(solar_data$unsigned_flux ~ -1 +
  SSMcustom(Z = Zt, T = Tt, R = Rt, Q = Qt, a1 = a1, P1 = P1, P1inf = P1inf),
  H = Ht)

fit_gaussian <- fitSSM(model_gaussian, inits = c(0, 0), method = "BFGS")
#fit_gaussian

out_gaussian <- KFS(fit_gaussian$model)
att <- as.data.frame(out_gaussian$att)
#solar_data$unsigned_flux

qplot(solar_data$time, solar_data$unsigned_flux)
qplot(solar_data$time, att$custom1)
