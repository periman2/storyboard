
def is_image(filename: str):
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.webp']
    return any(filename.lower().endswith(ext) for ext in image_extensions)

def is_pdf(filename: str):
    return any(filename.lower().endswith(ext) for ext in ['.pdf'])

def is_txt(filename: str):
    return any(filename.lower().endswith(ext) for ext in ['.txt'])

#TODO: add support for this
def is_doc(filename: str):
    return any(filename.lower().endswith(ext) for ext in ['.doc'])

def is_docx(filename: str):
    return any(filename.lower().endswith(ext) for ext in ['.docx'])

def is_any_document(filename: str):
    return any(filename.lower().endswith(ext) for ext in [ '.docx', '.pdf', '.txt'])