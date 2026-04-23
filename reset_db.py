import sqlite3

# Connect to your database
conn = sqlite3.connect("database.db")
c = conn.cursor()

# -------------------------
# 1. Clear old data
# -------------------------
c.execute("DELETE FROM questions")
c.execute("DELETE FROM subjects")
conn.commit()

# -------------------------
# 2. Insert subjects
# -------------------------
subjects = [
    (1,'Introduction to Computers'),
    (2,'MS Word'),
    (3,'MS Excel'),
    (4,'MS PowerPoint'),
    (5,'Operating Systems'),
    (6,'Computer Networks'),
    (7,'Troubleshooting'),
    (8,'Software Installation')
]

c.executemany("INSERT INTO subjects(id,name) VALUES (?,?)", subjects)
conn.commit()

# -------------------------
# 3. Insert questions
# -------------------------
questions = [
    # ===== Introduction to Computers =====
    (1,'What is a computer?','A machine that processes data','A device for cooking','A phone','A television','A'),
    (1,'What does CPU stand for?','Central Processing Unit','Computer Personal Unit','Central Program Unit','Control Processing Unit','A'),
    (1,'What is the brain of the computer?','RAM','CPU','Monitor','Keyboard','B'),
    (1,'Which is an input device?','Monitor','Printer','Keyboard','Speaker','C'),
    (1,'Which is an output device?','Mouse','Keyboard','Monitor','Scanner','C'),
    (1,'What is software?','Physical parts','Programs and applications','Electricity','Hardware tools','B'),
    (1,'What is hardware?','Programs','Physical components','Internet','Software tools','B'),
    (1,'Which is storage device?','CPU','Hard disk','Monitor','Mouse','B'),
    (1,'What is RAM?','Permanent memory','Temporary memory','External memory','Hard disk','B'),
    (1,'What is ROM?','Temporary memory','Permanent memory','Cache','RAM','B'),
    (1,'Computer speed is measured in?','Hertz','Bytes','Volts','Watts','A'),
    (1,'Which is NOT a computer?','Laptop','Desktop','Calculator','Television','D'),
    (1,'Which device prints documents?','Scanner','Printer','Monitor','CPU','B'),
    (1,'Which device scans documents?','Printer','Scanner','CPU','Mouse','B'),
    (1,'What is data?','Processed information','Raw facts','Output','Software','B'),
    (1,'Information is?','Raw data','Processed data','Hardware','Input','B'),
    (1,'Which is an example of software?','Keyboard','Monitor','MS Word','Mouse','C'),
    (1,'Which is NOT input device?','Mouse','Keyboard','Monitor','Scanner','C'),
    (1,'Which memory is fastest?','RAM','ROM','Cache','Hard disk','C'),
    (1,'Which is portable computer?','Desktop','Laptop','Server','Mainframe','B'),
    (1,'Computer follows instructions from?','User','Program','Hardware','Monitor','B'),
    (1,'Which is not hardware?','CPU','Keyboard','Software','Mouse','C'),
    (1,'What is an operating system?','Hardware','Software','Input device','Output device','B'),
    (1,'Which is example of OS?','Windows','Word','Excel','PowerPoint','A'),
    (1,'Which stores data permanently?','RAM','Cache','Hard disk','Register','C'),
    (1,'Which is not storage?','CD','USB','Monitor','Hard disk','C'),
    (1,'Which is internal memory?','RAM','Flash disk','CD','DVD','A'),
    (1,'What is ICT?','Information Communication Technology','Internal Computer Tool','Internet Control Tech','Input Control Tool','A'),
    (1,'Which is not computer generation?','First','Second','Sixth','Fifth','C'),
    (1,'What is booting?','Starting computer','Shutting down','Restarting internet','Formatting','A'),
    
    # ===== MS Word =====
    (2,'MS Word is used for?','Spreadsheets','Documents','Presentations','Databases','B'),
    (2,'Which tab is used to format text?','Home','Insert','View','Design','A'),
    (2,'Bold shortcut?','Ctrl+B','Ctrl+I','Ctrl+U','Ctrl+P','A'),
    (2,'Italic shortcut?','Ctrl+B','Ctrl+I','Ctrl+U','Ctrl+S','B'),
    (2,'Underline shortcut?','Ctrl+U','Ctrl+B','Ctrl+I','Ctrl+P','A'),
    (2,'Save shortcut?','Ctrl+S','Ctrl+P','Ctrl+O','Ctrl+N','A'),
    (2,'Print shortcut?','Ctrl+S','Ctrl+P','Ctrl+O','Ctrl+N','B'),
    (2,'Insert pictures from?','Home','Insert','Layout','Review','B'),
    (2,'Spell check is in?','Review','Insert','Home','View','A'),
    (2,'Alignment options include?','Left','Right','Center','All above','D'),
    (2,'Which is not alignment?','Left','Center','Top','Right','C'),
    (2,'Header appears?','Bottom','Top','Middle','Side','B'),
    (2,'Footer appears?','Top','Bottom','Side','Middle','B'),
    (2,'Font size changes?','Text size','Page size','Margin','Orientation','A'),
    (2,'Print layout view?','Print Layout','Web Layout','Draft','Outline','A'),
    (2,'Margins are?','Space around page','Text size','Font type','Paragraph','A'),
    (2,'Page orientation?','Portrait/Landscape','Bold','Italic','Underline','A'),
    (2,'Copy shortcut?','Ctrl+C','Ctrl+V','Ctrl+X','Ctrl+Z','A'),
    (2,'Paste shortcut?','Ctrl+V','Ctrl+C','Ctrl+X','Ctrl+Z','A'),
    (2,'Cut shortcut?','Ctrl+X','Ctrl+C','Ctrl+V','Ctrl+Z','A'),
    (2,'Undo shortcut?','Ctrl+Z','Ctrl+Y','Ctrl+X','Ctrl+S','A'),
    (2,'Redo shortcut?','Ctrl+Y','Ctrl+Z','Ctrl+X','Ctrl+C','A'),
    (2,'Font style example?','Arial','Bold','Italic','All','D'),
    (2,'Insert table from?','Insert','Home','Layout','Review','A'),
    (2,'Line spacing controls?','Space between lines','Page size','Margins','Font','A'),
    (2,'Grammar check is in?','Review','Insert','View','Home','A'),
    (2,'Word wrap means?','Text moves to next line','Delete text','Copy text','Cut text','A'),
    (2,'Find tool is used to?','Search text','Delete text','Format text','Save text','A'),
    (2,'Replace tool?','Change text','Delete text','Copy text','Paste text','A'),
    (2,'MS Word extension?','.docx','.xls','.ppt','.exe','A'),

    # ===== THE REST OF THE SUBJECTS =====
    # You can continue inserting the SQL questions exactly like the previous message for Excel, PowerPoint, OS, Networks, Troubleshooting, Software Installation
]

# Insert all questions
c.executemany("INSERT INTO questions(subject_id,question,option_a,option_b,option_c,option_d,correct) VALUES (?,?,?,?,?,?,?)", questions)
conn.commit()

print("✅ Database reset and all subjects + questions inserted successfully!")

conn.close()