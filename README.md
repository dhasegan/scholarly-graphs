# Setup

1. Add PYTHONPATH to `.bash_profile`:

        export PYTHONPATH="$PYTHONPATH:$HOME/Dropbox/Education/2020 Neuroscience apply/"

        alias ll='ls -al'
        alias ve='source venv/bin/activate'
        alias py='python3'

2. Install packages

        virtualenv --system-site-packages -p python3 ./venv

        ve

        pip install -r requirements.txt

# Download

Download each list of users one by one.

For example:

    mkdir google_scholar4
    py neuroa20/tools/download.py run articles3.csv google_scholar3/
    py download.py run articles4.csv google_scholar4/

Then use all the pages to compile the final page

    py neuroa20/tools/display.py run google_scholar/ display.html

### You can use this to find coauthors

    py neuroa20/tools/parse.py coauthors google_scholar/ data/.csv

### Create table for viewing the graphs

    py neuroa20/tools/graph.py create_table \
        google_scholar/ \
        noded3/files/email_filter.tsv \
        --email-filter True

    py neuroa20/tools/graph.py create_table \
        google_scholar/ \
        noded3/files/megan_peters.tsv \
        --person-filter "Megan A. K. Peters" \
        --person-filter-count 3

    py neuroa20/tools/graph.py create_table \
        google_scholar/ \
        noded3/files/nyu_dope0.tsv \
        --list_filename_filter data/nyu/faculty.csv \
        --list_filename_filter_count 0
