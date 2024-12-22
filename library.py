import sqlite3

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
                                name TEXT, author TEXT, year INTEGER, publisher TEXT, isLent BOOLEAN DEFAULT 0)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS members
                               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT, phoneNumber TEXT, email TEXT, address TEXT)''')


    def addBook(self):

        book = Book(input("Kitap adı: "),input("Yazar: "),input("Yıl: "),input("Yayınevi: "))
        
        self.cursor.execute("INSERT INTO books (name, author, year, publisher,isLent) VALUES (?, ?, ?, ?,0)",
        (book.name, book.author, book.year, book.publisher))
        
        self.db.commit()
        print(f"{book.name} adlı kitap eklendi")


    def removeBook(self,bookID):
        bookID = str(bookID)
        if self.validate("book",bookID) == True:
            if self.collection[bookID]["isLent"] == True:
                LentToID = self.collection[bookID]["LentTo"]
                DeleteLentBook = input(f"Kitap, {LentToID} numaralı üye'ye ödünç verilmiş gözüküyor. Yine de silinsim mi?(E/H)")
                if DeleteLentBook == "E" or DeleteLentBook == "e":
                    self.members[LentToID]["booksLent"].remove(self.collection[bookID]["name"])
                    del self.collection[bookID]
                    self.writeToDatabase("collection")
                    self.writeToDatabase("members")
                    print("Kitap silindi")
                else: 
                    print("Kitap silme işlemi iptal edildi.")
            else:
                sure = input(f'"{self.collection[bookID]['name']}" adlı Kitabı silmek istiyor musunuz? (E/H): ')
                if sure == "E" or sure == "e":
                    del self.collection[bookID]
                    self.writeToDatabase("collection")
                    print("Kitap silindi")
                else:
                    print("Kitap silme işlemi iptal edildi.")
        else:
            print(f"Hata: {bookID} numaralı Kitap bulunamadı.")
        
        

    def addMember(self):

        member = Member(input("Ad: "),input("Telefon: "),input("E-posta: "),input("Adres: "))

        self.cursor.execute("INSERT INTO members (name, phoneNumber, email, address) VALUES (?, ?, ?, ?)",
            (member.name, member.phoneNumber, member.email, member.address))
        
        self.db.commit()
        print("Üye eklendi.")

    def lendBook(self,MemberID,bookID):
        MemberID = str(MemberID)
        bookID = str(bookID)
        if self.validate("member",MemberID) == True:
            if self.validate("book",bookID) == True:
                if self.collection[bookID]["isLent"] == False:
                    self.members[MemberID]["booksLent"].append(self.collection[bookID]["name"])
                    self.collection[bookID]["isLent"] = True
                    self.collection[bookID]["LentTo"] = MemberID
                    print("Kitap Ödünç verildi")
                    self.writeToDatabase("collection")
                    self.writeToDatabase("members")
                else:
                    print("Bu kitap başkasına ödünç verilmiş.")
            else:
                print("Kitap bulunamadı")
        else:
            print(f"{MemberID} numaralı kişinin kaydı bulunamadı.")

        

    def returnBook(self,MemberID,bookID):
        MemberID = str(MemberID)
        bookID = str(bookID)
        if self.validate("member",MemberID) == True:
            if len(self.members[MemberID]["booksLent"]) == 0:
                print(f"{MemberID} numaralı kişi kitap ödünç almamış.")
            else:
                if self.validate("book",bookID) == True:
                    if self.collection[bookID]["isLent"] == True:
                        self.members[MemberID]["booksLent"].remove(self.collection[bookID]["name"])
                        self.collection[bookID]["LentTo"] = ""
                        self.collection[bookID]["isLent"] = False
                        print("Kitap iade alındı")
                        self.writeToDatabase("collection")
                        self.writeToDatabase("members")
                    else:
                        print("Kitap ödünç alınmamış.")
                else:
                    print("Kitap bulunamadı")
        else:
            print(f"{MemberID} numaralı kişinin kaydı bulunamadı.")
        

    def deleteMember(self,MemberID):
        MemberID = str(MemberID)
        if len(self.members) == 0:
            print("Kayıtlı üye bulunamadı.")
        else:
            if self.members[MemberID]:
                if self.members[MemberID]["booksLent"] == []:
                    sure = input(f'"{self.members[MemberID]["name"]}" adlı üyeyi silmek istiyor musunuz? (E/H): ')
                    if sure == "E" or sure == "e":
                        del self.members[str(MemberID)]
                        print("Üye silindi.")
                        self.writeToDatabase("members")
                    else:
                        print("Üye silme işlemi iptal edildi.")
                else:
                    print(f"Hata: üye'nin iade etmediği kitap(lar) mevcut.\n {self.members[MemberID]['booksLent']}")
            else:
                print("Bu isimde bir kullanıcı bulunamadı.")



library = Library()

while True:

    Menu = input("\n0-Kitap Listesi\n1-Üye Listesi\n2-Kitap Ekle\n3-Kitap Sil\n4-Üye Ekle\n5-Üye Sil\n6-Kitap Ödünç Ver\n7-Kitap İade Al\n8-Çıkış\n \nSeçim: ")
    print("*"*20)

    if Menu == "0":
        if len(library.collection) == 0 or library.collection == False:
            print("Kitap kaydı bulunamadı.")
        else:
            for books in library.collection:
                if library.collection[books]["isLent"] == False:
                    print(f"{books} - {library.collection[books]['name']} - {library.collection[books]['author']} - {library.collection[books]['year']} - {library.collection[books]['publisher']} [RAFTA]")
                else:
                    print(f"{books} - {library.collection[books]['name']} - {library.collection[books]['author']} - {library.collection[books]['year']} - {library.collection[books]['publisher']} [ÖDÜNÇ VERİLDİ]")

    elif Menu == "1":
        if len(library.members) == 0:
            print("Üye kaydı bulunamadı.")
        else:
            for members in library.members:
                print(f"No: {members} Üye Adı: {library.members[members]['name']} - Telefon Numarası: {library.members[members]['phoneNumber']} - Email adresi: {library.members[members]['email']} - İkamet Adresi: {library.members[members]['address']}")
                if library.members[members]["booksLent"] != []:
                    print(f"Kitaplar: {library.members[members]['booksLent']}")
    elif Menu == "2":
         library.addBook()
    elif Menu == "3":
        id = int(input("Silinecek kitabın numarasını girin: "))
        library.removeBook(id)
    elif Menu == "4":
        library.addMember()
    elif Menu == "5":
         library.deleteMember(int(input("Silinecek üyenin numarasını girin: ")))
    elif Menu == "6":
         library.lendBook(int(input("Ödünç verilen üyenin numarasını girin: ")),int(input("Kitabın numarasını girin: ")))
    elif Menu == "7":
        library.returnBook(int(input("İade alınan üyenin numarasını girin: ")),int(input("Kitabın numarasını girin: ")))
    elif Menu == "8":
        print("Programdan çıkılıyor...")
        break
    else:
        print("Hatalı giris.")
