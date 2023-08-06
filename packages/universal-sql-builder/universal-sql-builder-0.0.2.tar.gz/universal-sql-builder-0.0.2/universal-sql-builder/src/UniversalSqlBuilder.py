from SqlLoader import SqlLoader


class UniversalSqlBuilder:

    @staticmethod
    def table(tableName):
        return SqlLoader().table(tableName)


print(UniversalSqlBuilder.table("employee").groupBy("department").get())
