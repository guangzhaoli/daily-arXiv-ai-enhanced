import json
import argparse
import os
import sys
from itertools import count

from pydantic import BaseModel, Field
import langchain_core.exceptions
from langchain_openai import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, help="Path to the jsonline file")
    args = parser.parse_args()
    data = []
    preference = os.environ.get('CATEGORIES', 'cs.CV, cs.CL').split(',')
    preference = list(map(lambda x: x.strip(), preference))
    interests = os.environ.get('RESEARCH_INTERESTS', '').split(',')
    interests = [i.strip() for i in interests if i.strip()]
    none_rank = len(interests)

    class Rank(BaseModel):
        rank: int = Field(description="index of best matching interest")

    if interests:
        sys_prompt = (
            "You will decide which research interest best matches a given paper. "
            f"Return the index (0-based) of the best matching interest, or {none_rank} if none match."
        )
        human_template = (
            "Research interests: {interests}\n\n" 
            "Title: {title}\nSummary: {summary}\nTLDR: {tldr}"
        )
        prompt_template = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(sys_prompt),
            HumanMessagePromptTemplate.from_template(template=human_template),
        ])
        llm = ChatOpenAI(model=os.environ.get('MODEL_NAME', 'deepseek-chat')).with_structured_output(
            Rank, method="function_calling"
        )
        rank_chain = prompt_template | llm
    def rank(cate):
        if cate in preference:
            return preference.index(cate)
        else:
            return len(preference)

    with open(args.data, "r") as f:
        for line in f:
            data.append(json.loads(line))

    def interest_rank(item: dict):
        try:
            resp: Rank = rank_chain.invoke(
                {
                    "interests": ", ".join(interests),
                    "title": item.get("title", ""),
                    "summary": item.get("summary", ""),
                    "tldr": item.get("AI", {}).get("tldr", ""),
                }
            )
            return int(resp.rank)
        except langchain_core.exceptions.OutputParserException as e:
            print(f"{item.get('id', 'N/A')} rank error: {e}", file=sys.stderr)
            return none_rank
        except Exception as e:
            print(f"{item.get('id', 'N/A')} rank fail: {e}", file=sys.stderr)
            return none_rank

    if interests:
        data.sort(key=interest_rank)

    categories = set([item["categories"][0] for item in data])
    template = open("paper_template.md", "r").read()
    categories = sorted(categories, key=rank)
    cnt = {cate: 0 for cate in categories}
    for item in data:
        if item["categories"][0] not in cnt.keys():
            continue
        cnt[item["categories"][0]] += 1

    markdown = f"<div id=toc></div>\n\n# Table of Contents\n\n"
    for idx, cate in enumerate(categories):
        markdown += f"- [{cate}](#{cate}) [Total: {cnt[cate]}]\n"

    idx = count(1)
    for cate in categories:
        markdown += f"\n\n<div id='{cate}'></div>\n\n"
        markdown += f"# {cate} [[Back]](#toc)\n\n"
        markdown += "\n\n".join(
            [
                template.format(
                    title=item["title"],
                    authors=",".join(item["authors"]),
                    summary=item["summary"],
                    url=item['abs'],
                    tldr=item['AI']['tldr'],
                    motivation=item['AI']['motivation'],
                    method=item['AI']['method'],
                    result=item['AI']['result'],
                    conclusion=item['AI']['conclusion'],
                    cate=item['categories'][0],
                    idx=next(idx)
                )
                for item in data if item["categories"][0] == cate
            ]
        )
    with open(args.data.split('_')[0] + '.md', "w") as f:
        f.write(markdown)
