# MPI-prime-checker
MPI app for Computer Structure II Class at Universidad del Norte.

## Project Description:

Given 3 parameters: K (Number of digits), N (Number of processes), Q (Input)

**When Q=0**, Each process verifies a list of 10 numbers until it finds a prime of K digits, at that moment it sends the root process the number and stops receiving. At the end print the primes found and the execution time.

**When Q=1**, Each process verifies lists of 10 numbers checking primality until the root runs out of numbers of K digits. A the end print the number of packages verified by each process, the total number of prime numbers found and the execution time.

# How to use
In the project folder run:

`docker run -d -it --name mpicont -v "$(pwd)"/target:/app augustosalazar/un_mpi_image:v5`

Copy the file [primerChecker.py](./primerChecker.py) to ./target
# Execution
`docker exec -it mpicont mpiexec --oversubscribe --allow-run-as-root -n <# Processes> python /app/primerChecker.py <K> <Q>`

## Example:

`docker exec -it mpicont mpiexec --oversubscribe --allow-run-as-root -n 3 python /app/primerChecker.py 5 1`

Verifies primality for all 5 digit numbers
