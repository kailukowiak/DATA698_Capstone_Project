tb_cleaner <- function(tb){
  naByCols <- sapply(tb, function(x) sum(is.na(x)))
  naByRow <- apply(tb, 1, function(x) sum(is.na(x)))
  ## Row Cleaning
  NaRowToAdmit <- data.table(dateRow = tb[, time], naCount = naByRow)
  NaRowToAdmit <- NaRowToAdmit[naCount > 20, dateRow]
  
  tb <- tb[!(time %in% NaRowToAdmit)]
  # Results
  naByCols <- sapply(tb, function(x) sum(is.na(x)))
  naByRow <- apply(tb, 1, function(x) sum(is.na(x)))
  # Column Cleaing 
  bad_stations <- names(naByCols[naByCols >= 100])
  tb[, (bad_stations) := NULL]
  # Results
  naByCols <- sapply(tb, function(x) sum(is.na(x)))
  naByRow <- apply(tb, 1, function(x) sum(is.na(x)))
  ## ColClean two
  bad_stations <- names(naByCols[naByCols >= 20])
  tb[, (bad_stations) := NULL]
  
  # Results
  naByCols <- sapply(tb, function(x) sum(is.na(x)))
  naByRow <- apply(tb, 1, function(x) sum(is.na(x)))
  # Row Clean two
  NaRowToAdmit <- data.table(dateRow=tb[, time], naCount = naByRow)
  NaRowToAdmit <- NaRowToAdmit[naCount>0, dateRow]
  
  tb <- tb[!(time %in% NaRowToAdmit)]
  tb[, time := as.POSIXct(time)]
  print(paste("The dimesnions of the final DF are:", dim(tb)))
  return(tb)
}


city_selector <- function(tb, dt, city){
  dt_city_names <- dt[area_name == (city), unique(address)]
  city_names <- c('time', intersect(dt_city_names, names(tb)))
  city = tb[, (city_names), with = FALSE]
  return(city)
}

ts_maker <- function(df){
  time_vec = df[, time]
  margin_mat <- df[, -'time']
  df <- xts(margin_mat, order.by=time_vec)
  df <- t(as.matrix(df))
  return(df)
}


labeler <- function(cl, name, depth, dt, merg_col){
  lab_dt <- cl %>% 
    cutree(depth) %>% 
    stack %>% 
    data.table
  setnames(lab_dt, c('ind', 'values'), c((merg_col), (name)))
  lab_dt <- merge(lab_dt, dt, by = merg_col) 
  lab_dt[, `:=`(time = NULL,
                margin = NULL,
                price = NULL)] 
  lab_dt <- unique(lab_dt)
  lab_dt[, (name) := paste0('Cluster_', as.factor(get(name)))]
  return(lab_dt)
}

merge_cleaner <- function(df1, df2, by){
  drop_vars <- intersect(names(df1), names(df2))
  df = merge(df1, df2, by = by)
  df[, grep('\\.y', names(df), value = TRUE) := NULL]
  setnames(df, names(df), gsub("\\.x", "", names(df)))
  return(df)
}

cluster_getter <- function(tb, method = 'COR'){
  tb <- ts_maker(tb)
  h <- diss(tb, METHOD = method)
  c <- hclust(h)
  return(c)
}

knn_maker <- function(dt){
  # Lable Must be first in dataset with lat, lng following
  lab_col <- names(dt)[1]
  in_train <- createDataPartition(y = dt[,as.factor(get(lab_col))], p = 0.7, list = FALSE)
  train_dt <- dt[in_train]
  test_dt <- dt[!in_train]
  # CV
  trControl <- trainControl(method  = "cv",
                            number  = 10)
  fit <- train(as.formula(paste0(lab_col, "~ .")),
               method     = "knn",
               tuneGrid   = expand.grid(k = 1:20),
               trControl  = trControl,
               metric     = "Accuracy",
               data       = train_dt)
  result_list <- list()
  preds <- predict(fit, newdata = test_dt)
  # List gen
  actuals <- as.factor(test_dt[, get(lab_col)])
  #conf_mat <- confusionMatrix(preds, actuals)
  try(accuracy_table <- table(preds, actuals))
  train_labs <- predict(fit, newdata = train_dt)
  train_labs <- train_dt[, train_preds := train_labs]
  result_list[['preds']] <- preds
  try(result_list[['conf_mat']] <- conf_mat)
  try(result_list[['accuracy_table']] <- accuracy_table)
  result_list[['train_labs']] <- train_labs
  result_list[['k']] <- as.integer(c(fit$bestTune))
  result_list[['fit']] <- fit
  return(result_list)
  
}
