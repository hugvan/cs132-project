# GitHub setup

Intended repository: `hugvan/cs132-project`.

If the repository has not yet been created, run from the project root:

```bash
git init -b main
git add .
git commit -m "Set up eFOI processing workflow and research portfolio"
gh repo create cs132-project --public --source=. --remote=origin --push
```

Skip initialization/creation steps that have already been completed. Verify with
`git status` and `git remote -v` before running them. Authentication is through
your own GitHub account (`gh auth status`); do not put tokens in the repository.

## Publish the portfolio

In the repository, open **Settings → Pages**. Choose **Deploy from a branch**,
select **main** and **/docs**, then save. The expected project URL is
<https://hugvan.github.io/cs132-project/> once Pages has successfully deployed.
Check the actual URL in Settings → Pages before sharing it.

Equivalent CLI command (requires repository admin access):

```bash
gh api --method POST repos/hugvan/cs132-project/pages \
  -f 'source[branch]=main' -f 'source[path]=/docs'
```

If Pages is already enabled, use the settings UI to verify the source instead
of repeating the creation command. Public repositories can use Pages on GitHub
Free. See [GitHub's official setup instructions](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site).

## Collaborate

Invite the other three members through Settings → Collaborators using their
confirmed GitHub usernames. Work in branches and use pull requests:

```bash
git switch -c docs/collection-method
# Edit and review your files.
git add documentation/methodology.md
git commit -m "Document collection method"
git push -u origin docs/collection-method
```

Only commit intentional files. Raw/interim/processed data are ignored. Invite
collaborators and choose a code license after the team supplies those details.

## Submission freeze

Before submission, complete `submission-checklist.md`, record the commit SHA and
save the PDF snapshot. Do not merge portfolio edits between submission and
checking, per the course guidelines. Continue later work on a separate branch.
