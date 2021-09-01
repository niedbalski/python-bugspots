# Bughotspots

A Python based implementation of the bug prediction algorithm proposed by Google:  
[Bug Prediction at Google](http://google-engtools.blogspot.com/2011/12/bug-prediction-at-google.html)

## Example usage

Move to the repository directory  

```console
    $ bughotspots .

    Scanning ../app2 repo, branch:master
    Found 490 bugfix commits on the last 60 days

Fixes
--------------------------------------------------------------------------------
      -Pull request #784: fix(something): update left offset value for help text
      -fix(something): update left offset value for help text
      -Pull request #783: fix(iframe.js): added display = block after stylesheets removal
      -fix(iframe.js): added display = block after stylesheets removal
      -Pull request #782: fix(iframe.js): AB-9155 - prevented removal of custom style
      -fix(iframe.js): AB-9155 - prevented removal of custom style
      -Pull request #779: fix(feature): copy changes
      -fix(feature): copy changes
      -Pull request #777: Fix: Updated image is not visible on reloading the feature due to lazy loading
      -fix(feature): keypress - esc / when el is not set
      -fix(eslint): app eslint resolve
      -fix(feature): clubbed f1 & f2 toggle logic | limitSelection for 3 dots
      -fix(AB-9045): handle effected pages
      -Merge branch 'master' into AB-9045
      -fix(AB-9045): handle effected pages
      -fix(feature): merging master
      -fix(feature): move event handler in utils
      -f.......

Hotspots
--------------------------------------------------------------------------------
      8.96 = app/feature/js/file1.js
      3.20 = app/feature/js/operations/file2.js
      3.07 = app/feature/js/operations/file3.js
      2.99 = package.json
      2.86 = app/feature/js/operations/file4.js
      2.28 = app/feature/js/file5.js
      2.22 = app/modules/feature/file6.js
      2.18 = app/modules/feature/file7.js
      1.95 = app/feature/js/operations/file8.js
      1.88 = app/feature/js/file9.js
```

Scores mentioned in the Hotspots section are specific to the files and depict the rate of frequecny with which the file encounters errors and bug fixes. The higher the score, the more erroneous the file commit history.

## Parameters supported

| Optional Argument | Description                                                                   | Example usage                         |
|-------------------|-------------------------------------------------------------------------------|---------------------------------------|
| -h, --help        | Shows the help dialog describing usage                                        | bughotspots --help                       |
| --days            | Days ago to compute bug factor, default value: 30                             | bughotspots --days 60                    |
| --limit           | Max amount of results to show, default value: 10                              | bughotspots --limit 100                  |
| --branch          | Use a specific branch, default value: 'master'                                | bughotspots --branch feature-branch      |
| --bugsFile        | Use a file with list of bugs to search in commits, default to searching commits with QF issues mentioned                             | bughotspots --bugsFile bugs.csv          |
| --paths           | Provide repository paths to look into, default to search in current directory | bughotspots --paths ../app2 ../app1 |

## Build process

Build through setup.py

```bash
python setup.py build
```

Install the build

```bash
python setup.py install
```

Execution after installation

```bash
bughotspots --paths app2 app1 --days 60 --bugsFile bugIDs.csv --limit 100
```
