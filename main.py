import psycopg2
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from config import host, user, password, db_name, port

APPNAME = 'Инвентаризация в Дурке 0.001 pre-alpha build v3'

class MainApp(App):
    def build(self):
        SM.add_widget(MenuScreen())
        SM.add_widget(MainScreen())
        SM.add_widget(ErrorScreen())
        SM.current = 'MenuScreen'
        try:
            connection = psycopg2.connect(
            host = host,
            user = user,
            password = 'password',
            database = db_name,
            port = port
            )
            
            SM.current = 'MainScreen'
            connection.close()
            return SM
        except Exception as _ex:
            print(_ex)
            SM.current = 'ErrorScreen'
            return SM

class MenuScreen(Screen):
    
    menu_layout = GridLayout(cols = 1)
    
    def __init__(self):
        super().__init__()
        
        self.name = 'MenuScreen'
        
        self.menu_label = Label(text = APPNAME)
        self.menu_layout.add_widget(self.menu_label)
        
        
        
        
             
    
class ErrorScreen(Screen):
    def __init__(self):
        super().__init__()
        
        self.name = 'ErrorScreen'
        
        error_layout = GridLayout(cols = 1)
        self.add_widget(error_layout)
        error_layout.add_widget(Label(text = f'ОШИБКА СОЕДИНЕНИЯ', font_size = 45, color = 'red'))
        RetryButton = Button(text ='Попробовать снова')
        RetryButton.bind(on_release = self.retry)
        error_layout.add_widget(RetryButton)
        
    def retry(self, *args):
        try:
            connection = psycopg2.connect(
            host = host,
            user = user,
            password = password,
            database = db_name,
            port = port
            )
            
            self.manager.current = 'MainScreen'
            connection.close()
            return SM
        except Exception as _ex:
            print(_ex)
            self.manager.current = 'ErrorScreen'
            return SM
        

class MainScreen(Screen):
    
    main_layout = GridLayout(cols = 2)
    
    def __init__(self):
        super().__init__()
        
        self.name = 'MainScreen'
        
        
        self.add_widget(self.main_layout)
        
        self.main_layout.add_widget(Label(text = 'Запросить запись №: '))
        
        self.id = TextInput(multiline = False)
        self.main_layout.add_widget(self.id)
        
        Submit = Button(text ='Сделать запрос')
        Submit.bind(on_release = self.submit)
        self.main_layout.add_widget(Submit)
        
        self.answer = Label(text = ' ')
        self.main_layout.add_widget(self.answer)
        
        GoError = Button(text ='Go error')
        GoError.bind(on_release = self.error)
        self.main_layout.add_widget(GoError)
        
    def submit(self, *args):
        try:
            connection = psycopg2.connect(
                host = host,
                user = user,
                password = password,
                database = db_name,
                port = port
                )
            
            connection.autocommit = True
            
            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT name FROM tools WHERE id = %s;""" , [self.id.text]
                )
                #print(f'[INFO] Прочтено что-то {cursor.fetchone()}')
                x = str(cursor.fetchone())
                
                self.answer.text =  f'name of {self.id.text} is {x}'
                
        except Exception as _ex:
            print(_ex)
            self.manager.current = 'ErrorScreen'
            return SM
                
                
    def error(self, *args):
        self.manager.current = 'ErrorScreen'


SM = ScreenManager()

if __name__ == '__main__':
    MainApp().run()