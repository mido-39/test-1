from flet import *
import sqlite3

conn = sqlite3.connect('data.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS student(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               stdname TEXT,
               stdmail TEXT,
               stdphone TEXT,
               stdaddress TEXT,
               stmathamatic INTEGER,
               starabic INTEGER,
               stfrance INTEGER,
               stenglish INTEGER,
               stdrawing INTEGER,
               stchemistry  INTEGER
               )
''')
conn.commit()


def main(page:Page):
    page.title = 'imad'
    page.scroll = True
    page.window.width=330
    page.window.height=650
    page.theme_mode = ThemeMode.LIGHT

    table_name = 'student'
    query = f'SELECT COUNT (*) FROM {table_name}'
    cursor.execute(query)
    result = cursor.fetchone()
    row_count = result[0]

    def add(e):
        cursor.execute('INSERT INTO student (stdname, stdmail, stdphone, stdaddress, stmathamatic, starabic, stfrance, stenglish, stdrawing, stchemistry) VALUES (?,?,?,?,?,?,?,?,?,?)',
                       (tname.value, tmail.value, tphone.value, taddress.value, mathmatic.value, arabic.value, france.value, english.value, draw.value, chemistry.value))
        conn.commit()

    def show(e):
        c = conn.cursor()
        c.execute('SELECT * FROM student')
        users = c.fetchall()
        # print(users)
        if not users == '':
            keys = ['id', 'stdname', 'stdmail', 'stdphone', 'stdaddress', 'stmathamatic', 'starabic', 'stfrance', 'stenglish', 'stdrawing', 'stchemistry']
            result = [dict(zip(keys,values)) for values in users]
            for x in result:
                m = x['stmathamatic'] if x['stmathamatic'] !='' else 0
                a = x['starabic'] if x['starabic'] !='' else 0
                f = x['stfrance'] if x['stfrance'] !='' else 0
                e = x['stenglish'] if x['stenglish'] !='' else 0
                d = x['stdrawing'] if x['stdrawing'] !='' else 0
                c = x['stchemistry'] if x['stchemistry'] !='' else 0
                res = (m + a + f + e + d + c)/6
                if res < 10:
                    y = Text('😨 راسب، بمعدل: '+ str(res), size=19, color='white', rtl=True)
                elif res >= 10:
                    y = Text('😁 ناجح بمعدل: '+ str(res), size=19, color='white', rtl=True)

                page.add(
                    Card(color= 'black',
                        content= Container(
                            content=Column([
                                ListTile(
                                    leading= Icon(icons.PERSON),
                                    title=Text('Name: '+ x['stdname'], color='white'),
                                    subtitle= Text('Student Email: '+ x ['stdmail'], color='amber')   
                                ),
                                Row([
                                    Text('Phone: '+ x['stdphone'], color='green'),
                                    Text('Address: '+ x['stdaddress'], color='green')
                                ],alignment=MainAxisAlignment.CENTER),
                                Row([
                                    Text('رياضيات: '+ str(x['stmathamatic']),color='blue'),
                                    Text('عربي: '+ str(x['starabic']),color='blue'),
                                    Text('فرنسي: '+ str(x['stfrance']),color='blue')
                                ],alignment=MainAxisAlignment.CENTER),
                                Row([
                                    Text('انجليزي: '+ str(x['stenglish']),color='blue'),
                                    Text('رسم: '+ str(x['stdrawing']),color='blue'),
                                    Text('كيمياء: '+ str(x['stchemistry']),color='blue')
                                ],alignment=MainAxisAlignment.CENTER),
                                Row([y],alignment=MainAxisAlignment.CENTER)
                            ])
                        )
                    )
                )
                page.update()
    
    ###############################################
    ################# failds ######################
    tname = TextField(label='اسم الطالب', icon=icons.PERSON, rtl=True, height=38)
    tmail = TextField(label='بريد الكتروني', icon=icons.MAIL, rtl=True, height=38)
    tphone = TextField(label='الهاتف', icon=icons.PHONE, rtl=True, height=38)
    taddress = TextField(label='العنوان', icon=icons.LOCATION_ON, rtl=True, height=38)

    marktext = Text('Marks Student - علامات الطالب', text_align='center',weight='bold')
    mathmatic = TextField(label='رياضيات', width=90, rtl=True, height=38)
    arabic = TextField(label='العربية', width=90, rtl=True, height=38)
    france = TextField(label='الفرنسية', width=90, rtl=True, height=38)
    english = TextField(label='الانجليزية', width=90, rtl=True, height=38)
    draw = TextField(label='الرسم', width=90, rtl=True, height=38)
    chemistry = TextField(label='الكيمياء', width=90, rtl=True, height=38)
    ###############################################
    # ---------------------------------------------
    addbutton = ElevatedButton(
        'اضافة طالب جديد',
        width= 140,
        style= ButtonStyle(bgcolor='blue',color='white',padding=15),
        on_click= add
    )
    showbutton = ElevatedButton(
        'عرض كل الطلاب',
        width= 140,
        style= ButtonStyle(bgcolor='blue',color='white',padding=15),
        on_click= show
    )

    page.add(
        Row([Image(src = '2mVW.gif',
                   width=170)],
            alignment=MainAxisAlignment.CENTER),
        Row([Text('تطبيق الطالب والمعلم في جيبك',
                 size=20, 
                 font_family='Calibri (Body)',
                 color='black')],
            alignment=MainAxisAlignment.CENTER),
        Row([Text('عدد الطلاب المسجلين: ',
                 size=20, 
                 font_family='Calibri (Body)',
                 color='blue'),
            Text(row_count,
                 size=20, 
                 font_family='Calibri (Body)',
                 color='black')],
            alignment=MainAxisAlignment.CENTER,
            rtl=True),
            tname,
            tmail,
            tphone,
            taddress,
        Row([marktext],
            alignment=MainAxisAlignment.CENTER),
        Row([mathmatic, arabic, france],
            alignment=MainAxisAlignment.CENTER, rtl=True),
        Row([english, draw, chemistry],
            alignment=MainAxisAlignment.CENTER, rtl=True),
        Row([addbutton, showbutton],
            alignment=MainAxisAlignment.CENTER, rtl=True)
    )


    page.update()

app(main)
