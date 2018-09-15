# Gas Price Markets
## Relevant market areas, price leaders and where to invest

*---Proposal Abstract---*

Gas station pump prices, in competitive markets, are determined by the intersect
of supply and demand.

Laws in the US and Canada require review of mergers which might impact any
competitive markets. To do this they must pass a *Hypothetical Monopolist Test*
__CItation Needed__

This involves demonstrating that a monopolist in a relevant market could raise
prices. The relevant market is determined by a mix of product categories and
location. In our case, if a gas station was outside the geographic market, they
would not significantly impact prices of the other market. 

This is



## Description of the Problem
Retail Gas Prices (RGP) are determined in the competitive market. Gas stations
are surprisingly unsophisticated given that the market in Canada is [$34
billion](https://www.ibisworld.ca/industry-trends/market-research-reports/retail-trade/gas-stations.html). If pricing is granular it is almost entirely set by regional or
even station managers and national campaigns do not have the granularity to
capitalize on market differences.

There are many facets that go into the definition of a competitive market.
Cataloguing all features and recording them is a gargantuan task. Instead this
study hopes to discern which stations may be different from their surrounding
competition. This will allow more targeted experimentation.



The competition is based on many factors like loyalty programs, marketing,
customer preferences etc. One major influence on RGP is geographic
location. Even within the same distribution market (same base fuel price), a
station on a major highway, one in close proximity to three other competitors
and one in a rural area will all behave differently.



Gas stations are generally unsophisticated in their approach to pricing. There
needs to be a way to 

## Why the problem is interesting

There is aproximetly [$50 billion L](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=2310006601) of motor fuels sold in Canada yearly.
$\50,000,000,000L \cdot \alpha$ where $\alpha$ is small increase in cents per
litre (CPL) is still a lot of money. 

Beyond the fiscal incentives, this is an interesting study because it will
reveal (hopefully) two findings. The first is finding relevant markets in
geographic areas. For example, it is easy to believe that gas stations on
different sides of a major river or other barrier would price differently.

Secondly, after geographic markets are found, gas stations that are contained
within the market but behave differently can be further analyzed. For example, a
suburban area may be a well defined market with similar price fluctuation in
stations except for one. This will allow an analyst to further investigate this
one station to find which features make it more profitable (or less). 

These findings could help set prices more efficiently as well as indicate which
areas are best for future investment. 


## What other approaches have been tried

Investigating retail gasoline markets is nothing new. Most recently in Canada,
[Parkland](https://www.parkland.ca/en/our-businesses/retail/) has a large market of retail stations and merged with [Pioneer
Energy](https://en.wikipedia.org/wiki/Pioneer_Energy) based in Ontario. The [Competition Bureau](http://www.competitionbureau.gc.ca/eic/site/cb-bc.nsf/eng/04053.html) forced Parkland
to divest several stations they believed would form regional monopolies. 

I am also sure marketing departments have segmented promotional efforts based on
location. 

Both of these focus on a more macro level geography.

There are many examples of spatial/temporal regression investigating gas prices
in the economic literature. Some of these are quite granular, although I was
unable to find any on the same scale as I plan. 

Further these look at the causal effect of distance on price. My intention is to
cluster sites and compare them to other clustering techniques such as KNN


## Discussion on your hypothesis is and how your specific solution will improve

My hypothesis is that there are anomalous gas stations and unobserved
sub-regions which can be detected through variance spatial/temporal pricing.

Further, due to my disinterest in causality/interpretation I can use also use
non-linear techniques that make interpretation difficult.

My first approach will be to use [PySal](https://www.earthdatascience.org/tutorials/intro-to-spatial-regression/) to investigate linear relationships
between stores and cluster them by similarity to their prices.

I also plan on investigating other correlation/regression techniques with
numbers weighted by distance.

After getting a functioning model, I plan on comparing this to clustering
algorithms such as KNN with a similar number of centroids to the previous model.
I will then compare the overlap to the model taking into account price.

### Additional Features
I also plan on taking in historic prices for the area on an anualized basis.
This, along with weather, holiday and macroeconomic information will be added
to try and remove omitted variable bias.

### Data Acquisition

I plan on using a scraping script, AWS Lambda and S3 to find current gas prices
in Western Canada. Other data like historic weather conditions and gas prices,
will be found from Stats Can. 

Locational data will be scraped from google maps API.


## Additional Info

