#!/usr/bin/python
#coding = utf-8


from RiskQuantLib.Company.base import base
from RiskQuantLib.Set.Company.ListedCompany.listedCompany import setListedCompany

class listedCompany(base,setListedCompany):
    """
    This class represents listed company.
    """
    def __init__(self,nameString:str,codeString:str='',companyTypeString:str = 'Listed Company'):
        super(listedCompany,self).__init__(nameString,codeString,companyTypeString)



