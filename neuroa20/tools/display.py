import json
import os
import fire

def html(content):
    return """
<html lang="en"><head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="dhasegan">
    <link rel="icon" href="/docs/4.0/assets/img/favicons/favicon.ico">

    <title>Starter Template for Bootstrap</title>

    <!-- Bootstrap core CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">

  <body>

    <main role="main" class="container">
        {}
    </main><!-- /.container -->

    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
</body></html>
""".format(content)


# "title": "Exact solutions to the nonlinear dynamics of learning in deep linear neural networks",
# "cites": "9090095758382098911",
# "year": "2013",
# "url": "https://arxiv.org/abs/1312.6120",
# "author": "Andrew M Saxe and James L McClelland and Surya Ganguli",
# "journal": "arXiv preprint arXiv:1312.6120",
# "abstract": "Despite the widespread practical success of deep learning methods, our theoretical understanding of the dynamics of learning in deep neural networks remains quite sparse. We attempt to bridge the gap between the theory and practice of deep learning by systematically analyzing learning dynamics for the restricted case of deep linear neural networks. Despite the linearity of their input-output map, such networks have nonlinear gradient descent dynamics on weights that change with the addition of each new hidden layer. We show that deep linear networks exhibit nonlinear learning phenomena similar to those seen in simulations of nonlinear networks, including long plateaus followed by rapid transitions to lower error solutions, and faster convergence from greedy unsupervised pretraining initial conditions than from random initial conditions. We provide an analytical description of these phenomena by finding new exact solutions to the nonlinear dynamics of deep learning. Our theoretical analysis also reveals the surprising finding that as the depth of a network approaches infinity, learning speed can nevertheless remain finite: for a special class of initial conditions on the weights, very deep networks incur only a finite, depth independent, delay in learning speed relative to shallow networks. We show that, under certain conditions on the training data, unsupervised pretraining can find this special class of initial conditions, while scaled random Gaussian initializations cannot. We further exhibit a new class of random orthogonal initial conditions on weights that, like unsupervised pre-training, enjoys depth independent learning times. We further \u2026",
# "eprint": "https://arxiv.org/pdf/1312.6120"

def _row_id(row):
    return row['name'].lower().replace(' ', '_')

def _display_pub(pub):
    bib = pub['bib']
    year = bib['year'] + ', ' if 'year' in bib else ''
    return """
    {}{}
    <span class="badge badge-primary badge-pill">{}</span>
""".format(year, bib['title'], bib['cites'] if len(bib['cites']) < 6 else '-')


def _display_row(row):

    tp_li_start = '<li class="list-group-item d-flex justify-content-between align-items-center">'
    top_papers = '\n'.join([
        ''.join([tp_li_start, _display_pub(pub), '</li>']) for pub in row['publications'][:10]])

    sort_by_year = lambda arr: sorted(
        arr,
        key=lambda pub: int(pub['bib']['year']) * 1000 + min(int(pub['bib']['cites']), 999) if 'year' in pub['bib'] and 'cites' in pub['bib'] else 0,
        reverse=True)
    latest_papers = '\n'.join([
        ''.join([tp_li_start, _display_pub(pub), '</li>']) for pub in sort_by_year(row['publications'])[:10]])

    first_year_published = 999999
    for pub in row['publications']:
        if 'year' in pub['bib'] and first_year_published > int(pub['bib']['year']):
            first_year_published = int(pub['bib']['year'])
    first_year_published_html = "<h5> Starting year: {} </h5>".format(first_year_published) if first_year_published < 999999 else ''

    i_li_start = '<li class="list-group-item">'
    interests = '\n'.join([
        ''.join([i_li_start, interest, '</li>']) for interest in row['interests']])


    brain_inspired = ''
    if 'brain_inspired' in row:
        brain_inspired = '<h5> <a href="{}"> {} </a> </h5> <p> {} </p>'.format(
            row['brain_inspired']['link'],
            row['brain_inspired']['title'],
            row['brain_inspired']['text'])

    notes = ''
    if 'notes' in row:
        notes = '<h5> Notes </h5> <p> {} </p>'.format(row['notes'])

    return """
    <h1 id='{}'> {} </h1>
    <h3> {} </h3>
    <h6> cited: {} (5y: {}); hindex: {} </h6>
    {}

    <div>
        <h6> Interests </h6>
        <ul class="list-group list-group-flush">
            {}
        </ul>
    </div>

    <div>
        {}
    </div>

    <div>
        {}
    </div>

    <div>
        <h6> Top Papers </h6>
        <ul class="list-group">
            {}
        </ul>

        <h6> Latest Papers </h6>
        <ul class="list-group">
            {}
        </ul>
    </div>

    """.format(_row_id(row), row['name'], row['affiliation'], row['citedby'], row['citedby5y'], row['hindex'],
        first_year_published_html, interests, brain_inspired, notes, top_papers, latest_papers)

def _display_coauthors(coauthors):
    displayed = ''
    for _, details in coauthors:
        displayed += """
            <li class="list-group-item d-flex justify-content-between align-items-center">
                {} - {} 
                <span class="badge badge-primary badge-pill">{}</span>
            </li>
        """.format(details['name'], details['affiliation'], len(details['links']))

    return """
    <div id='coauthors'>
        <h1> All Coauthors </h1>
        <ul class="list-group">
            {}
        </ul>
    </div>
    """.format(displayed)

def _display_link(url, text):
    return """
    <button type="button" class="btn btn-link">
        <a href="{}"> {} </a> 
    </button>
    <br/>""".format(url, text)

def run(input_dirs, output_file, sort_mechanism='citedby'):
    if type(input_dirs) == str:
        input_dirs = input_dirs.split(',')
    files = [os.path.join(input_dir, file) for input_dir in input_dirs for file in os.listdir(input_dir)]

    rows = []
    for filename in files:
        with open(filename) as f:
            row = json.load(f)
            rows.append(row)

    rows = sorted(rows, key=lambda x:x[sort_mechanism], reverse=True)
    rows_names = [r['name'] for r in rows]

    coauthors = {}
    for row in rows:
        for coauthor in row['coauthors']:
            ca_id = coauthor['name'] + coauthor['affiliation']
            if ca_id not in coauthors and coauthor['name'] not in rows_names:
                coauthors[ca_id] = {
                    'name': coauthor['name'],
                    'affiliation': coauthor['affiliation'],
                    'links': []
                }
            if ca_id in coauthors:
                coauthors[ca_id]['links'].append(row['name'])

    coauthors = sorted(list(coauthors.items()), key=lambda x:len(x[1]['links']), reverse=True)

    content = ''
    with open(output_file, 'w') as out:
        content += '\n'.join([
            _display_link('#' + _row_id(row), '{}: {} ({})'.format(idx+1, row['name'], row['citedby']))
            for idx,row in enumerate(rows)] + [_display_link('#coauthors', '=== Coauthors ===')])

        content += '\n'.join([_display_row(row) for row in rows])

        content += '<br/>  <br/>  <br/> ' + _display_coauthors(coauthors)

        out.write(html(content))


if __name__ == '__main__':
    fire.Fire({
        'run': run
    })