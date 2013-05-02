# Code Switch

## Getting Started: Git management
Clone this repository, then delete the .git folder like this:

```
rm -rf .git
```

You can initialize this as a new git repository like this:

```
git init
```

And then follow the instructions on GitHub for creating a new repository.

## Getting Started: Editing files

This site is entirely static. Using fab <target> <branch> deploy will deploy the static assets from www/ to S3.

## Getting Started: Viewing the site

You can view the site locally like this:
```
cd www/
python -m SimpleHTTPServer
```

In your Web browser, the site is visible at `http://127.0.0.1:8000/` which will load `index.html`.
