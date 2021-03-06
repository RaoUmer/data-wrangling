# See egmm_with_r p. 22 for an example

library(gmm)

# load the data from 'test_r.csv'
setwd('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly')
df = read.csv('test_r.csv')

summary(res <- lm(p_2008~s_2008 + c_2008, df[,3:5]))  # Works

# theta is a list of the parameters to be estimated
#   theta[1] = just a number; solve for omega_g later
#   theta[2] = just a number; solve for sigma_g later
# x is the dataframe? colums are:
#   1: PRODUCT_NC
#   2: PARTNER
#   3: s_YYYY
#   4: p_YYYY
#   5: c_YYYY

theta0 <- coef(res)[cbind(2, 3)]
y <- as.matrix(df[,4])
z1 <- as.matrix(df[,3])
z2 <- as.matrix(df[,5])

res <-gmm(y~ z1 + z2, x=cbind(y, z2, z2))







df2 = df[1:10,]

g0 <- function(theta, x) {
  m = x[,2] - theta[1] * x[,1] - theta[2]*x[,3]
 return(m)
 }


g1 <- function(theta, x) {
    elas <- (x[4] - theta[1] * x[3] - theta[2] * x[5])
    for(i in 1:length(x[,1])){
        x[i, 4] - theta[1] * x[i, 3] - theta[2] * x[i, 5]
    }

    return(elas)
}

g2 <- function(theta, x) {
    m1 <- x[1, 4] - theta[1] * x[1, 3] - theta[2] * x[1, 5]
    m2 <- x[2, 4] - theta[1] * x[2, 3] - theta[2] * x[2, 5]
    m3 <- x[3, 4] - theta[1] * x[3, 3] - theta[2] * x[3, 5]
    m4 <- x[4, 4] - theta[1] * x[4, 3] - theta[2] * x[4, 5]
    m5 <- x[5, 4] - theta[1] * x[5, 3] - theta[2] * x[5, 5]
    m6 <- x[6, 4] - theta[1] * x[6, 3] - theta[2] * x[6, 5]
    m7 <- x[7, 4] - theta[1] * x[7, 3] - theta[2] * x[7, 5]
    m8 <- x[8, 4] - theta[1] * x[8, 3] - theta[2] * x[8, 5]
    m9 <- x[9, 4] - theta[1] * x[9, 3] - theta[2] * x[9, 5]
    m10 <- x[10, 4] - theta[1] * x[10, 3] - theta[2] * x[10, 5]
    f <- cbind(m1, m2, m3, m4, m5, m6, m7, m8, m9, m10)
    return(f)
}
theta0 = cbind(4,4)
res <- gmm(g2, x=df2, t0=theta0)
"""
Fails with:
Error in ar.ols(x, aic = aic, order.max = order.max, na.action = na.action,  : 
  'order.max' must be < 'n.used'
  OR
  can't eval at given params depending upon t0.
"""
# Linear method?
g3 <- function(theta, x){
   h = theta[1] * x[0] - theta[2] * x[5]}
   
   return h



############
g6 <- function(theta, x) {
    t <- length(x)
    et1 <- diff(x) - theta[1] - theta[2] * x[-t]
    ht <- et1^2 - theta[3] * x[-t] ^ (2 * theta[4])
    g <- cbind(et1, et1 * x[-t], ht, ht*x[-t])
    return(g)
}


