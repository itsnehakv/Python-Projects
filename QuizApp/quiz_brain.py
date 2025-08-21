import html
class QuizBrain:

    def __init__(self, q_list):
        self.question_number = 0
        self.score = 0
        self.question_list = q_list
        self.current_question = None

    def still_has_questions(self):
        return self.question_number < len(self.question_list)

    def next_question(self):
        if self.question_number>=len(self.question_list):
            return False
        self.current_question = self.question_list[self.question_number]
        self.question_number += 1
        self.q_text=html.unescape(self.current_question.text)  #unescapes the html entities
        return f"Q.{self.question_number}: {self.q_text}"
        # self.check_answer(user_answer)

    def check_answer(self, user_answer):
        correct_answer = self.current_question.answer
        if user_answer.lower() == correct_answer.lower():
            self.score+=1
            print("You got it right!")
            print(f"{len(self.question_list)}")
            print(f"{self.question_number}")
            return True
        else:
            print("That's wrong.")
            return False

