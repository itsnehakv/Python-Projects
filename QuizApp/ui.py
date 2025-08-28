from tkinter import *
from quiz_brain import QuizBrain

THEME_COLOR = "#A53860"
CANVAS_BG="#FFDBDB"
WRONG_COLOR="#CD5656"
RIGHT_COLOR="#73946B"
class QuizInterface:
    def __init__(self,quiz_brain: QuizBrain):  
        self.quiz=quiz_brain

        #----Initialising the interface----
        self.window=Tk()
        self.window.title("Welcome to the Quiz!")
        self.window.minsize(height=600,width=360)
        self.window.config(padx=20,pady=20,bg=THEME_COLOR)

        self.score_label = Label(text="Score:0", fg="white",bg=THEME_COLOR,font=("SimSun",24))
        self.score_label.grid(column=1, row=0)

        self.canvas=Canvas(width=300,height=300,borderwidth=0,bg=CANVAS_BG)
        self.question_text=self.canvas.create_text(150,150,text="some",fill=THEME_COLOR,width=280,
                                                   font=("SimSun",20,"italic"))
        self.canvas.grid(column=0,row=1,columnspan=4,pady=50)

        self.tick_button=Button(bg=RIGHT_COLOR,height=2,width=5,highlightthickness=0,command=self.true_pressed)
        self.tick_button.grid(column=3,row=3)

        self.wrong_button=Button(bg=WRONG_COLOR,highlightthickness=0,height=2,width=5,command=self.false_pressed)
        self.wrong_button.grid(column=0,row=3)

        self.get_next_question()

        self.window.mainloop()


    def get_next_question(self):
        if self.quiz.still_has_questions():
            self.canvas.config(bg=CANVAS_BG)  
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
        else:
            self.end_of_game()


    def true_pressed(self):
       is_right=self.quiz.check_answer("true")
       self.give_feedback(is_right)

    def false_pressed(self):
        is_right=self.quiz.check_answer("false")
        self.give_feedback(is_right)

    def give_feedback(self, is_right):
        if is_right:
            self.canvas.config(bg="green")
            self.score_label.config(text=f"Score:{self.quiz.score}")
        else:
            self.canvas.config(bg="red")

        self.window.after(1000, self.get_next_question) 

    def end_of_game(self):
        self.canvas.config(bg=THEME_COLOR)
        self.canvas.itemconfig(self.question_text,
                           text=f"Quiz Completed!\n\nYou got {self.quiz.score} out of {len(self.quiz.question_list)} correct.",
                           fill="white", font=("SimSun", 18, "bold"),justify="center")
        #disable buttons after last question is reached
        self.tick_button.config(state="disabled")
        self.wrong_button.config(state="disabled")

