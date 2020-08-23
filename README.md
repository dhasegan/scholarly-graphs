Download each list of users one by one.

For example:

    mkdir google_scholar4
    py download.py run articles3.csv google_scholar3/
    py download.py run articles4.csv google_scholar4/

Then use all the pages to compile the final page

    py display.py run google_scholar/,google_scholar2/,google_scholar3/,google_scholar4/ display.html

You can use this to find coauthors

    py parse.py coauthors google_scholar/ articlesX.csv 

Sources Note:
- 1: from brain inspired
- 2: from coauthors of brain inspired
- 3: from local finds and personal interests
- 4: from Megan Peters recommendation
