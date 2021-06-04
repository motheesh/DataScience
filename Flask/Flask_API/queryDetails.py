from customErrorHandler import inSufficientDataError
class query_details:
    def __init__(self,obj):
        self.tablename=obj["tablename"] if "tablename" in obj else None
        self.columns=obj["columns"] if "columns" in obj else None
        self.filters=obj["filters"] if "filters" in obj else None
        self.update=obj["update"] if "update" in obj else None
        self.data_list=obj["data_list"] if "data_list" in obj else None
        
    def __str__(c):
        return "This class holds structure of query details"

    def is_data_valid(self,data,typeOfOperation):
        
        if typeOfOperation == "select":
            if data.columns!=None and data.filters!=None  and data.tablename!=None:
                return True
        elif typeOfOperation == "create":
            if data.columns!=None and data.tablename!=None:
                return True
        elif typeOfOperation == "delete":
            if data.filters!=None and data.tablename!=None:
                return True
        elif typeOfOperation == "insert":
            if data.columns!=None and data.tablename!=None:
                return True
        elif typeOfOperation == "update":
            if data.filters!=None and data.tablename!=None and data.update!=None and len(data.update)>0:
                return True
        elif typeOfOperation == "exist":
            if data.tablename!=None:
                return True
        elif typeOfOperation == "bulk":
            if data.tablename!=None and data.columns!=None and data.data_list!=None:
                return True
        return False

 
    def generate_query(self,data,typeOfOperation):
        query=""
        if(self.is_data_valid(data,typeOfOperation)):
            if typeOfOperation=="select":
                query=f'select {"*" if "all" in data.columns else ",".join(data.columns)} from {data.tablename}'
                if len(data.filters)>0:
                    filter_condition=" and ".join([ f"{key}='{data.filters[key]}'" for key in data.filters ])
                    query+=f' where {filter_condition}'
            elif typeOfOperation=="create":
                col_value=",".join([ f"{key} {data.columns[key]}" for key in data.columns ])
                query=f'create table {data.tablename} ({col_value})'
            elif typeOfOperation=="insert":
                col_name=",".join([str(key) for key in data.columns ])
                col_value=",".join([f"'{data.columns[key]}'" for key in data.columns ])
                query=f'insert into {data.tablename} ({col_name}) values ({col_value})'
            elif typeOfOperation=="bulk":
                col_name=",".join([str(key) for key in data.columns ])
                col_value=",".join(["%s" for key in data.columns ])
                query=f'insert into {data.tablename} ({col_name}) values ({col_value})'
                bulk_data=[tuple(row) for row in data.data_list]
                print(bulk_data)
                query={"query":query,"data":bulk_data}
            elif typeOfOperation=="delete":
                query=f'delete from {data.tablename}'
                if len(data.filters)>0:
                    filter_condition=" and ".join([ f"{key}='{data.filters[key]}'" for key in data.filters ])
                    query+=f' where {filter_condition}'
            elif typeOfOperation=="update":
                update_set=",".join([f'{key}="{data.update[key]}"' for key in data.update])
                query=f'update {data.tablename} set {update_set}'
                if len(data.filters)>0:
                    filter_condition=" and ".join([ f"{key}='{data.filters[key]}'" for key in data.filters ])
                    query+=f' where {filter_condition}'
            elif typeOfOperation=="exist":
                if typeOfOperation=="select":
                    query=f'select top 1 from {data.tablename}'
            elif typeOfOperation=="UpdateSelect":
                if typeOfOperation=="select":
                    query=f'select * from {data.tablename}'
                    if len(data.filters)>0:
                        filter_condition=" and ".join([ f"{key}='{data.filters[key]}'" for key in data.filters ])
                        query+=f' where {filter_condition}'
            return query
        else:
            raise inSufficientDataError(error=f"400 bad request, data not sufficient unable to perform {typeOfOperation} Operation",statusCode=400)
            return ""
    
