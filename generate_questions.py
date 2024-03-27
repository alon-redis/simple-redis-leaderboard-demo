from faker import Faker
import random

fake = Faker()

def generate_random_questions(num_questions=10):
    questions = []
    for _ in range(num_questions):
        question = fake.sentence()
        questions.append(question)
    return questions

if __name__ == "__main__":
    num_questions = 10
    questions = generate_random_questions(num_questions)
    for i, question in enumerate(questions, 1):
        print(f"Question {i}: {question}")
