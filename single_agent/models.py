from pydantic import BaseModel,field_validator,Field


class Topics(BaseModel):
    title :str 
    summary : str = Field(...,max_length=250)
    importance : int = Field(...,ge=1,le=10)

class Domain(BaseModel):
    domain : str = Field(description="use the get_domain tool to get the domain for the user provided")
    topics : list[Topics]
    overall_summary : str
    source : str

    @field_validator("topics")
    def validate_topics(cls,topics):
        if len(topics)>5:
            raise ValueError(f"the length of topics is {len(topics)} which is too high it should be less than 6 topics")
        return topics
    
    @field_validator("overall_summary")
    def validate_summary(cls,summary):
        if len(summary.split())>50:
            raise ValueError(f"the length of topics is {len(summary.split())} which is too high it should be less than 50 words")
        return summary


