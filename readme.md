Inspried from: 
https://medium.com/@meeusdylan/extracting-kindle-highlights-1e5308fcda77

Prerequisites:
- python3
- selenium (pip install selenium)

Resolved some of the issues faced with the scripts mentioned in above article.
Issues seems to be with Python version changes and minor changes in kindle portal. 
Currently repo mentioned in that page seems to be not available. Hence re-written and fixed the issues. 

### Sync kindle highlights to a local json file.
Syntax: python get_highlights.py kindle-username kindle-password

This writes the output file kindle-books-highlights.json. 

### Random Quote
To show a random quote, run random-quote.py

Syntax: python random-quote.py <kindle-books-highlights.json file path>  

To display a random quote whenever I open a terminal, installed cowsay application in terminal 
Copy kindle-books-highlights.json to home folder (~/).

Add below lines to ~/.bashrc file
```
alias qclear="clear;python3 random-quote.py ~/kindle-books-highlights.json | cowsay"
python3 random-quote.py ~/kindle-books-highlights.json | cowsay
```

Instead of clear, I use qclear (an alias created and added in bashrc) to clear the screen and display a random quote on the top of the screen. 

Note: For these changes in .bashrc to take place, restart terminal.
