# Setup

1. Add PYTHONPATH to `.bash_profile`:

        export PYTHONPATH="$PYTHONPATH:$HOME/Dropbox/Education/2020 Neuroscience apply/"

        alias ll='ls -al'
        alias ve='source venv/bin/activate'
        alias py='python3'

2. Install packages

        brew install geckodriver

        virtualenv --system-site-packages -p python3 ./venv

        ve

        pip install -r requirements.txt

# Download

Download each list of users one by one.

For example:

    mkdir google_scholar4
    py neuroa20/tools/download.py run articles3.csv google_scholar3/
    py download.py run articles4.csv google_scholar4/


    py neuroa20/tools/download.py run data/ucla/neuro_profs.csv google_scholar/ \
        --patterns ucla

Then use all the pages to compile the final page

    py neuroa20/tools/display.py run google_scholar/ display.html

    py neuroa20/tools/display.py run google_scholar/ display.html \
        --filter_file data/new-2021/faculty.csv

### You can use this to find coauthors

    py neuroa20/tools/parse.py coauthors \
        google_scholar/ \
        data/other/profs_hakwan_coauthors.csv \
        --list_filename_filter data/other/profs_hakwan_meetup.csv \
        --min_links 1

    py neuroa20/tools/download.py run \
        data/other/profs_hakwan_coauthors.csv \
        google_scholar/ \
        --download_on_exact_name True


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

    py neuroa20/tools/graph.py create_table \
        google_scholar/ \
        noded3/files/hakwan_meetup.tsv \
        --list_filename_filter data/other/profs_hakwan_meetup.csv \
        --list_filename_filter_count 1

    py neuroa20/tools/graph.py create_table \
        google_scholar/ \
        noded3/files/new_2021.tsv \
        --list_filename_filter data/new-2021/faculty.csv \
        --list_filename_filter_count 1

### Start server

    cd noded3
    python3 -m http.server 9000
