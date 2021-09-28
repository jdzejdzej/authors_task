# Data Engineering @ PeakData - Jedrzej Jaskolski solution

# How to run 
## requirements
    * python3.8
    * pipenv
## running
    pipenv sync
    pipenv run python main.py --path "path to csv"

# Approach
I'll try to describe the steps I took in order to finish the task.
My thinking has changed many times when solving the problem, 
so the steps can seem a bit chaotic.

### Browse the data
I've checked random entries from provided csv, but the collection is too big to analyse it manually.
To better understand the data I decided to divide candidates by their last name.
This was my first assumption - the last word in author name is surname.
Using this grouping, first challenges appeared:
 * `Beatrice J Edwards`, `Ceiridwen J Edwards`, `J Edwards` - Is `J Edwards` 
   another author or one of previous?
 * `Hans-Uwe Simon`, `H U Simon`, `H Simon` - are they the same person?
 * Should I add to final list names like `S W Kohler` ?
 * are dashes important?  Can I split by `-`?
 * What to do with `l-l`, `a.`, `k-d` abbreviations?

### Searching
Because the number of questions was rising, I decided to google the problem of name matching.
There is a python library that suppose to solve the whole problem - `hmni`, 
machine learning pretrained model. Unfortunately after few tries it wasn't working on my pc - too much 
heavy dependencies, no time to waist. I looked up also to fuzzywuzzy library but after few experiments 
it wasn't for me(at least to do in 4 hours). I decided to tailor my own solution. 
At this point I knew my solution will be working only for some cases.
For me it was more important to deliver something than searching for best solution.
  
### Implementation
After some considerations I decided to meet task example output - 
my goal was to generate csv with firstname and lastname (even if the author has more tha one name).

I grouped the data by lastname and applied some rules to select first name 
(or none - I decided to skip entries like `S W koh` because expanding potential names 
was too time-consuming, and I even didn't know how to approach this in given time).

Firstname rules:
* should be longer than 1 word
* names shorter than 4 should contains only letters (excluding p-p, a.b., ...)
* don't accept common prefixes (md, ll, van, der, la, ...)
* select first name from the candidate that matches the rules, in other case drop candidate

This rules in general should select the first solid name from the string, for example:
* `J Arjuna Ratnayaka` -> `Arjuna Ratnayaka`
* `R H Watkins` -> skip
* `Celine Noha Isabelle Haller` -> `Celine Haller`
* ...

### Loose ends
The solution is skipping a lot of names which should be probably in the final list 
(`B C Adelmann-Grill`, `M Giacca`, ...)

The final list is also raising questions - Should the `Stephan` and `Stephen` be treated as the same name?
If yes, then what other names are the same?


# Considerations
This task is very complex and in general it's hard to tailor 100% accurate solution.
Reading a bit about this problem make me thinking that ruled-based approach won't be enough, 
and definitely not a nice solution. If I had much more time I would try to prepare solution 
based on rules, dictionary with names, abbreviations and alternatives 
to each name, and use methods of nlp.

# Before production
Some things need to be done before going with this to production
* unit tests (Not enough time to write them) !
* add logging
* handle exceptions
* add end-to-end tests
* Think of something better :) 


