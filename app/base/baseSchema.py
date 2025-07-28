from pydantic import BaseModel, validator
from typing import Optional, List, Dict, Any
from app.exceptions.exceptions import UnprocessableEntity
from fastapi import Query
import json


#TO-DO check where to use it
class SchemaBaseModel(BaseModel):
    def dict(self, *args, **kwargs) -> Dict[str, Any]:
        kwargs.pop('exclude_none', None)
        return super().dict(*args, exclude_none=True, **kwargs)
    

class SchemaBaseListRequest(BaseModel):
    offset: Optional[int] = Query(None)  
    limit: Optional[int] = Query(None)   
    sort: Optional[str] = Query(None)    
    fields: Optional[str] = Query(None)  
    q: Optional[str] = Query(None)       
    filter: Optional[str] = Query(None)  


    @validator('filter')
    def set_filter(cls, filter):
        filter = filter or "{}"
        try:
            json.loads(filter)
        except:
            raise UnprocessableEntity('Invalid Filters Json')
        
        return filter

    @validator('offset')
    def set_offset(cls, offset):
        return offset or 0
    
    @validator('limit')
    def set_limit(cls, limit):
        limit = limit or 100

        if limit > 500:
            raise UnprocessableEntity(f'Data limit is 500, sent {limit}')
        
        return limit
    
    @validator('sort')
    def set_sort(cls, sort):
        return sort or 'id+ASC'


class MetadataPagination(BaseModel):
    offset: Optional[int] = None
    limit: Optional[int] = None
    previousOffset: Optional[int] = None
    nextOffset: Optional[int] = None
    currentPage: Optional[int] = None
    pageCount: Optional[int] = None
    totalCount: Optional[int] = None


class SortPagination(BaseModel):
    field: str = None
    order: str = None


class GetListMetadata(BaseModel):
    pagination: MetadataPagination
    sortedBy: List[SortPagination]
    