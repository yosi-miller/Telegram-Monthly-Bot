import telebot
from telebot import types


class BudgetData:
    # הגדרת מחלקה שתכיל את הנתונים הכלכליים של המשתמשים

    def __init__(self):
        # הגדרת משתנה שיכיל את ההכנסות והכנסות של המשתמשים, כל משתמש יזוהה לפי מזהה (ID)
        self.incomes = {}
        self.weekly_expenses = {}
        self.general_expenses = {}

    def update_income(self, user_id: int, amount: float) -> None:
        # פונקציה לעדכון ההכנסה של משתמש מסויים
        self.incomes[user_id] = amount

    def update_weekly_expenses(self, user_id: int, amount: float) -> None:
        # פונקציה לעדכון ההוצאות השבועיות של משתמש מסויים
        self.weekly_expenses[user_id] = amount

    def update_general_expenses(self, user_id: int, amount: float) -> None:
        # פונקציה לעדכון ההוצאות הכלליות של משתמש מסויים
        self.general_expenses[user_id] = amount

    def get_statistics(self, user_id: int) -> (float, float, float, float):
        # פונקציה לקבלת נתונים סטטיסטיים של משתמש מסויים

        # חישוב הוצאות והכנסות של משתמש, אם אין הכנסה יחזיר 0
        income = self.incomes.get(user_id, 0)
        weekly_expense = self.weekly_expenses.get(user_id, 0)
        general_expense = self.general_expenses.get(user_id, 0)
        # חישוב המאזן של המשתמש על ידי חיסור ההוצאות מההכנסות
        balance = income - (weekly_expense + general_expense)

        return income, weekly_expense, general_expense, balance

