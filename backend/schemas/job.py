from datetime import datetime
from pydantic import BaseModel

class StoryJobBase(BaseModel):
    theme: str
    
class StoryJobResponse(BaseModel):
    job_id:         int
    status:         str
    created_at:     datetime
    story_id:       int         | None = None
    completed_at:   datetime    | None = None
    error:          str         | None = None
    
    class Config:
        from_attributes = True
        
# It's just a renaming tactic; it'll makes more sense when using this class
class StoryJobCreate(StoryJobBase):
    pass