# Bughotspots

A Python based implementation of the bug prediction algorithm proposed by Google:  
[Bug Prediction at Google](http://google-engtools.blogspot.com/2011/12/bug-prediction-at-google.html)

## Example usage

Move to the repository directory  

```bash
    $ bughotspots .

    Scanning ../app2 repo, branch:master
    Found 490 bugfix commits on the last 60 days

Fixes
--------------------------------------------------------------------------------
      -Pull request #784: fix(codeMirrorHelp): update left offset value for help text on codemirror editor
      -fix(codeMirrorHelp): update left offset value for help text on codemirror editor
      -Pull request #783: fix(inject-topframe.js): added display = block after stylesheets removal
      -fix(inject-topframe.js): added display = block after stylesheets removal
      -Pull request #782: fix(inject-topframe.js): QF-9155 - prevented removal of plugin custom style during mobile mode load
      -fix(inject-topframe.js): QF-9155 - prevented removal of plugin custom style during mobile mode load
      -Pull request #779: fix(editor): copy changes
      -fix(editor): copy changes
      -Pull request #777: Fix: Updated image is not visible on reloading the editor due to lazy loading
      -fix(editor): keypress - esc / when el is not set
      -fix(eslint): app eslint resolve
      -fix(editor): clubed monitorMutation & refreshElements toggle logic | limitSelection for 3 dots
      -fix(QF-9045): handle effected nodes mutations in dom-footprint
      -Merge branch 'master' into QF-9045
      -fix(QF-9045): handle effected nodes mutations in dom-footprint
      -fix(editor): merging master
      -fix(editor): move bindPasteListener handler in vendor-utils
      -f.......

Hotspots
--------------------------------------------------------------------------------
      8.96 = app/editor/js/designer.js
      3.20 = app/editor/js/operations/AddElementOperation.js
      3.07 = app/editor/js/operations/ImageOperation.js
      2.99 = package.json
      2.86 = app/editor/js/operations/ContentOperation.js
      2.28 = app/editor/js/StateMetadata.js
      2.22 = app/modules/editor/CompatibilityModeBannerController.js
      2.18 = app/modules/editor/CodeEditorController.js
      1.95 = app/editor/js/operations/BaseOperation.js
      1.88 = app/editor/js/globalCode.js
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