# מחלקה לניהול הבוט של משק הבית
class HomeBudgetBot:
    # פונקציית האתחול של המחלקה
    def __init__(self, token: str):
        # יצירת אובייקט הבוט עם הטוקן שהועבר
        self.bot = telebot.TeleBot(token)
        # יצירת אובייקט לניהול הנתונים של המשק הבית
        self.data = BudgetData()
        # הגדרת פונקציות הליסנר לכל פקודה או כפתור בבוט
        self.bot.message_handler(commands=['start'])(self.start_bot)
        self.bot.message_handler(commands=['help'])(self.help_bot)
        self.bot.message_handler(func=lambda message: message.text == 'עדכון הכנסות')(self.request_income_update)
        self.bot.message_handler(func=lambda message: message.text == 'עדכון הוצאות שבועיות')(self.test)
        self.bot.message_handler(func=lambda message: message.text == 'עדכון הוצאות כלליות')(
            self.request_general_expenses_update)
        self.bot.message_handler(func=lambda message: message.text == 'קבלת נתונים סטטיסטיים')(self.get_statistics)

    # פונקציית התחלה - מציגה את התפריט הראשי למשתמש
    def start_bot(self, message):
        user_id = message.chat.id  # שמירת מזהה המשתמש
        markup = types.ReplyKeyboardMarkup(row_width=3)  # יצירת תפריט כפתורים
        # הוספת כפתורים לתפריט
        itembtn1 = types.KeyboardButton('עדכון הכנסות')
        itembtn2 = types.KeyboardButton('עדכון הוצאות שבועיות')
        itembtn3 = types.KeyboardButton('עדכון הוצאות כלליות')
        itembtn4 = types.KeyboardButton('קבלת נתונים סטטיסטיים')
        markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
        self.bot.send_message(user_id, "בחר את הפעולה הרצויה:", reply_markup=markup)  # שליחת ההודעה עם התפריט למשתמש

    def test(self, message):
        user_id = message.chat.id  # שמירת מזהה המשתמש
        markup = types.ReplyKeyboardMarkup(row_width=4)  # יצירת תפריט כפתורים
        # הוספת כפתורים לתפריט
        itembtn1 = types.KeyboardButton('week 1')
        itembtn2 = types.KeyboardButton('week 2')
        itembtn3 = types.KeyboardButton('week 3')
        itembtn4 = types.KeyboardButton('week 4')
        markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
        self.bot.send_message(user_id, "בחר את הפעולה הרצויה:", reply_markup=markup)  # שליחת ההודעה עם התפריט למשתמש

    def help_bot(self, message):
        self.bot.reply_to(message, "test")

    # פונקציה לבקשת עדכון הכנסה חודשית
    def request_income_update(self, message):
        user_id = message.chat.id  # שמירת מזהה המשתמש
        # שליחת הודעה למשתמש ובקשה להזין את ההכנסה החודשית
        msg = self.bot.send_message(user_id, "אנא הזן את ההכנסה החודשית:")
        # רישום הפונקציה שתטפל בתגובה של המשתמש
        self.bot.register_next_step_handler(msg, self.update_income)

    # פונקציה לבקשת עדכון ההוצאות השבועיות
    def request_weekly_expenses_update(self, message):
        user_id = message.chat.id  # שמירת מזהה המשתמש
        # שליחת הודעה למשתמש ובקשה להזין את ההוצאות השבועיות
        msg = self.bot.send_message(user_id, "אנא הזן את ההוצאות השבועיות:")
        # רישום הפונקציה שתטפל בתגובה של המשתמש
        self.bot.register_next_step_handler(msg, self.update_weekly_expenses)

    # פונקציה לבקשת עדכון ההוצאות הכלליות
    def request_general_expenses_update(self, message):
        user_id = message.chat.id  # שמירת מזהה המשתמש
        # שליחת הודעה למשתמש ובקשה להזין את ההוצאות הכלליות
        msg = self.bot.send_message(user_id, "אנא הזן את ההוצאות הכלליות:")
        # רישום הפונקציה שתטפל בתגובה של המשתמש
        self.bot.register_next_step_handler(msg, self.update_general_expenses)

    # פונקציה לעדכון ההכנסה החודשית
    def update_income(self, message):
        user_id = message.chat.id  # שמירת מזהה המשתמש
        amount = float(message.text)  # המרת הטקסט למספר עשרוני
        self.data.update_income(user_id, amount)  # עדכון ההכנסה בנתונים
        # שליחת הודעת אישור למשתמש
        self.bot.reply_to(message, "ההכנסה עודכנה בהצלחה.")

    # פונקציה לעדכון ההוצאות השבועיות
    def update_weekly_expenses(self, message):
        user_id = message.chat.id  # שמירת מזהה המשתמש ששלח את ההודעה
        amount = float(message.text)  # המרת הטקסט שהמשתמש הזין למספר עשרוני
        # קריאה לפונקציה שמעדכנת את ההוצאות השבועיות עבור המשתמש בבסיס הנתונים
        self.data.update_weekly_expenses(user_id, amount)
        # שליחת הודעת אישור למשתמש על עדכון הנתונים
        self.bot.reply_to(message, "ההוצאות השבועיות עודכנו בהצלחה.")

    # פונקציה לעדכון ההוצאות הכלליות
    def update_general_expenses(self, message):
        user_id = message.chat.id  # שמירת מזהה המשתמש ששלח את ההודעה
        amount = float(message.text)  # המרת הטקסט שהמשתמש הזין למספר עשרוני
        # קריאה לפונקציה שמעדכנת את ההוצאות הכלליות עבור המשתמש בבסיס הנתונים
        self.data.update_general_expenses(user_id, amount)
        # שליחת הודעת אישור למשתמש על עדכון הנתונים
        self.bot.reply_to(message, "ההוצאות הכלליות עודכנו בהצלחה.")

    # פונקציה לקבלת נתונים סטטיסטיים על המשק הבית
    def get_statistics(self, message):
        user_id = message.chat.id  # שמירת מזהה המשתמש
        # קריאה לפונקציה שמחזירה את הנתונים הסטטיסטיים
        income, weekly_expense, general_expense, balance = self.data.get_statistics(user_id)
        # יצירת טקסט עם הנתונים הסטטיסטיים
        stats_text = f"""
        הכנסה: {income}
        הוצאה שבועית: {weekly_expense}
        הוצאה כללית: {general_expense}
        מאזן: {balance}
        """
        # שליחת הנתונים למשתמש
        self.bot.reply_to(message, stats_text)

    # פונקציה להפעלת הבוט
    def start(self):
        self.bot.polling()  # התחלת ההאזנה להודעות מהמשתמשים


# החלף בטוקן שלך
token = "6264576225:AAFpKP8TySlaYnEmlI03r1HfAVezeGKGR1k"
# יצירת אובייקט הבוט עם הטוקן
bot = HomeBudgetBot(token)
# הפעלת הבוט
bot.start()