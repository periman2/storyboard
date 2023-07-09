
from typing import List

from ai_text import exectuteTextAIPrompt
from ai_image import getDescriptionsOfImage

descriptions: List[str] = getDescriptionsOfImage("resources/beach.png")

print(descriptions)

story: str = exectuteTextAIPrompt("Create a story that has at least 500 words using the following concepts: " + ", ".join(descriptions))

print("This story is : " + str(len(story.split(" "))) + "size in words")
print(story)

from typing import List

from ai_text import exectuteTextAIPrompt
from ai_image import getDescriptionsOfImage

descriptions: List[str] = getDescriptionsOfImage("resources/beach.png")

print(descriptions)

story: str = exectuteTextAIPrompt("Create a story that has at least 500 words using the following concepts: " + ", ".join(descriptions))

print("This story is : " + str(len(story.split(" "))) + "size in words")
print(story)
