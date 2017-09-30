This is a small project trying to predict the user reputations from Stackoverflow with regression models. It uses features derived from graph mining techniques, particularly graph centrality measures.


## Dependencies
This project depends on graph-tool ([https://graph-tool.skewed.de/]) and keras.

## Workflow

1. Download Stackexchange dumps from [https://archive.org/details/stackexchange]
2. Create graphs runnning `extract.py` from inside the Stack Exchange folder
3. Create graph features running `centrality.py`
4. Running `analyse.py` given a features file will create various singlevariate regressions as well asa multivariate regression and a neural network regression. It also tries to predict other networks with the learned regression model
