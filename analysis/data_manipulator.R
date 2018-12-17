library(data.table)
library(magrittr)
library(zoo)
library(TSclust)
library(ggplot2)
library(lubridate)
library(dendextend)
library(circlize)
library(xts)
library(caret)
source('function.R')

# Data cleaning
dt <- fread("cleaned_list.csv")
dt[, `:=` (V1 = NULL,
           time = as.POSIXct(time))]

raw_marg <- tb_cleaner(fread('table.csv'))
adj_marg <- tb_cleaner(fread('no_trend.csv'))
raw_marg[, `:=`(`3407 43rd AveMill Woods, AB`=NULL,
                `7631 38th AveMill Woods, AB`=NULL)]

calg_raw <- city_selector(raw_marg, dt, 'calgary')
calg_adj <- city_selector(adj_marg, dt, 'calgary')
van_raw <- city_selector(raw_marg, dt, 'vancouver')
van_adj <- city_selector(adj_marg, dt, 'vancouver')

# ALL
raw_clust_cor <- cluster_getter(raw_marg)
raw_clust_eucl <- cluster_getter(raw_marg, method = 'EUCL')
adj_clust_cor <- cluster_getter(adj_marg)
adj_clust_eucl <- cluster_getter(adj_marg, method = "EUCL")
# Calgary
calg_raw_clust_cor <- cluster_getter(calg_raw)
calg_raw_clust_eucl <- cluster_getter(calg_raw, method = 'EUCL')
calg_adj_clust_cor <- cluster_getter(calg_adj)
calg_adj_clust_eucl <- cluster_getter(calg_adj, method = 'EUCL')

# Van
van_raw_clust_cor <- cluster_getter(van_raw)
van_raw_clust_eucl <- cluster_getter(van_raw, method = 'EUCL')
van_adj_clust_cor <- cluster_getter(van_adj)
van_adj_clust_eucl <- cluster_getter(van_adj, method = 'EUCL')

# Calg Lables
calg_lab <-  labeler(calg_raw_clust_cor, 'calg_raw_cor_2', 2, dt, 'address')
calg_lab <- labeler(calg_raw_clust_cor, 'calg_raw_cor_5', 5, calg_lab, 'address')

calg_lab <- labeler(calg_adj_clust_cor, 'calg_adj_cor_2', 2, calg_lab, 'address')
calg_lab <- labeler(calg_adj_clust_cor, 'calg_adj_cor_5', 5, calg_lab, 'address')

calg_lab <- labeler(calg_raw_clust_eucl, 'calg_raw_eucl_5', 5, calg_lab, 'address')
calg_lab <- labeler(calg_raw_clust_eucl, 'calg_raw_eucl_2', 2, calg_lab, 'address')

calg_lab <- labeler(calg_adj_clust_eucl, 'calg_adj_eucl_5', 5, calg_lab, 'address')
calg_lab <- labeler(calg_adj_clust_eucl, 'calg_adj_eucl_2', 2, calg_lab, 'address')

# All Lables
all_lab <- labeler(raw_clust_cor, 'raw_cor_6', 6, dt, 'address')
all_lab <- labeler(raw_clust_cor, 'raw_cor_12', 12, all_lab, 'address')

all_lab <- labeler(raw_clust_eucl, 'raw_eucl_12', 12, all_lab, 'address')
all_lab <- labeler(raw_clust_eucl, 'raw_eucl_6', 6, all_lab, 'address')

all_lab <- labeler(adj_clust_cor, 'adj_cor_12', 12, all_lab, 'address')
all_lab <- labeler(adj_clust_cor, 'adj_cor_6', 6, all_lab, 'address')

all_lab <- labeler(adj_clust_eucl, 'adj_eucl_6', 6, all_lab, 'address')
all_lab <- labeler(adj_clust_eucl, 'adj_eucl_12', 12, all_lab, 'address')


# Van Lables
van_lab <- labeler(van_raw_clust_cor,  'van_raw_cor_2', 2, dt, 'address')
van_lab <- labeler(van_raw_clust_cor,  'van_raw_cor_5', 5,  van_lab, 'address')

van_lab <- labeler(van_raw_clust_eucl,  'van_raw_eucl_2', 2,  van_lab, 'address')
van_lab <- labeler(van_raw_clust_eucl,  'van_raw_eucl_5', 5,  van_lab, 'address')

van_lab <- labeler(van_adj_clust_eucl, 'van_adj_eucl_5', 5, van_lab, 'address')
van_lab <- labeler(van_adj_clust_eucl, 'van_adj_eucl_2', 2, van_lab, 'address')

van_lab <- labeler(van_adj_clust_cor, 'van_adj_cor_5', 5, van_lab, 'address')
van_lab <- labeler(van_adj_clust_cor, 'van_adj_cor_2', 2, van_lab, 'address')

