# About
This tool will daily crawl https://arxiv.org and use LLMs to summarize them.

After enabling GitHub Pages on your fork, open it at: `https://<username>.github.io/<repo>/`

# How to use
This repo will daily crawl arXiv papers about **cs.CV, cs.GR and cs.CL**, and use **DeepSeek** to summarize the papers in **Chinese**.
If you wish to crawl other arXiv categories, use other LLMs or other languages, please follow the bellow instructions.
After deployment, you can use your own fork at `https://<username>.github.io/<repo>/`.

**Instructions:**
1. Fork this repo to your own account
2. Go to: your-own-repo -> Settings -> Secrets and variables -> Actions
3. Go to Secrets. Secrets are encrypted and are used for sensitive data
4. Create two repository secrets named `OPENAI_API_KEY` and `OPENAI_BASE_URL`, and input corresponding values.
5. Go to Variables. Variables are shown as plain text and are used for non-sensitive data
6. Create the following repository variables:
   1. `CATEGORIES`: separate the categories with ",", such as "cs.CL, cs.CV"
   2. `LANGUAGE`: such as "Chinese" or "English"
   3. `MODEL_NAME`: such as "deepseek-chat"
   4. `EMAIL`: your email for push to github
   5. `NAME`: your name for push to github
   6. `DATA_BRANCH`: optional; branch used to publish generated data files. Defaults to "data"
7. Go to your-own-repo -> Actions -> arXiv-daily-ai-enhanced
8. You can manually click **Run workflow** to test if it works well (it may takes about one hour). 
By default, this action will automatically run every day
You can modify it in `.github/workflows/run.yml`
9. If you wish to modify the content in `README.md`, do not directly edit README.md. You should edit `template.md`.
10. Set up GitHub Pages: Go to your own repo -> Settings -> Pages. In `Build and deployment`, set `Source="Deploy from a branch"` and choose your repository default branch with folder `/(root)`. If you renamed the repository, your Pages URL will become `https://<username>.github.io/<repo>/`.

# To-do list
- [x] Replace markdown with GitHub pages front-end.
- [ ] Bugfix: In the statistics page, the number of papers for a keyword is not correct.
- [ ] Update instructions for fork users about how to use github pages.

# Content
{readme_content}

# Related tools
- ICML, ICLR, NeurIPS list: deploy the companion OpenReview paper list project separately if you need it.

# Star history
If you want a star history badge for your fork, replace `<username>/<repo>` below with your own repository path:
`https://api.star-history.com/svg?repos=<username>/<repo>&type=Date`
