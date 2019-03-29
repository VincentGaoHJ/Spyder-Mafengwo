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

+ run `getList.py` to get all locations' basic information, and fill up the `list_all.txt`.

The proxy IP with http://www.xicidaili.com/ is obtained, and fakeUA is generated to test. After passing the test, use proxy IP and self-built UA list to access web of mafengwo http://www.mafengwo.cn/mdd/map/10065.html. After being blocked, the proxy IP is automatically retrieved to continue.

Please attention that tnere are nearly 10 thousands locations in Beijing and a large mount of locations have no comment or few comments, so I abondon the locations which have less than 5 comments.

+ run `getList_subpoi.py` to get all locations' basic information **including the sub-locations("角楼" is a sub location of "故宫")**, and fill up the `list_all_sub.txt`.

The proxy IP with http://www.xicidaili.com/ is obtained, and fakeUA is generated to test. After passing the test, use proxy IP and self-built UA list to access web of mafengwo http://www.mafengwo.cn/mdd/map/10065.html. After being blocked, the proxy IP is automatically retrieved to continue.

Please attention that tnere are lots of sub locations are seldom marked as visited, so I save the sublocations' informations only if it is marked by more than five visitors.

+ run `getComments.py` to get all locations' comments, and fill up the `comment_all.txt`.

Obtain the commentary data for each location (because of the restrictions of API, with the effort, you can climb up to 600 comments per site)



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

* **list_all_subpoi.txt**
```
name	type_id	id	lat	lng	page	father_name	father_id	sub_page
故宫	3	3474	39.916698	116.397185	1	0	0	0
角楼	3	6627770	39.916698	116.397185	1	故宫	3474	1
午门	3	21463	39.916698	116.397185	1	故宫	3474	1
故宫博物院-珍宝馆	3	6627769	39.916698	116.397185	1	故宫	3474	1
故宫九龙壁	3	6627771	39.916698	116.397185	1	故宫	3474	1
故宫博物院-御花园	3	6627768	39.916698	116.397185	1	故宫	3474	1
太和殿	3	834363	39.916698	116.397185	1	故宫	3474	1
太和门	3	6627806	39.916698	116.397185	1	故宫	3474	1
乾清宫	3	849540	39.916698	116.397185	1	故宫	3474	1
```

* **comment_all.txt**
```
3474	1	进入故宫的那一刻心情还是很激动的，......
3474	1	去之前很兴奋，故宫真的超多人。......
3474	1	这次来北京，最期待的，除了香山就是故宫了。......
3474	1	记住一个原则，从南到北走，才能不走冤枉路！
3474	1	从天安门城楼下来往北走就是故宫博物院了。故宫的门票应该是60元，里面有一个钟表馆和珍宝馆是单独收费的，......
3474	1	听了现场工作人员的引导，我们从东华门外沿着筒子河经午门再进宫，之前看到有攻略说这条路线少一道安检，而且排队人少比较快。也许是因为周末，人真的好多呀，尤其是旅游团特别多。
```

