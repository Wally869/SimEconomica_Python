# SimEconomica_Python   



## Current Development  
- Issues with production process: stuck with only initial trades for basic resources and nothing on secondary market.   
so either problem with production thingy, or is problem with market not looping    
actually was fixed because of error in GetProductionCapacity (was checking wrongly: temp < capacity, with no check if capacity != 0)  
still not good I think? will have to check   
- Need to set function to define buying/selling prices and quantities  
