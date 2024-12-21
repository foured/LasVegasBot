import random

class CodeGenerator:
    codes = set()
    
    @staticmethod
    def generate_code():
        if len(CodeGenerator.codes) >= 1000:
            print("Error to geberate more than 999 uniq codes.")
        
        while True:
            code = random.randint(0, 999)
            if code not in CodeGenerator.codes:
                CodeGenerator.codes.add(code)
                return code
    
    @staticmethod
    def reset():
        CodeGenerator.codes.clear() 