# zara.com-bot -- oskajup
A bot for zara.com that checks the availability of clothes and their specific sizes you want to buy (useful during sales)

If you're not from Poland, the only thing you need to change is this line:
btn_select = page.query_selector('button[aria-label^="Dodaj"]:not([aria-label^="Dodaj element"])')

Press Inspect, find the button line, or simply use "Pick an element," then change "Add" to the name that appears there, depending on the language your URL is in.

Also, change "Add element" to "X element," where X is the word you changed depending on the language your URL is in.

The script works without any problems for people using the Polish url

Also, don't forget to add the clothes you want to look for (their url) and the size you want to buy for them.
