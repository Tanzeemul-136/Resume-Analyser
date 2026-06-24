import PyPDF2

class ResumeParser:
    
    def extract_text(self,pdf):
        
        text = ""
        reader = PyPDF2.PdfReader(pdf)
        
        for page in reader.pages:
            text += page.extract_text()
        return text
            