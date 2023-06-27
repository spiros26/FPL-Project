# FPL Copilot

![Alt text](./data_flow.png?raw=true)


## Description

An open-source, full-scale Fantasy Premier League model.
The system was designed to: 

- Predict the EV (Expected Value)
- Generate optimal transfer paths
- Contribute to the FPL Analytics
  
## Installation
- Python Version: 3.9.5
- `pip install -r requirements.txt`
- Highs solver already there, Download cbc solver if you choose

## Data Sources

1. Fantasy Premier League API
2. [Understat](https://understat.com/) 
3. [Vaastav’s GitHub repo](https://github.com/vaastav/Fantasy-Premier-League)
4. [FiveThirtyEight](https://fivethirtyeight.com/)
5. [Chris Musson’s ID Map](https://github.com/ChrisMusson/FPL-ID-Map)

## Solver
I used a version of Sertalp's [solver](https://github.com/sertalpbilal/FPL-Optimization-Tools) that I personally integrated with the rest of the project and modified in some ways.

## Results
![Screenshot 2023-06-27 173707](https://github.com/spiros26/FPL-Project/assets/71256846/f6f627b5-44cb-46ad-87af-43e5c86da653)

![models_bubbleplot](https://github.com/spiros26/FPL-Project/assets/71256846/cee791eb-ac0d-4455-a6ce-88fe4ea1ecb0)

## The FPL Team managed by the model, got the #1 Place in the GW24 League (>25000 teams) - season:2022/23

![gw24](https://github.com/spiros26/FPL-Project/assets/71256846/49f5043c-52ad-4ad7-9b20-1c5437ce2143)

![AITeam](https://github.com/spiros26/FPL-Project/assets/71256846/9e138e88-c991-4bdd-b358-681c845efbd3)


## Future Work

- Home advantage not clearly depicted due to data collection during Covid-19 (empty stadiums)
- Separate project about xMins (expected minutes) prediction: one of the most important features
- Separate models for high performing players
- Deep Learning techniques: Explore the effect on predictive power
- Heuristics for faster solves: Sacrifice accuracy/optimality for speed


## Acknowledgements
I would like to express my appreciation to Sertalp, FPL Kiwi, Chris Musson, Owen, Fantasy Football Trout, and all the other members of the FPL community who have generously shared their knowledge, insights, and experiences. Their contributions and discussions have played a significant role in shaping my understanding of the subject matter and achieving my goals.


**My Google Slides presentation:** [Presentation](https://docs.google.com/presentation/d/1OXzX-5xrvi5fKxBk613t66wvC10UwuWqj6A1C8JHtVU/edit?usp=sharing)


**Contact Me:** [Spiros Valouxis - Twitter](https://twitter.com/SpirosValouxis "Twitter")
