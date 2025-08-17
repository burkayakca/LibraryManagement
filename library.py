import sqlite3
import pandas as pd
import tabulate
from colorama import Fore, Style, init, Back
import os
import time

def clear(menu=False,sleepTime=3):
    if menu == True:
        q = input("Q - Geri\nSeçim: ")
        if q.lower() == "q":
            time.sleep(0)
            os.system("cls")
    else:
        time.sleep(sleepTime)
        os.system("cls")

# Initialize colorama
init(autoreset=True)

class Book:
    def __init__(self,name,author,year,publisher):
        self.name = name
        self.author = author
        self.year = year
        self.publisher = publisher

class Member:
    def __init__(self,name,phoneNumber,email,address):
        self.name = name
        self.phoneNumber = phoneNumber
        self.email = email
        self.address = address

class Library:
    def __init__(self):
        self.db = sqlite3.connect("library.db")
        self.cursor = self.db.cursor()
        self.create_tables()

    def create_tables(self):

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS books
                               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT, author TEXT, year INTEGER,
                                publisher TEXT,
                                hasBeenLent INTEGER DEFAULT 0
                                )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS members
                               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                hasLentABook INTEGER DEFAULT 0
                            )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS member_contact
                               (id INTEGER NOT NULL UNIQUE,
                                phoneNumber TEXT, email TEXT,
                                address TEXT,
                                FOREIGN KEY("id") REFERENCES "members"("id")
                            )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS lentBooks
                                ("lentBookID" INTEGER NOT NULL UNIQUE,
                                "lentbyID" INTEGER NOT NULL UNIQUE,
                                FOREIGN KEY("lentBookID") REFERENCES "books"("id"),
                                FOREIGN KEY("lentbyID") REFERENCES "members"("id"))
                            ''')

    def print_table(self,table):
        os.system("cls")
        if table == "books":

            selectBooks = "SELECT * FROM books" 
            books_df = pd.read_sql_query(selectBooks, library.db)

            if books_df.empty == True:
                print("Kitap kaydı bulunamadı")
                clear()
            else:
                print(tabulate.tabulate
                    (
                    books_df, headers=[f"Kayıt No","Kitap Adı", "Yazar","Yıl","Yayıncı","Ödünç?"],
                    tablefmt='psql',showindex=False)
                    )
                clear(menu=True)

                
        elif table == "members":  
                                
            members_df = pd.read_sql_query("SELECT * FROM members", library.db)
            if members_df.empty == True:
                print("Üye kaydı bulunamadı")
                clear(3)
            else:
                print(tabulate.tabulate
                    (
                    members_df,headers=["Üye No","Üye Adı","Ödünç"], 
                    tablefmt='psql',showindex=False)
                    )
                
    def checkBookLent(self,bookID):
        lentStatus = self.cursor.execute("SELECT hasBeenLent FROM books WHERE id = (?)",[bookID]).fetchone()[0]
        if lentStatus == 1: 
            return True
        elif lentStatus == 0:
            return False

    def checkMemberLent(self,memberID):
        lentStatus = self.cursor.execute("SELECT hasLentABook FROM members WHERE id = (?)",[memberID]).fetchone()[0]
        if lentStatus == 1: 
            return True
        elif lentStatus == 0:
            return False
                
    def UserContactInquiry(self,id): 
        selectMember = f"SELECT * FROM member_contact WHERE id='{id}'"
        contact_df = pd.read_sql_query(selectMember, library.db)
        print(tabulate.tabulate
                    (
                    contact_df,headers=["Üye No","Telefon","Email","Adres"], 
                    tablefmt='psql',showindex=False)
                    )
   

    def addBook(self):

        book = Book(input("Kitap adı: "),input("Yazar: "),input("Yıl: "),input("Yayınevi: "))
        
        self.cursor.execute("INSERT INTO books (name, author, year, publisher,hasBeenLent) VALUES (?, ?, ?, ?,0)",
        (book.name, book.author, book.year, book.publisher))
        self.db.commit()
        print(f"{book.name} adlı kitap eklendi")
        clear()


    def removeBook(self,bookID):

        bookName = self.cursor.execute("SELECT name FROM books WHERE id = (?)",[bookID]).fetchone()
        if bookName == None:
            print("Kitap bulunamadı")
            clear()
        else:
                sure = input(f"'{bookName[0]}' adlı kitabı silmek istiyormusunuz?(E/H - Y/N)")
                if sure.lower() == "e":
                    
                    if self.checkBookLent(bookID) == False:
                        try:
                            self.cursor.execute("DELETE FROM books WHERE id = (?)",[bookID])
                            self.db.commit()
                            print("Kitap Silindi.")
                            clear()
                        except:
                            return "Hata: Kitap Silinemedi"
                    else:
                        print("Hata: Kitap ödünç verilmiş gözüküyor. Silmeden önce iade işlemini gerçekleştirin.")
                else:
                    print("İşlem iptal edildi.")
                    clear()

    def addMember(self):

        member = Member(input("Ad: "),input("Telefon: "),input("E-posta: "),input("Adres: "))

        self.cursor.execute("INSERT INTO members (name, hasLentABook) VALUES (?,?)",
            (member.name,0))
        
        memberID = self.cursor.execute("SELECT seq FROM sqlite_sequence WHERE name='members'").fetchone()

        self.cursor.execute("INSERT INTO member_contact (id,phoneNumber, email, address) VALUES (?,?,?,?)",
            (memberID[0],member.phoneNumber, member.email, member.address))
        
        self.db.commit()
        print("Üye eklendi.")
        clear()

    def deleteMember(self):
        MemberID = input("Silinecek üyenin numarasını girin: ")
        memberName = self.cursor.execute("SELECT name FROM members WHERE id = (?)",[MemberID]).fetchone()
        if memberName == None:
            print("Üye bulunamadı")
            clear()
        else:

            if self.checkMemberLent(MemberID) == False:
                sure = input(f"'{memberName[0]}' adlı üyeyi silmek istiyormusunuz?(E/H)")
                if sure.lower() == "e" or sure.lower() == "y":
                    try:
                        self.cursor.execute("DELETE FROM members WHERE id = (?)",[MemberID])
                        self.db.commit()
                        print("Üye Silindi.")
                        clear()
                    except:
                        print("Hata: Üye silinemedi")
                        clear()
                else:
                    print("İşlem iptal edildi.")
                    clear()
            else:
                print("Hata: Üyenin ödünç aldığı kitap var. Üye silinemez")
                clear()


    def lendBook(self,MemberID,bookID):
       
        memberName = self.cursor.execute("SELECT name FROM members WHERE id = (?)",[MemberID]).fetchone()
        bookName = self.cursor.execute("SELECT name FROM books WHERE id = (?)",[bookID]).fetchone()
       
        if memberName != None and bookName != None: 

            if self.checkBookLent(MemberID) == False:

                sure = input(f"{bookName} adlı kitabı {memberName} adlı üyeye ödünç ver?(E/H): ")
                if sure.lower() == "e":
                    self.cursor.execute("INSERT INTO lentBooks (lentBookID, lentbyID) VALUES (?,?)", [MemberID,bookID])
                    self.cursor.execute("UPDATE members SET hasLentABook = 1 WHERE id = ?", [MemberID])
                    self.cursor.execute("UPDATE books SET hasBeenLent = 1 WHERE id = ?", [bookID])
                    print("Success!")
                    self.db.commit()
                else:
                    print("İşlem iptal edildi.")
                    clear(3)
            else:
               print("Error: Book already lent")       
        else:
           print("Error: Book/Member not found")
           

    def returnBook(self,MemberID,bookID):
        
        memberName = self.cursor.execute("SELECT name FROM members WHERE id = (?)",[MemberID]).fetchone()
        bookName = self.cursor.execute("SELECT name FROM books WHERE id = (?)",[bookID]).fetchone()

        if memberName:
            if self.checkMemberLent(MemberID) == False:
                print(f"{MemberID} numaralı kişi kitap ödünç almamış.")
            else:
                if bookName:
                    if self.checkBookLent(bookID):
                        checkLent = self.cursor.execute("SELECT * FROM lentBooks WHERE lentbyID = ? AND lentBookID = ?", [MemberID, bookID]).fetchone()
                        if checkLent: 
                            try:
                                self.cursor.execute("DELETE FROM lentBooks WHERE lentbyID = ? AND lentBookID = ?",[MemberID,bookID])
                                self.cursor.execute("UPDATE members SET hasLentABook = 0 WHERE id = ?", [MemberID])
                                self.cursor.execute("UPDATE books SET hasBeenLent = 0 WHERE id = ?", [bookID])
                                self.db.commit()
                                print("İade işlemi başarılı")
                                clear()
                            except:
                                print("Hata: İade işlemi başarısız")
                                clear()
                    else:
                        print("Ödünç Kaydı bulunamadı")
                        clear()
                else:
                    print("Kitap bulunamadı")
        else:
            print(f"{MemberID} numaralı kişinin kaydı bulunamadı.")
        
library = Library()

while True:

    Menu = input(
        f"\n{Back.BLUE}{Fore.WHITE}{Style.BRIGHT}*** MENÜ ***{Style.RESET_ALL} \t {Back.YELLOW}{Fore.BLACK}{Style.BRIGHT} language {Style.RESET_ALL}\n\n"
        f"{Back.BLACK}{Fore.CYAN}0 - Kitap Listesi       {Fore.RESET}| {Fore.CYAN}1 - Üye Listesi\n"
        f"{Fore.CYAN}2 - Kitap Ekle          {Fore.RESET}| {Fore.CYAN}3 - Üye Ekle\n"
        f"{Fore.CYAN}4 - Kitap Sil           {Fore.RESET}| {Fore.CYAN}5 - Üye Sil\n"
        f"{Fore.CYAN}6 - Kitap Ödünç Ver     {Fore.RESET}| {Fore.CYAN}7 - Kitap İade Al\n\n"
        f"{Back.RED}{Fore.WHITE}Q - Çıkış{Style.RESET_ALL}\n"
        "\nSeçim: ")

    if Menu == "0":
        library.print_table("books")
    elif Menu == "1":
        while True:
            library.print_table("members")
            secim = input(f"{Fore.CYAN} Q - Geri          {Fore.RESET}| {Fore.CYAN}C - İletişim bilgisi sorgula{Style.RESET_ALL}\nSeçim: {Style.RESET_ALL}")
            if secim.lower() == "q":
                os.system("cls")
                break
            elif secim.lower()== "c":
                id = int(input("Üye Numarası giriniz: "))
                print("\n")
                clear(0)
                library.UserContactInquiry(id)
                print("Enter - Geri")
                ask = input("")
                clear(0)
                break
            else:
                os.system("cls")
                pass
    elif Menu == "2":
         library.addBook()
    elif Menu == "3":
        library.addMember()
    elif Menu == "4":
        id = int(input("Silinecek kitabın numarasını girin: "))
        library.removeBook(id)
    elif Menu == "5":
         library.deleteMember()
    elif Menu == "6":
         library.lendBook(int(input("Ödünç verilen üyenin numarasını girin: ")),int(input("Kitabın numarasını girin: ")))
    elif Menu == "7":
        library.returnBook(int(input("İade alınan üyenin numarasını girin: ")),int(input("Kitabın numarasını girin: ")))
    elif Menu.lower() == "q":
        print("Programdan çıkılıyor...")
        library.db.close()
        break
    else:
        print("Hatalı giris.")
        clear()