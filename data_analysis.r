library(KFAS)
library(purrr)
require(ggplot2)

solar_data <- read.csv("./data/for_r/8.csv")
#solar_data <- within(solar_data, {
#  Flared <- factor(y, levels = 0:1, labels = c("no", "yes"))
#})
solar_data$unsigned_flux <- unlist(map(solar_data$unsigned_flux, ~ .x / 1e21))

#Zt <- matrix(c(1, 0), 1, 2)
#Ht <- matrix(NA)
#Tt <- matrix(c(1, 0, 1, 1), 2, 2)
#Rt <- matrix(c(1, 0), 2, 1)
#Qt <- matrix(NA)
#a1 <- matrix(c(1, 0), 2, 1)
#P1 <- matrix(0, 2, 2)
#P1inf <- diag(2)

#model_gaussian <- SSModel(solar_data$unsigned_flux ~ -1 +
#  SSMcustom(Z = Zt, T = Tt, R = Rt, Q = Qt, a1 = a1, P1 = P1, P1inf = P1inf),
#  H = Ht)
#model <- SSModel(solar_data$unsigned_flux ~ SSMtrend(1, Q = 0.01), H = 0.25)
model <- SSModel(solar_data$y ~ SSMtrend(degree = 1, Q = 0.01), distribution="binomial")

#fit <- fitSSM(model, inits = c(0, 0), method = "BFGS")
fit <- fitSSM(model, inits = log(0.25), method = "BFGS", hessian = TRUE)

out_filter <- KFS(fit$model)
partial_signal <- as.data.frame(signal(out_filter, states="all"))
out <- as.numeric(out_filter$muhat[,1])
#out_filter
#out_filter$muhat
#solar_data$unsigned_flux

plot(solar_data$time, solar_data$y, type="l", col="blue")
lines(solar_data$time, out, col="red")

#qplot(solar_data$time, solar_data$unsigned_flux, geom="line")
#qplot(solar_data$time, out, geom="line")
