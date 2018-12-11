library(caret)
source('function.R')
# source('data_manipulator.R')

calg_raw_cor_5_res <- knn_maker(calg_lab[, .(calg_raw_cor_5, lat, lng)])
calg_raw_cor_2_res <- knn_maker(calg_lab[, .(calg_raw_cor_2, lat, lng)])

calg_raw_eucl_2_res <- knn_maker(calg_lab[, .(calg_raw_eucl_2, lat, lng)])
calg_raw_eucl_5_res <- knn_maker(calg_lab[, .(calg_raw_eucl_5, lat, lng)])

van_raw_eucl_5_res <- knn_maker(van_lab[, .(van_raw_eucl_5, lat, lng)])


# lab_col <- names(dt)[1]
# if (class(dt[, get(lab_col)]) != 'factor') {
#   dt[, lab_col:= as.factor(get(lab_col))]
# }

