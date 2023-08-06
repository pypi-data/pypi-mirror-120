import html

class SqlLoader:
    selectList = list()
    tableName = ""
    whereList = list()
    havingList = list()
    orWhereList = list()
    orHavingList = list()
    sqlLimit = str("")
    sqlJoinList = list()
    sqlOrderBy=str("")
    sqlGroupBy=str("")

    def table(self, tableName):
        self.tableName = tableName
        return self

    def orderBy(self,col,sortType=""):
        if not sortType:
            self.sqlOrderBy=" order by "+col
        else:
            self.sqlOrderBy=" order by "+col+" "+sortType
        return self

    def groupBy(self,col):
        self.sqlGroupBy=" group by "+col
        return self

    def whereBetween(self, key, pointsList=[]):
        if not pointsList[1]:
            pointsList[1] = pointsList[0]
        self.whereList.append(key + ">= "+str(pointsList[0])+" AND "+key + "<= "+str(pointsList[1]))
        return self

    def join(self, tableName, whereText, joinType="INNER"):
        joinType = joinType.strip().upper()
        if joinType == "INNER" or joinType == "JOIN":
            self.sqlJoinList.append("INNER JOIN "+tableName+" ON "+whereText)
        if joinType == "LEFT":
            self.sqlJoinList.append("LEFT JOIN "+tableName+" ON "+whereText)
        if joinType == "RIGHT":
            self.sqlJoinList.append("RIGHT JOIN "+tableName+" ON "+whereText)
        if joinType == "FULL OUTER":
            self.sqlJoinList.append(
                "FULL OUTER JOIN "+tableName+" ON "+whereText)
        if joinType not in ['FULL OUTER', 'INNER', 'LEFT', 'RIGHT', 'JOIN']:
            self.sqlJoinList.append(joinType+" "+tableName+" ON "+whereText)
        return self

    def select(self, value):
        self.selectList.append(value)
        return self

    def where(self, keyOrRaw, value=""):
        if not value:
            self.whereList.append(keyOrRaw)
        else:
            self.whereList.append(keyOrRaw+"'"+html.escape(str(value))+"'")
        return self

    def orWhere(self, keyOrRaw, value=""):
        if not value:
            self.orWhereList.append(keyOrRaw)
        else:
            self.orWhereList.append(keyOrRaw+"'"+html.escape(str(value))+"'")
        return self

    def having(self, keyOrRaw, value=""):
        if not value:
            self.havingList.append(keyOrRaw)
        else:
            self.havingList.append(keyOrRaw+"'"+html.escape(str(value))+"'")
        return self

    def orHaving(self, keyOrRaw, value=""):
        if not value:
            self.orHavingList.append(keyOrRaw)
        else:
            self.orHavingList.append(keyOrRaw+"'"+html.escape(str(value))+"'")
        return self

    def limit(self, limitValue, offset=0):
        if not offset:
            self.sqlLimit = " LIMIT "+limitValue
        else:
            self.sqlLimit = " LIMIT "+str(offset)+","+str(limitValue)
        return self

    def get(self):
        """
            return -- string data
        """
        sql = "SELECT "
        if not self.selectList:
            sql += "* "
        else:
            sql += ("".join(self.selectList)).strip()

        sql += " FROM "+self.tableName     
        if self.sqlJoinList:
            sql +=  " "+(" ".join(self.sqlJoinList)).strip()
        if self.whereList or self.orWhereList:
            sql += " WHERE "
        if self.whereList:
            sql += (" AND ".join(self.whereList)).strip()
        
        if self.orWhereList:
            if len(self.orWhereList)==1:
                sql+=" OR "
            else:
                sql+=" AND ("
            sql += (" OR ".join(self.orWhereList)).strip()
            if len(self.orWhereList)>1:
                sql+=")"
        if self.havingList or self.orHavingList:
            sql += " HAVING "
        if self.havingList:
            sql += (" AND ".join(self.havingList)).strip()
        if self.orHavingList:
            if len(self.orHavingList)==1:
                sql+=" OR "
            else:
                sql+=" AND ("
            sql += (" OR ".join(self.orHavingList)).strip()
            if len(self.orHavingList)>1:
                sql+=")"
        if self.sqlGroupBy.strip():
            sql+=self.sqlGroupBy
        if self.sqlOrderBy.strip():
            sql+=self.sqlOrderBy
        if self.sqlLimit.strip():
            sql+=self.sqlLimit
        return sql.strip()
