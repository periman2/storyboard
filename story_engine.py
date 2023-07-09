from typing import Any, List
from typing import List
from enum import Enum
import uuid

from ai_text import exectuteTextAIPrompt, exectuteTextAIPromptStrict, executeDocumentSummarization
from ai_image import getDescriptionsOfImage
from prompts import continue_story_prompt, give_story_title_prompt

class StoryItemType(Enum):
    IMAGE = 1
    DOCUMENT = 2
    
class StoryItem:
    def __init__(self, path: str, filename: str, type: StoryItemType, date: int):
        self.path = path
        self.filename = filename
        self.type = type
        self.date = date
        self.description = ""

class StorySegment:
    def __init__(self, text: str, filename: str, origin_text: str):
        self.text = text
        self.filename = filename
        self.origin_text = origin_text

class StoryEngine:

    def __init__(self, genre: str):
        self.story_id: str = str(uuid.uuid4())
        self.story_gerne = genre
        self.store: List[StoryItem] = []
    
    story_progress: float = 0
    story_text: str = ''
    story_segments: List[StorySegment] = []
    story_title: str = ''

    def addItem(self, item: StoryItem):
        self.store.append(item)
        
    def onec_upon_a_time(self):
        indx = 1
        for item in self.store:
            if item.type == StoryItemType.DOCUMENT:
                item.description = executeDocumentSummarization(item.path)
            if item.type == StoryItemType.IMAGE:
                item.description = getDescriptionsOfImage(item.path)
        
            store_length = len(self.store)
            time_in_the_story = "middle"
            if store_length == 1:
                time_in_the_story = "beginning and end"
            elif indx == 1:
                time_in_the_story = "beginning"
            elif indx == store_length:
                time_in_the_story = "ending"
       
            prompt_res = exectuteTextAIPrompt(continue_story_prompt(item.description, self.story_text, self.story_gerne, time_in_the_story))
            self.story_segments.append(StorySegment(prompt_res, item.filename, item.description))
                
            self.story_text += prompt_res
            self.story_progress = indx / store_length
            
            if indx == store_length:
                self.story_title = exectuteTextAIPromptStrict(give_story_title_prompt(self.story_text))
                self.story_text = f"Presenting a storyboard narrative: {self.story_title}\n\n{self.story_text}"
                
            indx+=1
        
        return self.story_text
