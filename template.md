# About
This tool will daily crawl https://arxiv.org and use LLMs to summarize them.

# How to use
This repo will daily crawl arXiv papers about **cs.CV, cs.GR and cs.CL**, and use **DeepSeek** to summarize the papers in **Chinese**.
If you wish to crawl other arXiv categories, use other LLMs or other language, please follow the bellow instructions.
Otherwise, you can directly use this repo. Please star it if you like :)

**Instructions:**
1. Fork this repo to your own account
2. Go to: your-own-repo -> Settings -> Secrets and variables -> Actions
3. Go to Secrets. Secrets are encrypted and are used for sensitive data
4. Create two repository secrets named `OPENAI_API_KEY` and `OPENAI_BASE_URL`, and input corresponding values.
5. To enable email notifications, add the following repository secrets:
   - `SMTP_SERVER`: address of your SMTP server
   - `SMTP_PORT`: port of your SMTP server, such as `465`
   - `SMTP_USERNAME`: username of the email account used to send messages
   - `SMTP_PASSWORD`: password or app token for the email account
   - `RECIPIENT_EMAIL`: address that will receive the daily Markdown
6. Go to Variables. Variables are shown as plain text and are used for non-sensitive data
7. Create the following repository variables:
   1. `CATEGORIES`: separate the categories with ",", such as "cs.CL, cs.CV"
   2. `LANGUAGE`: such as "Chinese" or "English"
   3. `MODEL_NAME`: such as "deepseek-chat"
   4. `EMAIL`: your email for push to github
   5. `NAME`: your name for push to github
   6. `RESEARCH_INTERESTS`: keywords used to sort papers. A LLM ranks each paper by how well it matches these interests, e.g. `AIGC, 视频生成, 视频编辑, Diffusion`
8. Go to your-own-repo -> Actions -> arXiv-daily-ai-enhanced
9. You can manually click **Run workflow** to test if it works well (it may takes about one hour).
By default, this action will automatically run every day
You can modify it in `.github/workflows/run.yml`
10. If you wish to modify the content in `README.md`, do not directly edit README.md. You should edit `template.md`.

# Content
{readme_content}

# Related tools
- ICML, ICLR, NeurIPS list: https://dw-dengwei.github.io/OpenReview-paper-list/index.html

# Star history

[![Star History Chart](https://api.star-history.com/svg?repos=dw-dengwei/daily-arXiv-ai-enhanced&type=Date)](https://www.star-history.com/#dw-dengwei/daily-arXiv-ai-enhanced&Date)
