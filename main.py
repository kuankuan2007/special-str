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
import os
from .checker import *
from typing import Any, Dict,List,Union,Tuple,Union
from typing_extensions import Literal
import copy
__all__=["Url","Path","Email"]
class SpecialStr(str):
    checker=Checker() #type: Checker
    def __new__(cls, value):
        var=str(value)
        if not all([i.match(var)!=None for i in cls.checker.tester]):
            raise ValueError("\"%s\" does not appear to be a legal %s"%(var,cls.__name__.lower()))
        return super().__new__(cls, var)
    def __getattribute__(self, name: str):
        for i in super().__getattribute__("checker").finder:
                if name in i:
                    values=self.checker.finder[i].findall(self)[0] #type: Union[Tuple[str,...],str]
                    if type(values)==str:
                        return values
                    if type(values)==tuple:
                        return values[i.index(name)]
        return super().__getattribute__(name)
class Url(SpecialStr):
    """
    ## This class represents a URL and inherits from the SpecialStr class.
    ### Attributes:
        - checker (UrlChecker): An instance of the UrlChecker class used to validate URLs.
        - shame (str): A string representing any shameful content associated with the URL.
        - domain (str): The domain name of the URL.
        - port (str): The port number of the URL, if specified.
        - path (str): The path component of the URL after the domain and before any query parameters or anchors.
        - paramstr (str): A string representing all query parameters in key-value pairs separated by '&'.
        - anchor (str): The anchor component of the URL after '#' symbol.
        - Properties:
        - params: Returns a dictionary containing all query parameters as key-value pairs.
    """
    checker=UrlChecker()
    shame="" #type: str
    domain="" #type: str
    port="" #type: str
    path="" #type: str
    paramstr="" #type: str
    anchor="" #type: str
    @property
    def params(self)->Dict[str,str]:
        li=self.paramstr.replace("?","",1).split("&")
        return {i[0]:i[1] for i in [j.split("=",1) for j in li if j!=""]}

class Path(SpecialStr):
    """
    ## Represents a path. It can be used as same as a str, but it has more function about path.
    Attributes:
        - driver (str): The drive letter of the path.
        - path (str): The directory and file name of the path.
    ## Methods:
        - partition() -> List[str]: Split the path into list.
        - name() -> str: Return the name of the file or folder that this path points to.
        - add(value:str) -> "Path": Add another dir name after the current path and return a new Path object.
        - adds(value:List[str]) -> "Path": Add multiple dir names after the current path and return a new Path object.
        - findRest(other:"Path",error:Literal["strict","ignore"]="strict"): Find the same ancestor node between two paths. If error is set to "strict" (default), raise ValueError if other is not exactly parent directory of self. Otherwise, return remaining directories in self's partition after finding different ancestor with other's partition.
    """
    checker=PathChecker()
    def __new__(cls, value):
        var=str(value)
        if var.startswith("."):
            var=os.path.abspath(var)
        var=var.replace("\\","/")
        return super().__new__(cls,var)
    @property
    def partition(self)->List[str]:
        """split the path into list"""
        li=self.path.split("/")
        while "" in li:
            li.remove("")
        return li
    @property
    def name(self)->str:
        """The name of the path points to"""
        return self.partition[-1] if len(self.partition) else self.driver+"/"
    def add(self, value:str):
        """add another dir name after the path"""
        if self[-1]!="/":
            return Path(self+"/"+value)
        return Path(self+value)
    def adds(self, value:List[str])->"Path":
        new=copy.deepcopy(self)
        for i in value:
            new=new.add(i)
        return new
    def findRest(self,other:"Path",error:Literal["strict","ignore"]="strict"):
        """Find the same ancestor node of them
        :param error:"strict" means if other path not exactly the parent directory of this path, raise ValueError.
        """
        if error=="strict" and self.driver!=other.driver:
            raise ValueError("\"%s\" and \"%s\" has different driver"%(str(self),str(other)))
        retsult=copy.deepcopy(self.partition)
        for i in other.partition:
            if not len(retsult) or retsult[0]!=i:
                if error=="strict":
                    raise ValueError("\"%s\" is not the ancestor folder of %s"%(str(other),str(self)))
                return retsult
            del retsult[0]
        return retsult
    def getAbsolutePath(self,path)->"Path":
        """
        Returns the absolute path of a given file or directory by joining it with the current working directory.
        :param path: A string representing the relative path to be joined with the current working directory.
        :return: An object of type "Path" representing the absolute path obtained after joining.
        :raise ValueError: If input argument 'path' is not a valid string.
        """
        return Path(os.path.join(self, path))
class Email(SpecialStr):
    """
    ## Represents a email address. It can be used as same as a str, but it has more function about path.
    Attributes:
        - user (str): The user of the address.
        - domain (str): The doomain of address.
    """
    checker=EmailChecker()
    user="" #type: str
    domain="" #type: str