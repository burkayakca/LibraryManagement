import json

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
        self.collection = { 0 : {
            "name" : "Moby Dick",
            "author" : "Herman Melville",
            "year" : "1851",
            "publisher" : "Macmillan",
            "isLent" : False,
            "LentTo" : ""
            }
            ,
            1 : {
            "name" : "Yüzüklerin Efendisi",
            "author" : "J.R.R. Tolkien",
            "year" : "1954",
            "publisher" : "Yapıkredi Yayınları",
            "isLent" : False,
            "LentTo" : ""
            }
        }
        
        self.members = {
            0 : {
            "name" : "Mehmet",
            "phoneNumber" : "0555 555 55 55",
            "email" : "mehmet@yildiz.com",
            "address" : "Ankara",
            "booksLent" : []
            },
            1 : {
            "name" : "Ali",
            "phoneNumber" : "0555 555 55 55",
            "email" : "ali@yildiz.com",
            "address" : "Ankara",
            "booksLent" : []
            }
        }

    def writeToDatabase(self,database):
        if database == "members":
            with open ("members.json","w",encoding="utf-8") as file:
                json_string = json.dumps(self.members, ensure_ascii=False)
                file.write(json_string)
        elif database == "collection":
            with open ("collection.json","w",encoding="utf-8") as file:
                json_string = json.dumps(self.collection, ensure_ascii=False)
                file.write(json_string)
    def addBook(self):
        
        while True:
            bookID = int(input("Kitaba atanacak bir numara girin: "))
            if bookID in self.collection:
                print(f"Hata: {bookID} numarası mevcut bir kitaba atanmış. Farklı bir numara girin ")
            else:
                break
        
        book = Book(input("Kitap adı: "),input("Yazar: "),input("Yıl: "),input("Yayınevi: "))
        
        self.collection[bookID] = {
            "name" : book.name,
            "author" : book.author,
            "year" : book.year,
            "publisher" : book.publisher,
            "isLent" : False,
            "LentTo" : ""
        }
        
        self.writeToDatabase("collection")

        print(f"{book.name} adlı kitap eklendi")
        print(self.collection)


    def removeBook(self,bookID):
        if bookID in self.collection:
            if self.collection[bookID]["isLent"] == True:
                LentToID = self.collection[bookID]["LentTo"]
                DeleteLentBook = input(f"Kitap, {LentToID} numaralı üye'ye ödünç verilmiş gözüküyor. Yine de silinsim mi?(E/H)")
                if DeleteLentBook == "E" or DeleteLentBook == "e":
                    self.members[LentToID]["booksLent"].remove(self.collection[bookID])
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

        while True:
            memberID = int(input("Üyelik numarası girin: "))
            if memberID in self.collection:
                print(f"Hata: {memberID} numarası mevcut bir üyeye atanmış. Lütfen farklı bir numara girin.")
            else:
                break

        member = Member(input("Ad: "),input("Telefon: "),input("E-posta: "),input("Adres: "))

        self.members[memberID] = {
            "name" : member.name,
            "phoneNumber" : member.phoneNumber,
            "email" : member.email,
            "address" : member.address,
            "booksLent" : []
        }

        self.writeToDatabase("members")



    def lendBook(self,MemberID,bookID):
        if self.members[MemberID]:
            if self.collection[bookID]:
                if self.collection[bookID]["isLent"] == False:
                    self.members[MemberID]["booksLent"].append(self.collection[bookID])
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
        if bookID in self.collection:
            if MemberID in self.members:
                self.members[MemberID]["booksLent"].remove(self.collection[bookID])
                self.collection[bookID]["isLent"] = False
                print("Kitap iade alındı")
                self.writeToDatabase("collection")
                self.writeToDatabase("members")
            else:
                print(f"{MemberID} numaralı kişinin kaydı bulunamadı.")
        else:
            print("Kitap bulunamadı")

    def deleteMember(self,MemberID):
        if len(self.members) == 0:
            print("Kayıtlı üye bulunamadı.")
        else:
            if self.members[MemberID]:
                if self.members[MemberID]["booksLent"] == []:
                    del self.members[MemberID]
                    print("Üye silindi.")
                    self.writeToDatabase("members")
                else:
                    print(f"Hata: üye'nin iade etmediği kitap(lar) mevcut.\n {self.members[int(MemberID)]['booksLent']}")
            else:
                print("Bu isimde bir kullanıcı bulunamadı.")

library = Library()

while True:

    Menu = input("\n0-Kitap Listesi\n1-Üye Listesi\n2-Kitap Ekle\n3-Kitap Sil\n4-Üye Ekle\n5-Üye Sil\n6-Kitap Ödünç Ver\n7-Kitap İade Al\n8-Cıkıs\n \nSecim: ")
    print("*"*20)

    if Menu == "0":
        if len(library.collection) == 0:
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
