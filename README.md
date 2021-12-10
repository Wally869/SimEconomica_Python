# SimEconomica_Python   

Implementation of the "Emergent Economies for Role Playing Games" model in Python.  
The model implements a videogame-like economy where actors have resources and can craft objects before selling them on the market.  
Actors decide on a price to buy or sell a given good depending on their price belief (price is drawn within a range).  

An important feature of the model is that markets are implemented as Double Auctions. Buyers and sellers receive imperfect information in return: the quantity they manage to trade compare to what they wanted and the clearing price.  

Given this imperfect information, traders adjust their price beliefs (raising or lowering boundaries of their price belief ranges). Traders also have a given starting capita and go bankrupt once they reach 0. When a trader goes bankrupt, a new one is added to the market with the highest recorded profitability.  

The initial paper shows that, depending on Simulation parameters, the global market reaches a state of equilibrium and even large external shocks get resorbed over time therefore showing the Invisible Hand at work.  

This repository has several objectives:  
- Reimplement the initial model described in the paper   
- Expand on the initial model with added complexity (different cities/regions, add currencies, different behaviour models for traders)  
- Expose a convenient data-based approach (easy to add/modify objects and recipes, tunable parameters)  
- Serve as a base for a Golang port for more complex simulations  


## Current Development  
- Issues with production process: stuck with only initial trades for basic resources and nothing on secondary market.   
so either problem with production thingy, or is problem with market not looping    
actually was fixed because of error in GetProductionCapacity (was checking wrongly: temp < capacity, with no check if capacity != 0)  
still not good I think? will have to check   
- Need to set function to define buying/selling prices and quantities  

## Logic  

### Setup 
- Start by defining a list of resources/objects which can be harvested or crafted  
- Create "recipes" for crafting  


### Running  
