Notes from actually trying stuff:
- Specifying "less than 200 lines" seemed to cause wild overestimates for complexity (ie 100+ lines for prime number function)
- Pushing it towards class-based too much - need to allow bare functions
- Expected output format needs to be painfully clear - how to handle dependencies, whether "desc" and "funcs" are needed, fact that you can/can't do "classname:" "desc".. etc
	- Way of handling deps cannot duplicate deps.
- Need to request output in a single code block
- Find way to get rid of this type of message:
	- `'A few lines to a small function', as the Sieve of Eratosthenes is a simple algorithm with a clear mathematical implementation.`
- Get rid of 'or's