# The Invitae interview homework assignment.

The assignment was to map locations on transcripts onto a genome,
given a set of transcript <-> genome mappings.  The *purpose* of the
assignment, as I understand it, is to get a sense of my bioinformatics
*and* software engineering skills.

> Software engineering is what happens to programming when you add
> time and other programmers.
>
> [Russ Cox](https://research.swtch.com/vgo-eng)

## Bioinformatics

The implementation is (believed to be) correct in the sense that

- it returns the assignment output given the assignment inputs

    ``` python-console
    (.venv) (alice)[19:58:05]nvta-homework>>cat sample_data/transcript_mapping.tsv
    TR1	CHR1	3	8M7D6M2I2M11D7M
    TR2	CHR2	10	20M
    (.venv) (alice)[20:18:25]nvta-homework>>cat sample_data/queries.tsv
    TR1	4
    TR2	0
    TR1	13
    TR2	10
    (.venv) (alice)[20:18:32]nvta-homework>>poetry run hw lift --mf sample_data/transcript_mapping.tsv --qf sample_data/queries.tsv
    TR1	4	CHR1	7
    TR2	0	CHR2	10
    TR1	13	CHR1	23
    TR2	10	CHR2	20
    (.venv) (alice)[20:18:50]nvta-homework>>
    ```

  and;

- it returns reasonable output (including handling "between" locations
  for the inserts) for *all* of the locations on the supplied
  transcripts:

    ``` python-console
    (.venv) (alice)[20:18:50]nvta-homework>>cat sample_data/transcript_mapping.tsv
    TR1	CHR1	3	8M7D6M2I2M11D7M
    TR2	CHR2	10	20M
    (.venv) (alice)[20:22:43]nvta-homework>>cat sample_data/queries_exhaustive.tsv
    TR1	0
    TR1	1
    TR1	2
    TR1	3
    TR1	4
    TR1	5
    TR1	6
    TR1	7
    TR1	8
    TR1	9
    TR1	10
    TR1	11
    TR1	12
    TR1	13
    TR1	14
    TR1	15
    TR1	16
    TR1	17
    TR1	18
    TR1	19
    TR1	20
    TR1	21
    TR1	22
    TR1	23
    TR1	24
    TR2	0
    TR2	1
    TR2	2
    TR2	3
    TR2	4
    TR2	5
    TR2	6
    TR2	7
    TR2	8
    TR2	9
    TR2	10
    TR2	11
    TR2	12
    TR2	13
    TR2	14
    TR2	15
    TR2	16
    TR2	17
    TR2	18
    TR2	19
    (.venv) (alice)[20:22:51]nvta-homework>>poetry run hw lift --mf sample_data/transcript_mapping.tsv --qf sample_data/queries_exhaustive.tsv
    TR1	0	CHR1	3
    TR1	1	CHR1	4
    TR1	2	CHR1	5
    TR1	3	CHR1	6
    TR1	4	CHR1	7
    TR1	5	CHR1	8
    TR1	6	CHR1	9
    TR1	7	CHR1	10
    TR1	8	CHR1	18
    TR1	9	CHR1	19
    TR1	10	CHR1	20
    TR1	11	CHR1	21
    TR1	12	CHR1	22
    TR1	13	CHR1	23
    TR1	14	CHR1	23^24
    TR1	15	CHR1	23^24
    TR1	16	CHR1	24
    TR1	17	CHR1	25
    TR1	18	CHR1	37
    TR1	19	CHR1	38
    TR1	20	CHR1	39
    TR1	21	CHR1	40
    TR1	22	CHR1	41
    TR1	23	CHR1	42
    TR1	24	CHR1	43
    TR2	0	CHR2	10
    TR2	1	CHR2	11
    TR2	2	CHR2	12
    TR2	3	CHR2	13
    TR2	4	CHR2	14
    TR2	5	CHR2	15
    TR2	6	CHR2	16
    TR2	7	CHR2	17
    TR2	8	CHR2	18
    TR2	9	CHR2	19
    TR2	10	CHR2	20
    TR2	11	CHR2	21
    TR2	12	CHR2	22
    TR2	13	CHR2	23
    TR2	14	CHR2	24
    TR2	15	CHR2	25
    TR2	16	CHR2	26
    TR2	17	CHR2	27
    TR2	18	CHR2	28
    TR2	19	CHR2	29
    (.venv) (alice)[20:22:57]nvta-homework>>
    ```

On the other hand, it is not particularly innovative as I took
advantage of the assignment to explore various Python software
engineering nooks and crannies (see below).  I've written "performant"
production versions of this code in Perl+C at Genentech and
contributed to fixing/extending/... the BioPerl coordinate mapping
code, though those projects were designed for smaller, single
genome-ish, data sets.

## Software Engineering

Most of my recent Python experience has been extending and fixing
large Python code bases (e.g. [Spack](https://spack.io)); it's been a
while since I built something *de novo*.  Given the instability of the
Python toolchains and packaging technology I wanted to use the
opportunity to explore some things that have come to my notice:

I consider the following to be important:

- Accurate dependency management; exact versions of dependencies
  should be recorded and ideally "vendored" to provide repeatability.
- Code should follow best practices
  (e.g. [PEP8](https://www.python.org/dev/peps/pep-0008/))
- Code should follow a single coding standard (the details of which
  rarely matter) and automated tests should ensure that that standard
  is followed.
- Test coverage should be included in the automated tests.
- Testings should be automated and run on every push to the
  repositories important branches (including Pull Requests).
  - tests should include "unit-ish" and "integration-ish" test cases
    and include "good" and "bad" inputs.

I'd seen a Python project setup tool (using
[cookiecutter](https://cookiecutter.readthedocs.io/en/latest/)) [by
WeMake Services on lobste.rs](
https://lobste.rs/s/q6ymgl/new_python_project_starter_tool_with) a few
months ago that seemed to meet the above criteria, so I used the
assignment as a chance to take it (and the tooling it sets up) for a
test drive.  It worked out well, and/but

- I swapped GitHub Actions for its Travis Ci.
- I added a `yapf` formatting test.
- `yapf` and `flake8` (using the wemake configuration) don't get along
  very well; for this assignment I simply ignored the problematic
  "bugs" but in production "someone" would need to be better (see my
  comments in back in the [lobste.rs
  thread](https://lobste.rs/s/q6ymgl/new_python_project_starter_tool_with)).
- I didn't bother setting up Sphinx documentation on Read The Docs (
  although I did confirm that the templated docs build and view
  properly).
- I added:
  - [Click](https://click.palletsprojects.com/en/7.x/) to build the
    CLI; and
  - [yapf](https://github.com/google/yapf) for code formatting (I
    explored Black, but it causes even more problems with wemake's
    `flake8` configuration).

Although I was working alone, I followed a
[gitflow](https://nvie.com/posts/a-successful-git-branching-model/)
inspired workflow, each unit of work happened on it's own branch, was
pushed to GitHub, and was merged after its Pull Request passed its
tests.  The [GitHub network
graph](https://github.com/hartzell/nvta-homework/network) gives a nice
graphical overview of the work sequence.

# Features

- uses the [WeMake Services project setup
  tool](https://github.com/wemake-services/wemake-python-package).
  - Uses [Poetry](https://python-poetry.org/) to manage dependencies,
    packaging and development.
    - Uses Sphinx and ReadTheDocs for documentation (*unused*).
  - Uses [Flake8](https://gitlab.com/pycqa/flake8) to check that code
    follows accepted practices and [Doc8](https://launchpad.net/doc8)
    for the documentation.
  - Uses [pytest](https://docs.pytest.org/en/latest/contents.html) for testing.
  - Uses [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/)
    for coverage testing (passing tests require 100% code coverage).
- additionally
  - The code was developed using
    [Yapf](https://github.com/google/yapf) to format files every time
    they're saved.
  - The tests were extended to ensure that they're always in *Yapf
    normal form*.
  - Travis CI tests were replaced with GitHub Actions tests; tests run
    on all pushes (including Pull Requests).

# Installation

This project uses poetry to manage it's dependencies and *etc*....
While poetry makes it simple to upload the project to PyPi, I haven't
done so.

You can build it an run the tests by installing poetry, cloning the
repository from GitHub, cd'ing into the top of the project, running
`poetry install` to install the prerequisites and then running `make
test` to run the tests (the `Makefile` invokes `poetry run`).

```bash
# Install poetry, see https://python-poetry.org/docs/#installation
# clone the repository
git clone https://github.com/hartzell/nvta-homework
cd nvta-homework
poetry install
make test
# given a file of transcript mapping info and a file of queries:
poetry run hw lift --mf transcript_mapping_file.tsv --qf query_file.tsv
```
# License

[MIT](https://github.com/hartzell/nvta-homework/blob/master/LICENSE)


# Credits

This project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [aa39fa83ce92d9572a57fe74ed14464ffb77d9b4](https://github.com/wemake-services/wemake-python-package/tree/aa39fa83ce92d9572a57fe74ed14464ffb77d9b4). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/aa39fa83ce92d9572a57fe74ed14464ffb77d9b4...master) since then.
