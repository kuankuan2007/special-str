"""
Copyright (c) 2023 Gou Haoming
specialStr is licensed under Mulan PSL v2.
You can use this software according to the terms and conditions of the Mulan PSL v2.
You may obtain a copy of Mulan PSL v2 at:
         http://license.coscl.org.cn/MulanPSL2
THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
See the Mulan PSL v2 for more details.
"""
import re
from typing import List,Dict,Tuple
__all__=["UrlChecker","PathChecker","EmailChecker","Checker"]
class Checker(object):
    tester=[] #type: List[re.Pattern]
    finder={} #type: Dict[Tuple[str,...],re.Pattern]
    
class UrlChecker(Checker):
    tester=[re.compile(r"^[^/\\\.&\?\#]*://(?:[^/\\\.&\?\#]+\.)+[^/\\\.&\?\#]+(?::[0-9]+)?(?:(?:/[^/\\\.&\?\#]+)*/?)(?:\?(?:(?:[^/\\\.&\?\#]+=[^/\\\.&\?\#]*)&?)+)?(?:#[^&\?\#]*)?$")]
    finder={
        (
            "scheme","domain","port","path","paramstr","anchor"
        ):re.compile(r"^([^/\\\.&\?\#]*)://((?:[^/\\\.&\?\#]+\.)+[^/\\\.&\?\#]+)((?::[0-9]+)?)((?:(?:/[^/\\\.&\?\#]+)*/?))((?:\?(?:(?:[^/\\\.&\?\#]+=[^/\\\.&\?\#]*)&?)+)?)((?:#[^&\?\#]*)?)$")
    }
    
class PathChecker(Checker):
    tester=[re.compile(r"^(?:(?:[a-zA-Z]:)?|//[^/\\\*\?]+)/(?:[^/\\\*\?]+/?)*$")]
    driverFinder=re.compile(r"^((?:(?:[a-zA-Z]:)?|//[^/\\\*\?]+))/(?:[^/\\\*\?]+/?)*$")
    pathFinder=re.compile(r"^(?:(?:[a-zA-Z]:)?|//[^/\\\*\?]+)(/(?:[^/\\\*\?]+/?)*)$")
    finder={
        (
            "driver","path"
        ):re.compile(r"^((?:(?:[a-zA-Z]:)?|//[^/\\\*\?]+))(/(?:[^/\\\*\?]+/?)*)$")
    }
class EmailChecker(Checker):
    tester=[re.compile(r"^[\w.%+-]+@(?:[^/\\\.&\?\#]+\.)+[^/\\\.&\?\#]+$")]
    finder={
        (
            "user","domain"
        ):re.compile(r"^([\w.%+-]+)@((?:[^/\\\.&\?\#]+\.)+[^/\\\.&\?\#]+)$")
    }
