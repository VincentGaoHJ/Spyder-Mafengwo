# Spyder-Mafengwo

## Description
* This is a project to crawl the mafengwo website(http://www.mafengwo.cn). 
* In the project, I got all the locations' imformations in **Beijing**, including latitude and longitude, and their comments.
* No framework was used.


## Dependencies

```
import os
import json
import urllib
import random
import requests
import telnetlib
from random import choice
from bs4 import BeautifulSoup
from proxy import prepare_proxy
from fake_useragent import UserAgent
```

## Operation

+ run `getList.py` to get all collations basic information, and fill up the `list_all.txt`.

The proxy IP with http://www.xicidaili.com/ is obtained, and fakeUA is generated to test. After passing the test, use proxy IP and self-built UA list to access web of mafengwo http://www.mafengwo.cn/mdd/map/10065.html. After being blocked, the proxy IP is automatically retrieved to continue.



## Output Format
* **list_all.txt**
```
name	type_id	id	lat	lng	page
故宫	3	3474	39.91804	116.397015	1
颐和园	3	3557	39.99243	116.272876	1
八达岭长城	3	3519	40.356183	116.016838	1
天安门广场	3	3498	39.903756	116.397693	1
天坛	3	3503	39.883675	116.412784	1
圆明园	3	6427	40.007905	116.303579	1
南锣鼓巷	3	3511	39.93744	116.403138	1
798艺术区	3	21100	39.985041	116.494624	1
```

