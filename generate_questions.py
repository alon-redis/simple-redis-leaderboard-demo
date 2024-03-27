import random

def generate_math_questions(num_questions=10):
    questions = []
    for _ in range(num_questions):
        num1 = random.randint(1, 50)
        num2 = random.randint(1, 50)
        operation = random.choice(['+', '-'])
        
        if operation == '+':
            result = num1 + num2
        else:
            # Ensure the result is not negative
            result = max(num1, num2) - min(num1, num2)
        
        question = f"Is {num1} {operation} {num2} = {result}?"
        questions.append(question)
    
    return questions

if __name__ == "__main__":
    num_questions = 10
    questions = generate_math_questions(num_questions)
    for i, question in enumerate(questions, 1):
        print(f"Question {i}: {question}")
