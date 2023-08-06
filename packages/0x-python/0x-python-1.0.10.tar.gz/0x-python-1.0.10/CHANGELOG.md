# Changelog

**0.1.0 : Setup : 5/10/2021**
**0.2.0 : 9/20/2021**
	- updates & testing
**1.0.0 : 9/21/2021**
	- basic operations
	**1.0.1-3**
	- package layout fixes
	**1.0.4**
	- imports cleanup
	**1.0.5-10**
	- package layout final fix? who knows; nobody knows
	

## TODO

- documentation comments





add:

def fill_or_kill_quote
def fill_quotes
def fill_or_kill_quote
def fill_or_kill_quotes
def fill_no_throw_quotes

fillOrder

This is the most basic way to fill an order. All of the other methods call fillOrder under the hood 
with additional logic


fillOrKillOrder 

can be used to fill an order while guaranteeing that the specified amount will either be filled 
or the call will revert.



batchFillOrders 

can be used to fill multiple orders in a single transaction.



batchFillOrKillOrders 

batchFillOrKillOrders can be used to fill multiple orders in a single transaction while 
guaranteeing that the specified amounts will either be filled or the call will revert.



batchFillOrdersNoThrow

batchFillOrdersNoThrow can be used to fill multiple orders in a single transaction while 
guaranteeing that no individual fill throws an error (which would typically cause the entire function call to fail).




### Bugs

