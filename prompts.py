from langchain import PromptTemplate

def give_story_title_prompt(story: str):
    prompt_text = """Give the following story an apt title. Do not return anything else but the title, do not give explanation as to how you came up with it.
    "{story}"
    """
    prompt = PromptTemplate.from_template(prompt_text)
    final = prompt.format(story=story)
    return final

def continue_story_prompt(doc_sum: str,story_so_far: str, genre: str, story_point: str):
    
    prompt_text = """You are an expert storyteller. You are currently writing a story of the genre {genre}.
    You are at the {story_point} of the story.
    
    This is what you have written so far: "{story_so_far}" 
    
    Take inspiration, ideas and concepts from the following description in order to continue the story: "{doc_sum}"
    """
    
    prompt = PromptTemplate.from_template(prompt_text)
    final = prompt.format(doc_sum=doc_sum, genre=genre,story_point=story_point, story_so_far=story_so_far)
    # print("continuing with prompt", final)
    return final