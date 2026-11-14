hey check the repo livefile

there are 4 website drafts in drafts/. review them, reconcile all 4 into one real site without dropping any of the actual content, then publish it and verify it actually works.

put the public site in site/ (homepage should be site/index.html). required-content.json is the list of stuff that has to survive verbatim — don’t paraphrase those away. if hours disagree, trust draft 1, not the “weekdays 10–4” bit in draft 2. don’t invent new facts and don’t edit the drafts themselves.

pages should keep deploying from site/ via .github/workflows/pages.yml. when you’re done run python scripts/verify_site.py and fix it until it says VERIFY PASSED.
