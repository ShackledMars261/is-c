# Example Service
A example service to serve as a template for how to use the InterScript-Communications server.

Contains a single listener that broadcasts a random with the "Number-Result" event once it recieves the event "Generate-Number" with the data shown below
```
Event: Generate-Number
{
    "lowerBound": int,
    "upperBound": int
}

Event: Number-Result
{
    "lowerBound": int,
    "upperBound": int,
    "result": int
}
```