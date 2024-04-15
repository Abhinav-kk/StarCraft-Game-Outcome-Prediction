# StarCraft Game Outcome Prediction

The world of StarCraft is filled with strategic complexities that demand players to make calculated decisions to achieve victory. Predicting the outcome of a StarCraft match accurately has become a topic of immense interest within the gaming community. In this dissertation, we delve into various machine learning and deep learning techniques to uncover the secrets behind successful win-loss predictions in StarCraft matches. By closely analyzing replays from expert-level games, we can train our machine-learning algorithms to recognize visible patterns and strategies that strongly correlate with winning teams. Additionally, integrating relevant in-game data, including player characteristics and battle statistics, enables us to further improve the accuracy and dependability of our prediction models.

In this project we were able to create a pipeline to build a pre-processed dataset from raw .rep, using the dataset extracted build machine learning models to predict game outcomes and also an interactive GUI application where users can enter values for different sets of features and get the win percentage for both players. All the source code in this project is will have GNU General Public V2 license and is published on GitHub.

## Folder Structure

### Dataset Building Scripts
This folder contains scripts used to construct and preprocess the dataset.

- `1) rep to JSON`: Scripts to convert replay files into JSON format.
- `2) JSON to Combined CSV`: Scripts to combine JSON files into a single CSV.
- `3) rgd to set of CSV`: Scripts to convert format (`rgd`) into a set of CSV files.
- `4) Sets of CSV to Single File`: Scripts to convert sets of CSV to a single file.
- `5) Final Processing`: Scripts to perform optional processing on the dataset.

### Overview of Dataset Scripts
Further processing of files is done by different scripts.

- `basicActionsToCSV.py`: Converts basic actions to CSV format.
- `Converter_To_Single.py`: Converts multiple CSV files into a single file.
- `Combine_Replays.py`: Merges replay data into one CSV.
- `Final Processing`: Final data cleaning and preparation scripts.

### Processed Datasets
Processed and cleaned datasets ready for analysis or machine learning.

- `ID_All_ReplaysData_*.csv`: Set of cleaned replay data files, likely categorized by race combination.
- `StarCraft_Combined_Dataset.csv'`: All races combined dataset.

### Project Notebooks
Jupyter notebooks used for data analysis, visualization, and modeling.

- `Dataset_Visualisation.ipynb`: Notebook for visualizing the dataset.
- `Feature_Selection.ipynb`: Notebook for selecting features for the machine learning models.
- `Final Figures Generation.ipynb`: Notebook to generate final figures for reports or presentations.
- `*_Model.ipynb`: Various notebooks for different machine learning models. Models included are Random Forest, k-Nearest Neighbors, Logistic Regression, Support Vector Machines, Long-Short Term Memory, Neural Network.
- `Time_Based_Models.ipynb`: Models which make predictions at different minutes of the game rather than game progression percentile.
- `Predictor_Tool_Models.ipynb`: Notebook used to build the models for StarCraft Winner Prediction tools.

### Winner Prediction Tool
Contains scripts and models related to predicting winners in the dataset.

- `models`: Saved machine learning models for the prediction tool.
- `Scalers`: Saved scaling objects for data normalization.

### models
Saved machine learning models as `.joblib` files for easy loading and tensorflow models are saved using tensorflow's built in save function.

### app
The application layer, containing the main script for executing the prediction tool and any associated utilities.

- `app_main.py`: Main script to run the application.
- `ai_model.py`: Script to run ai models for predicting from user input.
- `requirements.txt`: Lists dependencies for the project to ensure replicability.
- `starcraft-wallpaper.jpg`: Background image for winner prediction tool.

#### Installation

Instructions on setting up the project environment.

```bash
pip install -r requirements.txt
```

#### Usage

Use the following command to run the winner prediction tool.

```bash
python app_main.py
```
## Demo Video of Winner Prediction Tool
<p align="center">
  <a href="https://www.youtube.com/watch?v=GOvOatxa2KY">
  <img src="https://img.youtube.com/vi/GOvOatxa2KY/0.jpg" alt="Demo Video"/>
  </a>
</p>

## VM for Replay Parser using BwRepDump
### [Replay Parser VM Single Download (25.1 GB)](https://heriotwatt-my.sharepoint.com/:u:/g/personal/akk2002_hw_ac_uk/EablqPLOzjdPiUqdYdS1yJgBJWRs4qwmR4G0wTLYst_YKA?e=pO7bDH) <br>
### [Replay Parser VM Split into 11 parts of 2 GB each Zip Files](https://heriotwatt-my.sharepoint.com/:f:/g/personal/akk2002_hw_ac_uk/Ev2Vv_T8rY5MhwbPtXVCNdQBz0njQ59ha6j7l4GBcYbFgg?e=JtvBH5)

## License

This project is licensed with GNU General Public License V2.
